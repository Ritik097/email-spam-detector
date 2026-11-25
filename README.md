# 📧 Email Spam Detector

**AI-Based Email Spam Detection Web Application**  
Semester 3 Project | Computer Science – Artificial Intelligence & Machine Learning

---

## Overview

This application uses a **Multinomial Naive Bayes** machine learning model to
classify email messages as **Spam** or **Not Spam**. Users enter email text
through a clean web interface and receive an instant prediction with a
confidence score.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| Web Framework | Flask |
| ML Library | Scikit-learn |
| Text Vectorisation | CountVectorizer |
| Classifier | Multinomial Naive Bayes |
| Data Handling | Pandas |
| Model Persistence | Joblib |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

---

## Project Structure

```
email-spam-detector/
├── app.py                      ← Flask web application
├── train_model.py              ← ML training script
├── model.pkl                   ← Saved model (created after training)
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
├── dataset/
│   ├── emails.csv              ← Training dataset
│   └── generate_dataset.py     ← Sample dataset generator
├── templates/
│   └── index.html              ← HTML user interface
├── static/
│   ├── css/style.css           ← Styles
│   └── js/main.js              ← Client-side logic
└── docs/
    ├── 01_problem_analysis.md
    ├── 02_requirements.md
    ├── 03_ui_design.md
    ├── 04_code_explanation.md
    ├── 05_testing_plan.md
    └── 06_debugging_improvements.md
```

---

## Quick Start (macOS)

Open the VS Code integrated terminal (`` Ctrl+` ``) and run these commands:

```bash
# 1. Navigate to the project
cd "/Users/ritikkushwaha/ipe project/email-spam-detector"

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the sample dataset
python dataset/generate_dataset.py

# 5. Train the ML model
python train_model.py

# 6. Start the web application
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## Using a Real Dataset (Recommended)

For higher accuracy (~98%), download the SMS Spam Collection dataset:

1. Visit: https://archive.ics.uci.edu/ml/datasets/sms+spam+collection
2. Download and extract the file.
3. Rename it to `emails.csv` and place it in the `dataset/` folder.
4. Re-run `python train_model.py`.

The column names `v1` and `v2` are automatically detected and renamed.

---

## Features

- 🔍 Instant spam prediction with confidence score
- 🎨 Colour-coded results (red for spam, green for legitimate)
- 📋 Sample emails for quick testing
- ⚠️ Empty and short input validation
- 📊 Model evaluation: accuracy, precision, recall, F1-score, confusion matrix
- 📱 Responsive design for all screen sizes

---

## Documentation

All academic documentation is in the `docs/` folder:

| File | Content |
|---|---|
| `01_problem_analysis.md` | Problem statement, objectives, ML approach |
| `02_requirements.md` | Functional, non-functional, software, hardware requirements |
| `03_ui_design.md` | Layout, component descriptions, colour scheme |
| `04_code_explanation.md` | Step-by-step code explanation + setup instructions |
| `05_testing_plan.md` | 20 test cases with expected results (ready to fill in) |
| `06_debugging_improvements.md` | Common errors, fixes, and optional improvements |

---

*Academic project — built for educational purposes.*
