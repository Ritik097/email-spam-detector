# Prompt 1 – Problem Analysis

## AI-Based Email Spam Detection Web Application

---

## 1. The Real-World Problem: Email Spam

Email spam refers to unsolicited, unwanted, or fraudulent messages sent in bulk
to large numbers of recipients. These emails are typically sent for commercial
advertising, phishing scams, malware distribution, or financial fraud.

### Why Is It a Problem?

| Problem | Impact on Users |
|---|---|
| **Phishing attacks** | Criminals impersonate banks, PayPal, or government agencies to steal passwords and financial details |
| **Financial scams** | Fake lottery wins, loan offers, and gift card claims trick users into sending money |
| **Malware links** | Spam emails often carry links or attachments that install viruses on the user's device |
| **Productivity loss** | Employees and students waste time sorting through irrelevant messages every day |
| **Storage waste** | Bulk spam emails consume inbox storage and slow down email services |
| **Psychological stress** | Constant unwanted messages cause frustration and reduce trust in email communication |

### Statistics (Why This Matters)
- More than **45% of all global email traffic** is spam.
- Phishing emails cost businesses billions of dollars in losses each year.
- Over **3 billion phishing emails** are sent every single day worldwide.

---

## 2. Problem Statement

> "Users receive a large number of unwanted and potentially harmful emails daily.
> Manually identifying spam messages is time-consuming, unreliable, and error-prone.
> There is a need for an automated, intelligent system that can accurately
> classify emails as spam or legitimate."

---

## 3. How Machine Learning Solves This Problem

Machine learning allows a computer to **learn patterns** from past examples of
spam and legitimate emails. Once trained, the model can automatically classify
new, unseen emails — without needing manually written rules.

### Why Naive Bayes?
- **Fast to train** – suitable for large email datasets.
- **Works well with text data** – email classification is a text problem.
- **High accuracy for spam detection** – industry-standard choice for this task.
- **Beginner-friendly** – simple probability calculations that are easy to understand.
- **Proven in production** – Gmail's first spam filter was based on Naive Bayes.

### ML Approach Used in This Project

```
Email Text → CountVectorizer (text → numbers) → Multinomial Naive Bayes → Spam / Not Spam
```

---

## 4. Proposed Solution

Build a web application where:
1. The user pastes or types an email message.
2. A trained ML model analyses the text.
3. The application returns a clear prediction: **Spam** or **Not Spam**.
4. A confidence percentage is shown to indicate how certain the model is.

---

## 5. Project Objectives

1. Train a Multinomial Naive Bayes classifier on labelled email data.
2. Build a simple Flask web interface for user interaction.
3. Connect the trained model to the web interface.
4. Display results clearly with visual indicators (colour-coded).
5. Handle edge cases: empty input, very short messages.
6. Demonstrate model performance using accuracy, precision, recall, and F1-score.

---

## 6. Expected Outcome

| Deliverable | Description |
|---|---|
| Trained ML model | A `.pkl` file saved with joblib |
| Web application | A Flask app accessible at `http://127.0.0.1:5000` |
| Prediction interface | Enter email text, click Predict, see result instantly |
| Model evaluation | Printed accuracy, precision, recall, F1-score, confusion matrix |
| Project documentation | This folder of markdown documents |

---

## 7. Suitability for Semester 3

This project is well-suited for a Semester 3 Computer Science student because:

- It uses **Python**, which students learn from Semester 1.
- The ML algorithm (Naive Bayes) is introduced early in AI/ML courses.
- The web framework (Flask) is lightweight and beginner-friendly.
- The dataset handling (Pandas + CSV) reinforces Python data handling skills.
- The project demonstrates a complete, end-to-end AI application lifecycle:
  data → model → evaluation → deployment.
