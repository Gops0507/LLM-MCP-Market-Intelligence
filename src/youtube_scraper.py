from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)

# YT video IDs
video_ids = [
    "xf2DPY3vGto",  
    "F-rpaK0mFlc",
    "lAAApdiF7hQ",
    "bfloSehwRng",
    "KLWdtl5S51g",
    "jZTE5ouxZXQ"
]

comments_data = []

def get_comments(video_id, max_total=120):
    count = 0
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=120
    )
    while request and count < max_total:
        response = request.execute()
        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments_data.append({
                "source": "YouTube",
                "video_id": video_id,
                "comment_text": snippet["textDisplay"],
                "likes": snippet["likeCount"],
                "publishedAt": snippet["publishedAt"]
            })
            count += 1
            if count >= max_total:
                break
        request = youtube.commentThreads().list_next(request, response)

for vid in video_ids:
    print(f"📺 Fetching comments for video: {vid}")
    get_comments(vid, max_total=100)

# Save to CSV
os.makedirs("data/raw", exist_ok=True)
df = pd.DataFrame(comments_data)
df.to_csv("data/raw/youtube_comments.csv", index=False)
print(f"✅ Saved {len(df)} comments to data/raw/youtube_comments.csv")
