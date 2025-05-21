import yt_dlp
import os
import re
from transformers import pipeline

def get_youtube_captions(video_url, language='en'):
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [language],
        'subtitlesformat': 'vtt',
        'outtmpl': '%(id)s.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        video_id = info_dict.get("id", None)

    subtitle_file = f"{video_id}.{language}.vtt"
    if os.path.exists(subtitle_file):
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            vtt_data = f.read()
        os.remove(subtitle_file)
        return vtt_data
    else:
        return None

def vtt_to_text(vtt_data):
    lines = vtt_data.split('\n')
    text_lines = []
    for line in lines:
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line) or line.strip() == '' or "-->" in line:
            continue
        text_lines.append(line.strip())
    return ' '.join(text_lines)

def summarize_text(text, max_tokens=512):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # Truncate long text to fit model token limit
    if len(text) > 1000:
        text = text[:1000]
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_youtube_video(video_url, language='en'):
    vtt_data = get_youtube_captions(video_url, language)
    if not vtt_data:
        return "No captions found."

    plain_text = vtt_to_text(vtt_data)
    summary = summarize_text(plain_text)
    return summary

# Example usage:
# video_url = "https://www.youtube.com/watch?v=VIDEO_ID"
# print(summarize_youtube_video(video_url))
