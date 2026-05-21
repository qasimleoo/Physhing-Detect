import pandas as pd

print("=" * 50)
print("DATASET CHECK")
print("=" * 50)

# ==========================================
# URL DATASET CHECK
# ==========================================
print("\n[1] URL Dataset Check:")
print("-" * 30)

try:
    df_url = pd.read_csv('dataset_phishing.csv')
    print(f"Total Rows: {len(df_url)}")
    print(f"Total Columns: {len(df_url.columns)}")
    print(f"\nColumn Names:")
    for col in df_url.columns:
        print(f"  - {col}")
    print(f"\nFirst 3 Rows:")
    print(df_url.head(3))
    print(f"\nLabel Column Values:")
    print(df_url.iloc[:, -1].value_counts())

except Exception as e:
    print(f"Error: {e}")

# ==========================================
# EMAIL DATASET CHECK
# ==========================================
print("\n[2] Email Dataset Check:")
print("-" * 30)

try:
    df_email = pd.read_csv('spam.csv',
        encoding='latin-1')
    print(f"Total Rows: {len(df_email)}")
    print(f"Total Columns: {len(df_email.columns)}")
    print(f"\nColumn Names:")
    for col in df_email.columns:
        print(f"  - {col}")
    print(f"\nFirst 3 Rows:")
    print(df_email.head(3))
    print(f"\nLabel Column Values:")
    print(df_email.iloc[:, 0].value_counts())

except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("CHECK COMPLETE!")
print("=" * 50)