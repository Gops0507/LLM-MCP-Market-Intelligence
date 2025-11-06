import praw
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

query = "iPhone 16 vs Samsung S24 camera"
subreddits = ["Smartphones", "Android", "iPhone", "photography", "technology"]

comments_data = []

for sub in subreddits:
    print(f"🔍 Searching r/{sub}...")
    for submission in reddit.subreddit(sub).search(query, limit=50):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments_data.append({
                "source": "Reddit",
                "subreddit": sub,
                "post_title": submission.title,
                "comment_text": comment.body,
                "score": comment.score,
                "post_url": submission.url
            })

df = pd.DataFrame(comments_data)
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/reddit_comments.csv", index=False)
print(f"✅ Saved {len(df)} comments to data/raw/reddit_comments.csv")
