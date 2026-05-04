import datetime
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "openclaw_session.log"

def notify_user(message: str, priority: str = "normal"):
    """OpenClaw event hook — logs to stdout and session log for Sentinel UI streaming."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} [OpenClaw] [NOTIFY | Priority: {priority.upper()}] {message}"
    print(f"\n{line}\n")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
