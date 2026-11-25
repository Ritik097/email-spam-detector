"""
gmail_fetcher.py
----------------
Connects to Gmail via the official Google Gmail API (OAuth2).
Fetches unread emails, decodes the body, and returns them
as a list of dicts ready for spam detection.

Setup (do this ONCE):
  1. Go to https://console.cloud.google.com/
  2. Create a project → Enable Gmail API
  3. Create OAuth2 credentials (Desktop app) → Download as credentials.json
  4. Place credentials.json in this folder (gmail_integration/)
  5. Run:  pip install google-auth google-auth-oauthlib google-api-python-client
  6. First run will open a browser for you to log in — token.json is saved after that.
"""

import os
import base64
import json
from email import message_from_bytes

# Google API libraries (install via: pip install google-auth-oauthlib google-api-python-client)
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
TOKEN_PATH       = os.path.join(BASE_DIR, "token.json")


def get_gmail_service():
    """Authenticate and return a Gmail API service object."""
    if not GMAIL_AVAILABLE:
        raise ImportError(
            "Google API libraries not installed.\n"
            "Run: pip install google-auth google-auth-oauthlib google-api-python-client"
        )
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            f"credentials.json not found at {CREDENTIALS_PATH}\n"
            "Download it from https://console.cloud.google.com/ → APIs & Services → Credentials"
        )

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _decode_body(payload):
    """Recursively extract plain text body from a Gmail message payload."""
    body = ""
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    elif mime_type.startswith("multipart/"):
        for part in payload.get("parts", []):
            body += _decode_body(part)

    return body


def fetch_unread_emails(max_results=20):
    """
    Fetch up to `max_results` unread emails from the inbox.

    Returns a list of dicts:
      {
        "id":       Gmail message ID (string),
        "subject":  Email subject,
        "sender":   From address,
        "snippet":  Short preview text,
        "body":     Full plain-text body (may be empty for HTML-only emails),
        "date":     Email date string,
        "labels":   List of Gmail label IDs
      }
    """
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg_ref in messages:
        msg = service.users().messages().get(
            userId="me",
            id=msg_ref["id"],
            format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
        body    = _decode_body(msg["payload"]) or msg.get("snippet", "")

        emails.append({
            "id":      msg["id"],
            "subject": headers.get("Subject", "(No Subject)"),
            "sender":  headers.get("From", "Unknown"),
            "snippet": msg.get("snippet", ""),
            "body":    body.strip(),
            "date":    headers.get("Date", ""),
            "labels":  msg.get("labelIds", []),
        })

    return emails
