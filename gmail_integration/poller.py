"""
poller.py
---------
Background thread that fetches new emails from Gmail every POLL_INTERVAL seconds,
runs the ML model on each one, and stores results in email_store.

If Gmail credentials are not set up, it runs in DEMO mode with fake emails
so the dashboard still works for academic demonstration.
"""

import os
import time
import threading
import random
from datetime import datetime

from gmail_integration import email_store

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import POLL_INTERVAL
_stop_event   = threading.Event()


# ── Demo emails (used when Gmail is not configured) ───────────────────────────
DEMO_EMAILS = [
    {
        "id": "demo_001",
        "subject": "Congratulations! You've Won $10,000 Prize",
        "sender": "noreply@prize-scam.fake",
        "snippet": "Click here to claim your reward immediately before it expires...",
        "body": "Congratulations! You have been selected as the lucky winner of our $10,000 prize draw. Click the link below to claim your reward. This offer expires in 24 hours. Reply with your bank details.",
        "date": "Mon, 25 Nov 2026 08:00:00 +0000",
    },
    {
        "id": "demo_002",
        "subject": "Team Meeting Tomorrow at 10 AM",
        "sender": "manager@company.com",
        "snippet": "Hi, just a reminder about our team standup tomorrow morning...",
        "body": "Hi everyone, just a reminder that we have our weekly team meeting tomorrow at 10 AM in Conference Room B. Please bring your project updates. Thanks, James",
        "date": "Mon, 25 Nov 2026 09:15:00 +0000",
    },
    {
        "id": "demo_003",
        "subject": "URGENT: Verify Your PayPal Account Now",
        "sender": "security@paypal-fake.net",
        "snippet": "Your account has been suspended. Click to verify immediately...",
        "body": "URGENT: We detected suspicious activity on your PayPal account. Your account will be permanently suspended unless you verify your information within 24 hours. Click here: http://paypal-verify.fake/login",
        "date": "Mon, 25 Nov 2026 10:30:00 +0000",
    },
    {
        "id": "demo_004",
        "subject": "Assignment Submission Received - CS301",
        "sender": "noreply@university.edu",
        "snippet": "Your ML lab assignment has been received. Submission ID: ML-2024-0892",
        "body": "Dear Student, your assignment submission for Machine Learning Lab (CS301) has been received successfully. Your submission ID is ML-2024-0892. Graded results will be published within 5 working days. Academic Office",
        "date": "Mon, 25 Nov 2026 11:00:00 +0000",
    },
    {
        "id": "demo_005",
        "subject": "FREE iPhone 15 - Exclusive Offer for You!",
        "sender": "deals@win-free-stuff.fake",
        "snippet": "You have been selected for our exclusive FREE iPhone giveaway...",
        "body": "FREE offer! You have been exclusively selected to receive a brand new iPhone 15 at no cost. Limited time only. Click here to claim your free phone now before stocks run out. Act immediately!",
        "date": "Mon, 25 Nov 2026 12:00:00 +0000",
    },
    {
        "id": "demo_006",
        "subject": "Project Proposal Review - Feedback Inside",
        "sender": "professor@university.edu",
        "snippet": "I have reviewed your semester project proposal and have some feedback...",
        "body": "Dear Ritik, I have reviewed your AI-based spam detection project proposal. Overall it is well-structured. Please add more detail to the methodology section and clarify your dataset source. Good work so far. Dr. Sharma",
        "date": "Mon, 25 Nov 2026 13:45:00 +0000",
    },
]


def _classify_email(model, email):
    """Run the ML model on an email and add prediction fields."""
    text_to_classify = email.get("body") or email.get("snippet", "")

    if not text_to_classify.strip():
        label      = "unknown"
        prediction = "Unknown"
        confidence = 0.0
    else:
        try:
            label       = model.predict([text_to_classify])[0]
            probs       = model.predict_proba([text_to_classify])[0]
            classes     = list(model.classes_)
            spam_prob   = probs[classes.index("spam")] * 100
            confidence  = round(spam_prob if label == "spam" else 100 - spam_prob, 1)
            prediction  = "Spam Email" if label == "spam" else "Not Spam Email"
        except Exception as e:
            label       = "error"
            prediction  = "Error"
            confidence  = 0.0

    return {**email,
            "label":      label,
            "prediction": prediction,
            "confidence": confidence,
            "classified_at": datetime.now().strftime("%H:%M:%S")}


def _run_demo_mode(model):
    """Simulate incoming emails for demonstration when Gmail is not configured."""
    email_store.set_status("demo")
    all_demo = [_classify_email(model, e) for e in DEMO_EMAILS]
    # Drip-feed: show 2 emails initially, add one more each poll cycle
    shown = []
    idx   = 0
    while not _stop_event.is_set():
        if idx < len(all_demo):
            shown.append(all_demo[idx])
            idx += 1
        email_store.upsert_emails(list(shown))
        _stop_event.wait(POLL_INTERVAL)


def _run_gmail_mode(model):
    """Real Gmail polling loop."""
    from gmail_integration.gmail_fetcher import fetch_unread_emails

    while not _stop_event.is_set():
        email_store.set_status("fetching")
        try:
            raw_emails = fetch_unread_emails(max_results=20)
            classified = [_classify_email(model, e) for e in raw_emails]
            email_store.upsert_emails(classified)
            email_store.set_status("ok")
        except Exception as ex:
            email_store.set_status("error", str(ex))
        _stop_event.wait(POLL_INTERVAL)


def start(model):
    """Start the background poller thread. Detects Gmail availability automatically."""
    _stop_event.clear()

    # Check whether Gmail credentials exist
    creds_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "credentials.json"
    )
    use_gmail = os.path.exists(creds_path)

    target = _run_gmail_mode if use_gmail else _run_demo_mode
    thread = threading.Thread(target=target, args=(model,), daemon=True, name="EmailPoller")
    thread.start()
    print(f"[Poller] Started in {'GMAIL' if use_gmail else 'DEMO'} mode.")
    return thread


def stop():
    _stop_event.set()
