import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import joblib

print("=" * 50)
print("URL PHISHING MODEL TRAINING")
print("=" * 50)

# ==========================================
# STEP 1: DATASET LOAD
# ==========================================
print("\n[1] Loading Dataset...")

df = pd.read_csv('dataset_phishing.csv')
print(f"Total Rows: {len(df)}")

# ==========================================
# STEP 2: FEATURES SELECT KAREIN
# ==========================================
print("\n[2] Selecting Features...")

# Best features select karein
selected_features = [
    'length_url',
    'length_hostname',
    'ip',
    'nb_dots',
    'nb_hyphens',
    'nb_at',
    'nb_qm',
    'nb_and',
    'nb_slash',
    'nb_www',
    'nb_com',
    'nb_dslash',
    'http_in_path',
    'https_token',
    'ratio_digits_url',
    'ratio_digits_host',
    'punycode',
    'port',
    'tld_in_path',
    'abnormal_subdomain',
    'nb_subdomains',
    'prefix_suffix',
    'shortening_service',
    'nb_redirection',
    'phish_hints',
    'domain_in_brand',
    'suspecious_tld',
    'login_form',
    'external_favicon',
    'iframe',
    'popup_window',
    'domain_in_title',
    'domain_age',
    'web_traffic',
    'page_rank'
]

# Features jo dataset main hain
available_features = [
    f for f in selected_features
    if f in df.columns
]

print(f"Features Selected: {len(available_features)}")

X = df[available_features]
y = df['status']

# Label encode karein
# legitimate=0, phishing=1
y = y.map({
    'legitimate': 0,
    'phishing': 1
})

print(f"X Shape: {X.shape}")
print(f"y Shape: {y.shape}")

# ==========================================
# STEP 3: MISSING VALUES FIX
# ==========================================
print("\n[3] Handling Missing Values...")

X = X.fillna(0)
print("Missing values filled with 0")

# ==========================================
# STEP 4: TRAIN TEST SPLIT
# ==========================================
print("\n[4] Splitting Data...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print(f"Training: {len(X_train)} rows")
print(f"Testing: {len(X_test)} rows")

# ==========================================
# STEP 5: MODEL TRAIN
# ==========================================
print("\n[5] Training Random Forest Model...")
print("Please wait... (1-2 minutes)")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=15,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("Training Complete!")

# ==========================================
# STEP 6: MODEL TEST
# ==========================================
print("\n[6] Testing Model...")

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*40}")
print(f"Model Accuracy: {accuracy:.2%}")
print(f"{'='*40}")

print("\nDetailed Report:")
print(classification_report(
    y_test, y_pred,
    target_names=['Legitimate', 'Phishing']
))

# ==========================================
# STEP 7: MODEL SAVE
# ==========================================
print("\n[7] Saving Model...")

joblib.dump(model, 'url_phishing_model.pkl')
joblib.dump(available_features, 'url_feature_names.pkl')

print("Model saved: url_phishing_model.pkl")
print("Features saved: url_feature_names.pkl")

print("\n" + "=" * 50)
print("URL MODEL TRAINING COMPLETE!")
print("=" * 50)
