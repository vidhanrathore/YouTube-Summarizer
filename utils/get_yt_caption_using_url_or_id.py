from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

def get_youtube_id(url):
    # Extract video ID from URL
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def get_captions(video_url, lang='en'):
    video_id = get_youtube_id(video_url)
    # print(video_id)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
        # print(transcript)
        text = ""
        for dic in transcript:
            text += dic["text"]
            text += " "
        return text
    except Exception as e:
        return f"Error: {e}"


# Run this block only if executed directly
if __name__ == "__main__":
    yt = "https://www.youtube.com/watch?v=15_pppse4fY"
    result = get_captions(yt)
    print(result)

