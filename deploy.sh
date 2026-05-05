#!/bin/bash
# ==============================================================================
# AetherShelf Firebase Deployment Script
# ==============================================================================

echo "Initializing Firebase Deploy Sequence..."

# Check if firebase-tools is installed
if ! command -v firebase &> /dev/null
then
    echo "⚠️ Firebase CLI could not be found."
    echo "Please install it globally via: npm install -g firebase-tools"
    exit 1
fi

echo "[*] Authenticating with Google Cloud..."
# Note: Ensure you have run 'firebase login' previously!

echo "[*] Deploying AetherShelf Frontend to Firebase Hosting..."
firebase deploy --only hosting

echo "=============================================================================="
echo "✅ Deployment Successful!"
echo "Check your terminal output above for the official Google Firebase URL."
echo "=============================================================================="
