"""
train_model.py
--------------
Trains the spam detection model and saves it as 'model.pkl'.

Steps:
  1. Load the dataset from dataset/emails.csv
  2. Preprocess email text (lowercase, strip whitespace)
  3. Split into 70% train / 30% test
  4. Build a pipeline: CountVectorizer → Multinomial Naive Bayes
  5. Train and evaluate the model
  6. Save the trained pipeline with joblib

Run this script once before starting the web app:
    python train_model.py
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# ── 1. Load Dataset ──────────────────────────────────────────────────────────
DATASET_PATH = os.path.join("dataset", "emails.csv")

if not os.path.exists(DATASET_PATH):
    print("Dataset not found. Generating it now …")
    import subprocess
    subprocess.run(["python", "dataset/generate_dataset.py"], check=True)

df = pd.read_csv(DATASET_PATH)
print(f"Dataset loaded: {len(df)} rows, columns: {list(df.columns)}")

# ── 2. Basic Validation ───────────────────────────────────────────────────────
# Accept common column name variants
if "message" not in df.columns or "label" not in df.columns:
    # Try SMS Spam Collection format: 'v1' and 'v2'
    if "v1" in df.columns and "v2" in df.columns:
        df.rename(columns={"v1": "label", "v2": "message"}, inplace=True)
    else:
        raise ValueError(
            "Dataset must have 'label' and 'message' columns "
            "(or 'v1'/'v2' for the SMS Spam Collection format)."
        )

# Drop rows where message or label is missing
df = df.dropna(subset=["message", "label"])
print(f"After dropping nulls: {len(df)} rows")
print(f"Label distribution:\n{df['label'].value_counts()}\n")

# ── 3. Preprocess ─────────────────────────────────────────────────────────────
df["message"] = df["message"].str.lower().str.strip()

# ── 4. Features and Labels ───────────────────────────────────────────────────
X = df["message"]
y = df["label"]

# ── 5. Train / Test Split (70 / 30) ──────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
print(f"Training samples : {len(X_train)}")
print(f"Testing  samples : {len(X_test)}\n")

# ── 6. Build Pipeline ────────────────────────────────────────────────────────
pipeline = Pipeline(
    [
        ("vectorizer", CountVectorizer(stop_words="english")),
        ("classifier", MultinomialNB()),
    ]
)

# ── 7. Train the Model ───────────────────────────────────────────────────────
pipeline.fit(X_train, y_train)
print("Model training complete.\n")

# ── 8. Evaluate the Model ────────────────────────────────────────────────────
y_pred = pipeline.predict(X_test)

accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label="spam", zero_division=0)
recall    = recall_score(y_test, y_pred, pos_label="spam", zero_division=0)
f1        = f1_score(y_test, y_pred, pos_label="spam", zero_division=0)
cm        = confusion_matrix(y_test, y_pred, labels=["spam", "ham"])
report    = classification_report(y_test, y_pred, zero_division=0)

print("=" * 50)
print("        MODEL EVALUATION RESULTS")
print("=" * 50)
print(f"  Accuracy  : {accuracy  * 100:.2f}%")
print(f"  Precision : {precision * 100:.2f}%")
print(f"  Recall    : {recall    * 100:.2f}%")
print(f"  F1-Score  : {f1        * 100:.2f}%")
print()
print("Confusion Matrix (rows=actual, cols=predicted):")
print("             Spam   Ham")
print(f"  Spam  →  {cm[0][0]:>5}  {cm[0][1]:>5}")
print(f"  Ham   →  {cm[1][0]:>5}  {cm[1][1]:>5}")
print()
print("Classification Report:")
print(report)
print("=" * 50)

# ── 9. Save the Trained Model ─────────────────────────────────────────────────
MODEL_PATH = "model.pkl"
joblib.dump(pipeline, MODEL_PATH)
print(f"\nModel saved to '{MODEL_PATH}'.")
print("You can now run the web app:  python app.py")
