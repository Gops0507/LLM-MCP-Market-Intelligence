import praw
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Configuration
query = "iphone or samsung"
subreddits = ["Smartphones", "Android", "iPhone", "photography", "technology"]

comments_data = []
max_total_comments = 600   # ✅ Limit total comments to ~600

# Loop through subreddits
for sub in subreddits:
    print(f"🔍 Searching r/{sub}...")
    for submission in reddit.subreddit(sub).search(query, limit=50):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            if len(comments_data) >= max_total_comments:
                break  # stop if limit reached
            comments_data.append({
                "source": "Reddit",
                "subreddit": sub,
                "post_title": submission.title,
                "comment_text": comment.body,
                "score": comment.score,
                "post_url": submission.url
            })
        if len(comments_data) >= max_total_comments:
            break
    if len(comments_data) >= max_total_comments:
        break

# Convert to DataFrame
df = pd.DataFrame(comments_data)

# Save to CSV
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/reddit_comments.csv", index=False)
print(f"✅ Saved {len(df)} Reddit comments to data/raw/reddit_comments.csv")