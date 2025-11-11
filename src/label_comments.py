import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv
from tqdm import tqdm

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the cleaned dataset
df = pd.read_csv("data/processed/cleaned_comments.csv")

# Initialize the model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Define function to label one comment
def classify_comment(comment):
    prompt = f"Label this comment about iPhone vs Samsung as [Pro-iPhone], [Pro-Samsung], or [Neutral]. Comment: {comment}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Error processing comment: {e}")
        return "Error"

# Apply the function with a progress bar
df["label"] = [classify_comment(c) for c in tqdm(df["comment_text"], desc="Labeling comments")]

# Save the results
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/labeled_comments.csv", index=False)
print("✅ Labeled comments saved → data/processed/labeled_comments.csv")
