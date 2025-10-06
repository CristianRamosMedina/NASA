"""
Script 1: Download Kepler Data
Downloads the Kepler cumulative dataset from NASA Exoplanet Archive
"""
import requests
import pandas as pd

print("=" * 80)
print("DOWNLOADING KEPLER CUMULATIVE DATASET")
print("=" * 80)

# NASA Exoplanet Archive API
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+*+from+cumulative&format=csv"

print(f"\nFetching data from NASA Exoplanet Archive...")
print(f"URL: {url}\n")

response = requests.get(url)
response.raise_for_status()

# Save raw data
with open('kepler/kepler_raw.csv', 'wb') as f:
    f.write(response.content)

# Load and inspect
df = pd.read_csv('kepler/kepler_raw.csv')

print(f"Downloaded successfully!")
print(f"Dataset shape: {df.shape}")
print(f"   Rows: {df.shape[0]:,}")
print(f"   Columns: {df.shape[1]:,}")

print(f"\nSample columns:")
for i, col in enumerate(df.columns[:20], 1):
    print(f"   {i:2d}. {col}")
print(f"   ... and {len(df.columns) - 20} more columns")

print(f"\nTarget variable distribution (koi_disposition):")
print(df['koi_disposition'].value_counts())

print(f"\nSaved as: kepler/kepler_raw.csv")
print("=" * 80)
