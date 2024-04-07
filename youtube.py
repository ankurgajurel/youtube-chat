from typing import List, Dict
from googleapiclient.discovery import build
from config import config_environemnt
from youtube_transcript_api import YouTubeTranscriptApi


class VideoType:
    def __init__(self, title: str, description: str, video_id: str, transcript: str):
        self.title = title
        self.description = description
        self.video_id = video_id
        self.transcript = transcript

    def __str__(self):
        return f"Title: {self.title}\nDescription: {self.description}\nTranscript: {self.transcript}"


def search_videos(query: str, max_results: int = 5) -> List[Dict]:
    youtube = build("youtube", "v3", developerKey=config_environemnt["YOUTUBE_API_KEY"])
    request = youtube.search().list(q=query, part="snippet", maxResults=max_results)
    response = request.execute()

    videos: List[VideoType] = []

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video: VideoType = {
                "title": item["snippet"]["title"],
                # "description": item["snippet"]["description"],
                "video_id": item["id"]["videoId"],
                "transcript": get_video_transcript(item["id"]["videoId"]),
            }
            videos.append(video)
    return videos


def get_video_transcript(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # print(transcript)
        if "Could not retrieve a transcript for the video" in transcript:
            return ""

        text = ""

        for item in transcript:
            text += item["text"]

        return text
    except Exception as e:
        return ""
