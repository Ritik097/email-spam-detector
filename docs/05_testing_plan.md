# Prompt 5 – Testing Plan

## AI-Based Email Spam Detection Web Application

---

## 1. Testing Objectives

- Verify that the ML model classifies spam and legitimate emails correctly.
- Ensure the web interface handles all types of user input gracefully.
- Confirm that error handling works for empty and invalid inputs.
- Validate that the Predict and Clear buttons function as expected.
- Check that the model evaluation metrics are within acceptable ranges.

---

## 2. Types of Testing

| Type | Description |
|---|---|
| **Functional Testing** | Does each feature work as designed? |
| **Input Validation Testing** | Does the app handle bad input without crashing? |
| **UI Testing** | Do all buttons, displays, and interactions behave correctly? |
| **Model Evaluation Testing** | Does the trained model meet accuracy targets? |

---

## 3. Model Evaluation Metrics – How to Interpret Them

Run `python train_model.py` to see these metrics printed in the terminal.

| Metric | Formula | Target |
|---|---|---|
| **Accuracy** | (TP + TN) / Total | > 90% |
| **Precision** | TP / (TP + FP) | > 85% |
| **Recall** | TP / (TP + FN) | > 85% |
| **F1-Score** | 2 × (Precision × Recall) / (Precision + Recall) | > 85% |

**Confusion Matrix:**
```
                 Predicted Spam   Predicted Ham
Actual Spam  →       TP               FN
Actual Ham   →       FP               TN
```
- **TP (True Positive):** Model correctly identified a spam email as spam.
- **TN (True Negative):** Model correctly identified a legitimate email as not spam.
- **FP (False Positive):** Model incorrectly flagged a legitimate email as spam (False Alarm).
- **FN (False Negative):** Model missed a spam email and classified it as legitimate.

---

## 4. Test Cases

> **Note to student:** Run each test case after launching the application.
> Fill in the **Actual Result** and **Status** columns based on your observations.

---

### Section A – Input and Prediction Tests

| TC# | Test Case | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC-01 | Normal legitimate email | "Hi John, please find attached the meeting notes from today's session." | Result: **Not Spam Email** | _(fill in)_ | _(Pass / Fail)_ |
| TC-02 | Promotional spam email | "Congratulations! You have won $10,000. Click here to claim your prize now!" | Result: **Spam Email** | _(fill in)_ | _(Pass / Fail)_ |
| TC-03 | Phishing email with link | "URGENT: Your PayPal account is suspended. Verify at http://fake-login.com immediately." | Result: **Spam Email** | _(fill in)_ | _(Pass / Fail)_ |
| TC-04 | Very short input | "Hi" | Result: Error – "Email text is too short to analyse" | _(fill in)_ | _(Pass / Fail)_ |
| TC-05 | Long legitimate email | A multi-paragraph professional email (200+ words about project updates) | Result: **Not Spam Email** | _(fill in)_ | _(Pass / Fail)_ |
| TC-06 | Email with only spaces | "          " (whitespace only) | Result: Error – "Please enter some email text" | _(fill in)_ | _(Pass / Fail)_ |
| TC-07 | Email with numbers and symbols | "Your OTP is 456321. Valid for 10 minutes. Do not share this code." | Result: **Not Spam Email** | _(fill in)_ | _(Pass / Fail)_ |
| TC-08 | Spam keywords email | "FREE offer! Buy now! Limited time! Click here! Win money! Cheap pills!" | Result: **Spam Email** | _(fill in)_ | _(Pass / Fail)_ |

---

### Section B – UI / Button Tests

| TC# | Test Case | Action | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC-09 | Predict button – normal use | Type a valid email and click Predict | Spinner appears briefly; result card shows with prediction | _(fill in)_ | _(Pass / Fail)_ |
| TC-10 | Predict button – empty input | Leave textarea empty and click Predict | Error message shown: "Please enter some email text" | _(fill in)_ | _(Pass / Fail)_ |
| TC-11 | Clear button | Type text, then click Clear | Textarea is emptied; character count resets to 0; result card disappears | _(fill in)_ | _(Pass / Fail)_ |
| TC-12 | Character counter | Type 50 characters | Counter shows "50 characters" | _(fill in)_ | _(Pass / Fail)_ |
| TC-13 | Sample email loader – Spam 1 | Click "🚨 Spam Example 1" | Sample spam email loaded into textarea | _(fill in)_ | _(Pass / Fail)_ |
| TC-14 | Sample email loader – Ham 1 | Click "✅ Legitimate Example 1" | Sample legitimate email loaded into textarea | _(fill in)_ | _(Pass / Fail)_ |
| TC-15 | Enter key shortcut | Type email and press Enter | Prediction triggered (same as clicking Predict) | _(fill in)_ | _(Pass / Fail)_ |

---

### Section C – Model and System Tests

| TC# | Test Case | Method | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC-16 | Model file exists | Check that `model.pkl` is present after `python train_model.py` | File `model.pkl` exists in the project root | _(fill in)_ | _(Pass / Fail)_ |
| TC-17 | Model loads at startup | Run `python app.py` and check terminal | Terminal prints: "Model loaded from 'model.pkl'." | _(fill in)_ | _(Pass / Fail)_ |
| TC-18 | Model accuracy | Run `python train_model.py` and read terminal output | Accuracy printed is > 90% | _(fill in)_ | _(Pass / Fail)_ |
| TC-19 | Missing model file | Delete `model.pkl` and run `python app.py` | App raises `FileNotFoundError` with a helpful message | _(fill in)_ | _(Pass / Fail)_ |
| TC-20 | App runs without errors | Run `python app.py` | No errors in terminal; app accessible at http://127.0.0.1:5000 | _(fill in)_ | _(Pass / Fail)_ |

---

## 5. How to Run the Tests

1. Open Terminal in VS Code (`` Ctrl+` ``).
2. Activate your virtual environment: `source venv/bin/activate`
3. Train the model: `python train_model.py` → note the printed metrics.
4. Start the app: `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.
6. Work through each test case in Section A and B one by one.
7. Fill in the Actual Result and Status columns in the table above.

---

## 6. Acceptance Criteria

The project is considered complete and ready for submission if:

- [ ] All TC-01 to TC-08 input tests produce the expected result.
- [ ] All TC-09 to TC-15 UI tests behave correctly.
- [ ] Model accuracy is above 90% (TC-18).
- [ ] The app starts without any errors (TC-20).
- [ ] No unhandled Python exceptions appear in the terminal during testing.
