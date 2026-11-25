"""
app.py  –  Email Spam Detector  (MongoDB Edition)
--------------------------------------------------
Routes:
  GET  /              → Live dashboard
  GET  /manual        → Manual text entry
  POST /predict       → Manual prediction API
  GET  /api/emails    → JSON: all emails from MongoDB
  GET  /api/status    → JSON: poller + DB status
  GET  /api/stats     → JSON: spam/ham counts from MongoDB
"""

import os
import joblib
from flask import Flask, render_template, request, jsonify
from gmail_integration import email_store, poller
from config import HOST, PORT

app = Flask(__name__)

# ── Load ML model ─────────────────────────────────────────────────────────────
MODEL_PATH = "model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"'{MODEL_PATH}' not found.  Run  python train_model.py  first."
    )
model = joblib.load(MODEL_PATH)
print(f"[App] Model loaded from '{MODEL_PATH}'.")

# ── Start background email poller ─────────────────────────────────────────────
poller.start(model)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/manual")
def manual():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or "email_text" not in data:
        return jsonify({"error": "No email text provided."}), 400

    text = data["email_text"].strip()
    if not text:
        return jsonify({"error": "Email text cannot be empty."}), 400
    if len(text) < 3:
        return jsonify({"error": "Email text is too short to analyse."}), 400

    label      = model.predict([text])[0]
    probs      = model.predict_proba([text])[0]
    classes    = list(model.classes_)
    spam_prob  = probs[classes.index("spam")] * 100
    confidence = round(spam_prob if label == "spam" else 100 - spam_prob, 2)

    return jsonify({
        "prediction": "Spam Email" if label == "spam" else "Not Spam Email",
        "confidence": confidence,
        "label":      label,
        "message": (
            "⚠️ This email looks suspicious. It has characteristics commonly "
            "found in spam or phishing messages."
            if label == "spam" else
            "✅ This email appears to be legitimate. No spam indicators were detected."
        ),
    })


@app.route("/api/emails")
def api_emails():
    return jsonify(email_store.get_emails())


@app.route("/api/status")
def api_status():
    return jsonify(email_store.get_status())


@app.route("/api/stats")
def api_stats():
    return jsonify(email_store.get_stats())


# ── Entry point (local dev only — gunicorn uses app:app directly) ─────────────
if __name__ == "__main__":
    print(f"[App] Starting on http://{HOST}:{PORT}")
    app.run(debug=False, host=HOST, port=PORT)
