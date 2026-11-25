"""
email_store.py
--------------
MongoDB-backed store for classified emails.
Falls back to in-memory storage if MongoDB is unavailable
(so the app still starts on Render even before MONGO_URI is set).
"""

import threading
from datetime import datetime
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, MAX_EMAILS

# ── State ─────────────────────────────────────────────────────────────────────
_lock          = threading.Lock()
_status        = "idle"
_error_message = ""
_last_updated  = None

# MongoDB objects – set to None until first successful connection
_client        = None
_col           = None
_mongo_ok      = False          # True once we confirm MongoDB is reachable

# In-memory fallback used when MongoDB is unavailable
_mem_emails    = []


# ── MongoDB connection ────────────────────────────────────────────────────────
def _connect():
    """Try to connect to MongoDB. Returns the collection or None."""
    global _client, _col, _mongo_ok
    if _mongo_ok and _col is not None:
        return _col
    try:
        from pymongo import MongoClient, DESCENDING
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")           # test the connection
        db    = client[MONGO_DB]
        col   = db[MONGO_COLLECTION]
        col.create_index("email_id", unique=True)
        _client   = client
        _col      = col
        _mongo_ok = True
        print(f"[MongoDB] Connected → {MONGO_URI}  db={MONGO_DB}  col={MONGO_COLLECTION}")
        return _col
    except Exception as exc:
        _mongo_ok = False
        print(f"[MongoDB] Unavailable – using in-memory store. ({exc})")
        return None


# ── Status helpers ────────────────────────────────────────────────────────────
def set_status(status, error=""):
    global _status, _error_message
    with _lock:
        _status        = status
        _error_message = error


def get_status():
    with _lock:
        return {
            "status":       _status,
            "error":        _error_message,
            "last_updated": _last_updated.isoformat() if _last_updated else None,
            "storage":      "mongodb" if _mongo_ok else "memory",
        }


# ── Write ─────────────────────────────────────────────────────────────────────
def upsert_emails(classified_list):
    global _last_updated
    col = _connect()

    if col is not None:
        # ── MongoDB path ──────────────────────────────────────────────────────
        from pymongo import errors as me, DESCENDING
        for email in classified_list:
            doc = {**email, "email_id": email["id"]}
            try:
                col.update_one(
                    {"email_id": email["id"]},
                    {"$setOnInsert": doc},
                    upsert=True,
                )
            except me.DuplicateKeyError:
                pass
        # Prune to MAX_EMAILS
        total = col.count_documents({})
        if total > MAX_EMAILS:
            oldest = [
                d["_id"] for d in
                col.find({}, {"_id": 1})
                   .sort("classified_at", DESCENDING)
                   .skip(MAX_EMAILS)
            ]
            if oldest:
                col.delete_many({"_id": {"$in": oldest}})
    else:
        # ── In-memory fallback ────────────────────────────────────────────────
        with _lock:
            existing = {e["id"] for e in _mem_emails}
            for email in classified_list:
                if email["id"] not in existing:
                    _mem_emails.insert(0, email)
            del _mem_emails[MAX_EMAILS:]

    with _lock:
        _last_updated = datetime.now()


# ── Read ──────────────────────────────────────────────────────────────────────
def get_emails(limit=100):
    col = _connect()
    if col is not None:
        from pymongo import DESCENDING
        return list(
            col.find({}, {"_id": 0, "email_id": 0})
               .sort("classified_at", DESCENDING)
               .limit(limit)
        )
    with _lock:
        return list(_mem_emails[:limit])


def get_stats():
    col = _connect()
    if col is not None:
        total = col.count_documents({})
        spam  = col.count_documents({"label": "spam"})
        ham   = col.count_documents({"label": "ham"})
    else:
        with _lock:
            total = len(_mem_emails)
            spam  = sum(1 for e in _mem_emails if e.get("label") == "spam")
            ham   = sum(1 for e in _mem_emails if e.get("label") == "ham")
    return {
        "total":    total,
        "spam":     spam,
        "ham":      ham,
        "spam_pct": round(spam / total * 100, 1) if total else 0,
    }


def clear():
    col = _connect()
    if col is not None:
        col.delete_many({})
    with _lock:
        _mem_emails.clear()
