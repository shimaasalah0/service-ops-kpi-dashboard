import pandas as pd

# Load raw data
df = pd.read_csv('data/sample_tickets.csv')

# ── 1. Handle nulls ──────────────────────────────────────────
df['closed_date'] = df['closed_date'].fillna('Not Closed')
df['downtime_hours'] = df['downtime_hours'].fillna(0)

# ── 2. Format dates ──────────────────────────────────────────
df['opened_date'] = pd.to_datetime(df['opened_date'], errors='coerce')
df['closed_date'] = pd.to_datetime(df['closed_date'], errors='coerce')

# ── 3. Standardise text fields ───────────────────────────────
df['region'] = df['region'].str.strip().str.title()
df['category'] = df['category'].str.strip().str.title()
df['status'] = df['status'].str.strip().str.title()
df['billing_status'] = df['billing_status'].str.strip().str.title()

# ── 4. Calculate days to close ───────────────────────────────
df['days_to_close'] = (df['closed_date'] - df['opened_date']).dt.days

# ── 5. Flag tickets closed within 7 days ─────────────────────
df['closed_within_7_days'] = df['days_to_close'].apply(
    lambda x: 'Yes' if pd.notna(x) and x <= 7 else 'No'
)

# ── 6. Export cleaned file ───────────────────────────────────
df.to_csv('data/cleaned_tickets.csv', index=False)

print("✅ Data cleaning complete. File saved to data/cleaned_tickets.csv")
print(df.head())
