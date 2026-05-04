import subprocess
import time
import threading
import queue
import sys

def log_cot(message: str):
    with open("openclaw_session.log", "a") as f:
        f.write(f"[CoT] {message}\n")
    print(f"[CoT] {message}")

def run_utility_gap_finder():
    log_cot("Triggering UtilityGapFinder.skill to identify high-value use for expiring items...")
    result = subprocess.run([sys.executable, "UtilityGapFinder.skill/gap_finder.py"], capture_output=True, text=True)
    log_cot(f"UtilityGapFinder output:\n{result.stdout.strip()}")

def enqueue_output(out, q):
    for line in iter(out.readline, ''):
        q.put(line)
    out.close()

def main():
    log_cot("Initializing AetherShelf Agent Internal Reasoning")
    log_cot("Starting Flux Engine to monitor physical layer (pantry_ledger.yaml)")
    
    # Start flux engine as a background process
    flux_proc = subprocess.Popen(
        [sys.executable, "flux_engine.py"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        text=True,
        bufsize=1
    )
    
    q = queue.Queue()
    t = threading.Thread(target=enqueue_output, args=(flux_proc.stdout, q))
    t.daemon = True
    t.start()
    
    time.sleep(2) # Wait for engine to initialize and read ledger
    
    log_cot("Triggering EmailParser.skill to process cyber layer inputs (receipts)")
    email_result = subprocess.run([sys.executable, "EmailParser.skill/email_parser.py"], capture_output=True, text=True)
    log_cot(f"EmailParser output:\n{email_result.stdout.strip()}")
    
    log_cot("Waiting for Flux Engine to react to ledger changes...")
    
    start_time = time.time()
    action_triggered = False
    
    while time.time() - start_time < 5:
        try:
            line = q.get_nowait()
        except queue.Empty:
            time.sleep(0.1)
            continue
        
        if line:
            log_cot(f"[Flux Engine] {line.strip()}")
            if "target_skill: UtilityGapFinder.skill" in line or "UtilityGapFinder.skill" in line:
                action_triggered = True
                break
                
    if action_triggered:
        log_cot("Detected OpenClaw Action from Flux Engine.")
        run_utility_gap_finder()
    else:
        log_cot("No actionable trigger from Flux Engine.")
        
    log_cot("Shutting down internal reasoning.")
    flux_proc.terminate()

if __name__ == "__main__":
    main()
