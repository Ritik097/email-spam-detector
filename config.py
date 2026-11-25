"""
config.py
---------
Central configuration for the Email Spam Detector.
Reads from environment variables when deployed to Render/cloud.
Falls back to local defaults for development.
"""

import os

# ── MongoDB ───────────────────────────────────────────────────────────────────
# On Render: set MONGO_URI env var to your MongoDB Atlas connection string
# Locally:   uses localhost
MONGO_URI        = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB         = os.environ.get("MONGO_DB", "spam_detector")
MONGO_COLLECTION = "emails"

# ── App ───────────────────────────────────────────────────────────────────────
HOST          = "0.0.0.0"
PORT          = int(os.environ.get("PORT", 5001))
POLL_INTERVAL = 60
MAX_EMAILS    = 200
