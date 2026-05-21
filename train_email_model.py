import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib

print("=" * 50)
print("EMAIL PHISHING MODEL TRAINING")
print("=" * 50)

# ==========================================
# STEP 1: DATASET LOAD
# ==========================================
print("\n[1] Loading Email Dataset...")

df = pd.read_csv('spam.csv', encoding='latin-1')

# Sirf 2 columns chahiye
df = df[['v1', 'v2']]
df.columns = ['label', 'text']

print(f"Total Emails: {len(df)}")
print(f"Spam: {len(df[df['label']=='spam'])}")
print(f"Ham: {len(df[df['label']=='ham'])}")

# ==========================================
# STEP 2: LABELS CONVERT
# ==========================================
print("\n[2] Converting Labels...")

df['label'] = df['label'].map({
    'spam': 1,
    'ham': 0
})

# Missing values remove
df = df.dropna()

X = df['text']
y = df['label']

print(f"Total after cleaning: {len(df)}")

# ==========================================
# STEP 3: TRAIN TEST SPLIT
# ==========================================
print("\n[3] Splitting Data...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print(f"Training: {len(X_train)} emails")
print(f"Testing: {len(X_test)} emails")

# ==========================================
# STEP 4: PIPELINE BANAYEIN
# ==========================================
print("\n[4] Building Pipeline...")

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)
    )),
    ('model', MultinomialNB(alpha=0.1))
])

# ==========================================
# STEP 5: TRAIN
# ==========================================
print("\n[5] Training Model...")

pipeline.fit(X_train, y_train)
print("Training Complete!")

# ==========================================
# STEP 6: TEST
# ==========================================
print("\n[6] Testing Model...")

y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*40}")
print(f"Model Accuracy: {accuracy:.2%}")
print(f"{'='*40}")

print("\nDetailed Report:")
print(classification_report(
    y_test, y_pred,
    target_names=['Safe', 'Phishing']
))

# ==========================================
# STEP 7: SAVE
# ==========================================
print("\n[7] Saving Model...")

joblib.dump(pipeline, 'email_phishing_model.pkl')
print("Model saved: email_phishing_model.pkl")

print("\n" + "=" * 50)
print("EMAIL MODEL TRAINING COMPLETE!")
print("=" * 50)