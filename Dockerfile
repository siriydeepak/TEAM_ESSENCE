# AetherShelf Cloud Infrastructure - Pro Container
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bundle the Dashboard logic, Flux engine, and utilities
COPY api_bridge.py .
COPY ledger_handler.py .
COPY flux_engine.py .
COPY network_check.py .

# Include local skills so the UI can dynamically import required classes
COPY pantry_intel.skill/ ./pantry_intel.skill/
COPY EmailParser.skill/ ./EmailParser.skill/
COPY FluxAlgorithm.skill/ ./FluxAlgorithm.skill/
COPY CollisionDetection.skill/ ./CollisionDetection.skill/
COPY UtilityGapFinder.skill/ ./UtilityGapFinder.skill/

# Cloud providers typically map PORT dynamically
ENV PORT=8080
ENV CLOUD_MODE=true

EXPOSE 8080

# Execute the FastAPI bridge on the container network
CMD uvicorn api_bridge:app --host 0.0.0.0 --port ${PORT:-8080}
