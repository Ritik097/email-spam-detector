# Prompt 2 – Requirements

## AI-Based Email Spam Detection Web Application

---

## 1. Functional Requirements

Functional requirements describe **what the system must do**.

| # | Requirement | Description |
|---|---|---|
| FR-01 | Text Input Area | A large textarea where users can type or paste email content |
| FR-02 | Predict Button | A button that sends the email text to the ML model for classification |
| FR-03 | Clear Button | A button that removes the entered text and resets the result area |
| FR-04 | Spam Detection | The ML model must classify the email as "spam" or "ham" (not spam) |
| FR-05 | Result Display | The prediction must be displayed clearly: "Spam Email" or "Not Spam Email" |
| FR-06 | Confidence Score | Show the model's confidence percentage alongside the prediction |
| FR-07 | Result Message | Display an explanatory message describing the prediction result |
| FR-08 | Empty Input Handling | Show an error message if the user clicks Predict with no text |
| FR-09 | Short Input Handling | Reject inputs shorter than 3 characters with a helpful message |
| FR-10 | Sample Emails | Provide sample spam and legitimate emails for quick testing |
| FR-11 | Character Counter | Show a live count of characters entered in the textarea |

---

## 2. Non-Functional Requirements

Non-functional requirements describe **how the system must behave**.

| # | Requirement | Description |
|---|---|---|
| NFR-01 | Performance | Predictions must return within 1–2 seconds |
| NFR-02 | Usability | The interface must be simple enough for a non-technical user |
| NFR-03 | Accuracy | Model accuracy should be above 90% on the test dataset |
| NFR-04 | Responsiveness | The layout must work on both desktop and mobile screens |
| NFR-05 | Reliability | The app must handle unexpected inputs without crashing |
| NFR-06 | Maintainability | Code must be well-commented and organised into separate files |
| NFR-07 | Portability | The app must run on macOS, Windows, and Linux with the same setup |

---

## 3. Software Requirements

| Software | Version | Purpose |
|---|---|---|
| Python | 3.9 or higher | Main programming language |
| Flask | 2.3+ | Web framework for building the user interface |
| Pandas | 1.5+ | Loading and manipulating the CSV dataset |
| Scikit-learn | 1.2+ | ML pipeline, CountVectorizer, Naive Bayes, evaluation metrics |
| Joblib | 1.2+ | Saving and loading the trained model |
| VS Code | Latest | Development IDE |
| Web Browser | Chrome / Firefox / Safari | Accessing the web application |

---

## 4. Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Processor | Dual-core 1.8 GHz | Quad-core 2.5 GHz or higher |
| RAM | 2 GB | 4 GB or more |
| Storage | 500 MB free space | 1 GB free space |
| Internet | Optional (for fonts) | Broadband (for downloading libraries) |

---

## 5. Libraries and Technologies

### Machine Learning Stack
```
scikit-learn
  ├── CountVectorizer      → converts raw email text into word-count vectors
  ├── MultinomialNB        → Naive Bayes classifier for text classification
  ├── train_test_split     → splits dataset into training and testing sets
  └── metrics              → accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report
```

### Web Stack
```
Flask
  ├── render_template      → renders the HTML page
  ├── request              → receives JSON data from the browser
  └── jsonify              → sends JSON responses back to the browser
```

### Data Stack
```
Pandas
  └── read_csv             → loads the email dataset from a CSV file
```

### Serialisation
```
Joblib
  ├── dump                 → saves the trained pipeline to model.pkl
  └── load                 → loads the saved model at app startup
```

---

## 6. Dataset Requirements

- File format: CSV (`.csv`)
- Required columns: `label` (spam / ham) and `message` (email text)
- Minimum rows: 100 (500+ recommended for a reliable model)
- Balance: Both spam and ham classes should be represented
- Compatible alternative: UCI SMS Spam Collection dataset (5,574 messages)

---

## 7. Project File Structure

```
email-spam-detector/
├── app.py                      ← Flask web application (main entry point)
├── train_model.py              ← ML training script
├── model.pkl                   ← Saved trained model (generated after training)
├── requirements.txt            ← Python library dependencies
├── dataset/
│   ├── emails.csv              ← Training dataset (CSV format)
│   └── generate_dataset.py     ← Script to generate a sample dataset
├── templates/
│   └── index.html              ← HTML user interface
├── static/
│   ├── css/
│   │   └── style.css           ← Application styles
│   └── js/
│       └── main.js             ← Client-side JavaScript
└── docs/
    ├── 01_problem_analysis.md
    ├── 02_requirements.md
    ├── 03_ui_design.md
    ├── 04_code_explanation.md
    ├── 05_testing_plan.md
    └── 06_debugging_improvements.md
```
