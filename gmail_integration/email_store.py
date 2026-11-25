"""
email_store.py
--------------
MongoDB-backed store for classified emails.
Replaces the previous in-memory list.

Collection  :  spam_detector.emails
Index       :  { email_id: 1 }  (unique — prevents duplicates)
"""

import threading
from datetime import datetime
from pymongo import MongoClient, DESCENDING, errors as mongo_errors
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, MAX_EMAILS

# ── Connection ────────────────────────────────────────────────────────────────
_lock   = threading.Lock()
_client = None
_col    = None

_status        = "idle"
_error_message = ""
_last_updated  = None


def _get_collection():
    global _client, _col
    if _col is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000)
        db      = _client[MONGO_DB]
        _col    = db[MONGO_COLLECTION]
        # Unique index on email_id so upserts never duplicate
        _col.create_index("email_id", unique=True)
        print(f"[MongoDB] Connected → {MONGO_URI}  db={MONGO_DB}  col={MONGO_COLLECTION}")
    return _col


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
        }


# ── Write ─────────────────────────────────────────────────────────────────────
def upsert_emails(classified_list):
    """
    Insert new classified emails into MongoDB.
    Skips emails that already exist (matched by email_id).
    Prunes oldest records so the collection stays under MAX_EMAILS.
    """
    global _last_updated
    col = _get_collection()

    for email in classified_list:
        doc = {**email, "email_id": email["id"]}    # keep original id + add indexed field
        try:
            col.update_one(
                {"email_id": email["id"]},
                {"$setOnInsert": doc},
                upsert=True,
            )
        except mongo_errors.DuplicateKeyError:
            pass    # already exists — skip

    # Prune: keep only the MAX_EMAILS most recent documents
    total = col.count_documents({})
    if total > MAX_EMAILS:
        oldest_ids = [
            d["_id"]
            for d in col.find({}, {"_id": 1})
                        .sort("classified_at", DESCENDING)
                        .skip(MAX_EMAILS)
        ]
        if oldest_ids:
            col.delete_many({"_id": {"$in": oldest_ids}})

    with _lock:
        _last_updated = datetime.now()


# ── Read ──────────────────────────────────────────────────────────────────────
def get_emails(limit=100):
    """Return up to `limit` emails, newest first."""
    col  = _get_collection()
    docs = list(
        col.find({}, {"_id": 0, "email_id": 0})
           .sort("classified_at", DESCENDING)
           .limit(limit)
    )
    return docs


def get_stats():
    col   = _get_collection()
    total = col.count_documents({})
    spam  = col.count_documents({"label": "spam"})
    ham   = col.count_documents({"label": "ham"})
    return {
        "total":    total,
        "spam":     spam,
        "ham":      ham,
        "spam_pct": round(spam / total * 100, 1) if total else 0,
    }


def clear():
    col = _get_collection()
    col.delete_many({})
