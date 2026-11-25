# Prompt 4 – Code Explanation

## AI-Based Email Spam Detection Web Application

---

## Project Files Overview

| File | Role |
|---|---|
| `dataset/generate_dataset.py` | Creates a sample emails.csv dataset |
| `train_model.py` | Trains the ML model and saves it as model.pkl |
| `app.py` | Flask web server — handles routes and predictions |
| `templates/index.html` | HTML user interface |
| `static/css/style.css` | All visual styling |
| `static/js/main.js` | JavaScript: button actions, API calls, result rendering |

---

## 1. `train_model.py` – Step-by-Step Explanation

### Step 1 – Import Libraries
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
```
- `pandas` reads the CSV file into a table (DataFrame).
- `train_test_split` randomly divides data into training and testing sets.
- `CountVectorizer` converts raw email text into numbers (word frequency counts).
- `MultinomialNB` is the Naive Bayes classifier — it learns from these numbers.
- `Pipeline` chains CountVectorizer and MultinomialNB together into one object.

### Step 2 – Load the Dataset
```python
df = pd.read_csv("dataset/emails.csv")
```
The CSV has two columns:
- `label` → "spam" or "ham"
- `message` → the email text

### Step 3 – Preprocess Text
```python
df["message"] = df["message"].str.lower().str.strip()
```
- `.lower()` converts all text to lowercase so "FREE" and "free" are treated the same.
- `.strip()` removes leading and trailing whitespace.

### Step 4 – Separate Features and Labels
```python
X = df["message"]   # Input: email text
y = df["label"]     # Output: spam or ham
```
`X` is what the model learns from (the email text).
`y` is what the model is trying to predict (spam or ham).

### Step 5 – Train / Test Split
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
```
- `test_size=0.30` → 30% of data is used for testing, 70% for training.
- `random_state=42` → ensures the same split every time (reproducibility).
- `stratify=y` → ensures both spam and ham are proportionally represented in
  both the train and test sets. Without this, the test set might contain mostly
  one class.

### Step 6 – Build the Pipeline
```python
pipeline = Pipeline([
    ("vectorizer", CountVectorizer(stop_words="english")),
    ("classifier", MultinomialNB()),
])
```
A Pipeline is like a production line:
1. **CountVectorizer** receives raw email text and produces a matrix of word counts.
   - `stop_words="english"` removes common words like "the", "is", "and" that
     don't help distinguish spam from ham.
2. **MultinomialNB** receives the word counts and learns which words are
   associated with spam versus ham.

### Step 7 – Train the Model
```python
pipeline.fit(X_train, y_train)
```
The model reads all 70% of training emails and their labels. It learns the
probability of each word appearing in a spam email versus a legitimate email.

### Step 8 – Evaluate the Model
```python
y_pred = pipeline.predict(X_test)
accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label="spam")
recall    = recall_score(y_test, y_pred, pos_label="spam")
f1        = f1_score(y_test, y_pred, pos_label="spam")
cm        = confusion_matrix(y_test, y_pred, labels=["spam", "ham"])
```
Metric explanations:
- **Accuracy** – What percentage of all emails were classified correctly?
- **Precision** – Of all emails predicted as spam, how many actually were spam?
  (Avoids false alarms.)
- **Recall** – Of all actual spam emails, how many did the model catch?
  (Avoids missing spam.)
- **F1-Score** – Harmonic mean of precision and recall. The best single metric
  for imbalanced datasets.
- **Confusion Matrix** – A 2×2 table showing:
  ```
                  Predicted Spam  Predicted Ham
  Actual Spam  →      TP                FN
  Actual Ham   →      FP                TN
  ```
  TP = True Positive, FN = False Negative, FP = False Positive, TN = True Negative.

### Step 9 – Save the Model
```python
joblib.dump(pipeline, "model.pkl")
```
The trained pipeline (both CountVectorizer and MultinomialNB) is saved to a
single file. This avoids re-training every time the web app starts.

---

## 2. `app.py` – Step-by-Step Explanation

### Load the Model at Startup
```python
model = joblib.load("model.pkl")
```
When Flask starts, it loads the trained model into memory once.
All subsequent prediction requests reuse the same in-memory model.

### Route: `GET /`
```python
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
```
When a user visits `http://127.0.0.1:5000`, Flask returns the HTML page.

### Route: `POST /predict`
```python
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    email_text = data["email_text"].strip()
    prediction_label = model.predict([email_text])[0]
    probabilities    = model.predict_proba([email_text])[0]
    ...
    return jsonify({...})
```
1. Receives JSON from the browser: `{ "email_text": "..." }`.
2. Passes the text to the loaded model for prediction.
3. Gets the probability scores for each class.
4. Returns a JSON response with the result, confidence, and message.

---

## 3. `main.js` – Step-by-Step Explanation

### Character Counter
```javascript
emailInput.addEventListener("input", () => {
    charCount.textContent = emailInput.value.length;
});
```
Every time the user types a character, the counter updates.

### predictSpam() Function
1. Gets the text from the textarea.
2. Validates: not empty, at least 3 characters.
3. Shows a loading spinner on the Predict button.
4. Sends a `fetch()` POST request to `/predict` with the email text.
5. Receives JSON back and calls `renderResult()`.

### renderResult() Function
1. Checks whether the label is "spam" or "ham".
2. Dynamically builds the result HTML using template literals.
3. Inserts it into the result card.
4. Animates the confidence bar using `requestAnimationFrame`.

### escHtml() Function
Prevents XSS (Cross-Site Scripting) by escaping `<`, `>`, `&`, `"` characters
before inserting user-controlled text into the DOM.

---

## 4. Installation and Execution (macOS / VS Code)

### Step 1: Open Terminal in VS Code
Press `` Ctrl+` `` (backtick) to open the integrated terminal.

### Step 2: Navigate to the Project Folder
```bash
cd "/Users/ritikkushwaha/ipe project/email-spam-detector"
```

### Step 3: Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Generate the Dataset
```bash
python dataset/generate_dataset.py
```

### Step 6: Train the Model
```bash
python train_model.py
```
You will see the accuracy, precision, recall, F1-score, and confusion matrix
printed in the terminal.

### Step 7: Run the Web Application
```bash
python app.py
```

### Step 8: Open in Browser
Visit: **http://127.0.0.1:5000**

### To Stop the Server
Press `Ctrl + C` in the terminal.

---

## 5. Using a Real Dataset (Optional Upgrade)

You can replace the generated dataset with the **UCI SMS Spam Collection** dataset:

1. Download from: https://archive.ics.uci.edu/ml/datasets/sms+spam+collection
2. The file has columns `v1` (label: spam/ham) and `v2` (message text).
3. `train_model.py` automatically detects and renames these columns.
4. Place the file at `dataset/emails.csv` and re-run `python train_model.py`.
