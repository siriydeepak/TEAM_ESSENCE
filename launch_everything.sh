#!/bin/bash
# ==============================================================================
# AetherShelf Hybrid Launch Sequence (Local Brain + Global Face)
# ==============================================================================

echo "=================================================="
echo "Initializing AetherShelf Production Stack"
echo "=================================================="

# Check if firebase is installed
if ! command -v firebase &> /dev/null
then
    echo "⚠️ Firebase CLI could not be found."
    echo "Please run: npm install -g firebase-tools"
    echo "Then run: firebase login"
    exit 1
fi

echo "[1/3] 🌐 Pushing Frontend to Google Firebase..."
firebase deploy --only hosting

echo ""
echo "[2/3] ✅ Firebase Deployment Complete!"
echo "Your Official Google Link is printed above (e.g., https://your-project.web.app)."
echo "Make sure to update the API_BASE in public/index.html to point to your backend."
echo ""

echo "[3/3] 🧠 Igniting Local OpenClaw Gateway (The Brain)..."
# Starting the FastAPI backend to observe the pantry and serve the API
python main.py
