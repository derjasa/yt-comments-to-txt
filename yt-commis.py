from googleapiclient.discovery import build

API_KEY = ''
VIDEO_ID = ''

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_comments(video_id):
    comments = []
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    ).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            ).execute()
        else:
            break

    return comments

comments = get_video_comments(VIDEO_ID)

with open("youtube_comments.txt", "w", encoding="utf-8") as f:
    for comment in comments:
        f.write(comment + "\n")

print(f"{len(comments)} comments downloaded.")
