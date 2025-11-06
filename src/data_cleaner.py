import pandas as pd
import re
import os

# Load raw data
reddit_df = pd.read_csv("data/raw/reddit_comments.csv")
youtube_df = pd.read_csv("data/raw/youtube_comments.csv")

# Combine
df = pd.concat([reddit_df, youtube_df], ignore_index=True)

# Basic cleaning
def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+|www\S+", "", text)       # remove URLs
    text = re.sub(r"@\w+", "", text)                 # remove @mentions
    text = re.sub(r"[^A-Za-z0-9.,!?\'\s]", "", text) # remove special chars
    return text.strip()

df["comment_text"] = df["comment_text"].apply(clean_text)
df.dropna(subset=["comment_text"], inplace=True)
df.drop_duplicates(subset=["comment_text"], inplace=True)

# Remove identifiable columns (like author names if they exist)
cols_to_drop = [col for col in df.columns if "author" in col.lower() or "name" in col.lower()]
df.drop(columns=cols_to_drop, inplace=True, errors="ignore")

# Save cleaned combined file
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/cleaned_comments.csv", index=False)
print(f"✅ Cleaned & combined {len(df)} comments → data/processed/cleaned_comments.csv")
