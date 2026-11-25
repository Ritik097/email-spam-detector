/**
 * main.js  –  Email Spam Detector
 *
 * Handles:
 *  - Live character counter
 *  - Predict button → POST /predict → render result
 *  - Clear button
 *  - Sample email loader
 */

"use strict";

// ── Sample emails ──────────────────────────────────────────────────────────
const SAMPLES = {
  spam1: `Congratulations! You have been selected as the lucky winner of our $10,000 prize draw!
To claim your reward, click the link below immediately. This offer expires in 24 hours.
Reply with your full name, address, and bank details to process your payment.
http://claim-your-prize-now.fake/win`,

  spam2: `URGENT: Your account will be suspended unless you verify your information NOW.
We detected suspicious activity on your PayPal account.
Click here to restore access: http://paypal-secure-login.fake/verify
Failure to act within 48 hours will result in permanent account closure.`,

  ham1: `Hi Sarah,

Just a quick reminder about our team meeting tomorrow at 10:00 AM in Conference Room B.
Please bring the Q3 budget spreadsheet so we can review it together.

Let me know if you have any questions before then.

Best regards,
James`,

  ham2: `Dear Student,

Your assignment submission for Machine Learning Lab (CS301) has been received successfully.
Your submission ID is: ML-2024-0892.

The graded results will be published on the student portal within 5 working days.

Academic Office
Department of Computer Science`,
};

// ── Character counter ─────────────────────────────────────────────────────
const emailInput = document.getElementById("emailInput");
const charCount  = document.getElementById("charCount");

emailInput.addEventListener("input", () => {
  charCount.textContent = emailInput.value.length;
});

// ── Load sample email ─────────────────────────────────────────────────────
function loadSample(key) {
  emailInput.value = SAMPLES[key] || "";
  charCount.textContent = emailInput.value.length;
  emailInput.focus();
  hideResult();
}

// ── Clear input ───────────────────────────────────────────────────────────
function clearInput() {
  emailInput.value = "";
  charCount.textContent = "0";
  emailInput.focus();
  hideResult();
}

// ── Hide result card ──────────────────────────────────────────────────────
function hideResult() {
  const card = document.getElementById("resultCard");
  card.classList.remove("visible");
  document.getElementById("resultContent").innerHTML = "";
}

// ── Predict ───────────────────────────────────────────────────────────────
async function predictSpam() {
  const text        = emailInput.value.trim();
  const predictBtn  = document.getElementById("predictBtn");
  const resultCard  = document.getElementById("resultCard");
  const resultContent = document.getElementById("resultContent");

  // Client-side validation
  if (!text) {
    showError("⚠️ Please enter some email text before clicking Predict.");
    return;
  }
  if (text.length < 3) {
    showError("⚠️ The email text is too short to analyse. Please enter more content.");
    return;
  }

  // Loading state
  predictBtn.disabled = true;
  predictBtn.innerHTML = '<span class="spinner"></span> Analysing…';
  hideResult();

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email_text: text }),
    });

    const data = await response.json();

    if (!response.ok || data.error) {
      showError("⚠️ " + (data.error || "An unexpected error occurred."));
      return;
    }

    renderResult(data);

  } catch (err) {
    showError(
      "⚠️ Could not connect to the server. Make sure the Flask app is running."
    );
  } finally {
    predictBtn.disabled = false;
    predictBtn.innerHTML = "🔎 Predict";
  }
}

// ── Render result ─────────────────────────────────────────────────────────
function renderResult(data) {
  const resultCard    = document.getElementById("resultCard");
  const resultContent = document.getElementById("resultContent");
  const isSpam        = data.label === "spam";

  const colorClass    = isSpam ? "result-spam" : "result-ham";
  const icon          = isSpam ? "🚨" : "✅";
  const barClass      = isSpam ? "bar-spam" : "bar-ham";

  resultContent.innerHTML = `
    <div class="${colorClass}">
      <div class="result-banner">
        <span class="result-icon">${icon}</span>
        <div>
          <div class="result-title">${escHtml(data.prediction)}</div>
          <div class="result-subtitle">Confidence: ${data.confidence}%</div>
        </div>
      </div>

      <div class="confidence-wrap">
        <div class="confidence-label">Model Confidence</div>
        <div class="confidence-bar-bg">
          <div
            class="confidence-bar-fill ${barClass}"
            style="width: 0%"
            id="confBar"
          ></div>
        </div>
      </div>

      <div class="result-message">${escHtml(data.message)}</div>
    </div>
  `;

  resultCard.classList.add("visible");

  // Animate the confidence bar after a brief delay
  requestAnimationFrame(() => {
    setTimeout(() => {
      const bar = document.getElementById("confBar");
      if (bar) bar.style.width = data.confidence + "%";
    }, 80);
  });

  // Scroll to result
  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Show error ────────────────────────────────────────────────────────────
function showError(message) {
  const resultCard    = document.getElementById("resultCard");
  const resultContent = document.getElementById("resultContent");

  resultContent.innerHTML = `
    <div class="result-error">
      <span style="font-size:1.5rem">⚠️</span>
      <span>${escHtml(message)}</span>
    </div>
  `;
  resultCard.classList.add("visible");
  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Utility: escape HTML to prevent XSS ──────────────────────────────────
function escHtml(str) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
  return String(str).replace(/[&<>"']/g, (m) => map[m]);
}

// ── Allow Enter key to trigger predict (Shift+Enter = newline) ────────────
emailInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    predictSpam();
  }
});
