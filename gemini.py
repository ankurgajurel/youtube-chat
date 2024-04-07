import textwrap
import google.generativeai as genai
from config import config_environemnt
from youtube import search_videos, get_video_transcript
import requests
import re

from youtube import VideoType


# consuming api directly
def generate_content(prompt: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json",
    }
    params = {"key": config_environemnt["GEMINI_API_KEY"]}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": {
                    "text": """
                    Query Interpretation: You are an AI assistant tasked with interpreting user queries through advanced natural language processing. Analyze the intent, context, and specific details of each query to provide accurate and relevant responses.

                    YouTube Search and Summarization: You search YouTube for videos matching the user's queries. Extract keywords, apply filters for relevance, and use YouTube's API to retrieve video suggestions. Summarize the content of selected videos by accessing or generating transcriptions, highlighting key points, and distilling essential information into concise summaries.

                    Detailed Responsibilities:

                    Understand User Queries:

                    Decompose queries into actionable insights.
                    Identify the type of response needed: direct answer, video suggestion, or summary.
                    Execute Searches:

                    Use extracted keywords from the query for YouTube searches.
                    Apply advanced search techniques to filter results by relevance, popularity, and recency.
                    Select Relevant Videos:

                    Analyze video metadata, viewer engagement, and relevance to the query.
                    Choose videos that best match the query’s intent for summarization.
                    Summarize Video Content:

                    Access or generate video transcriptions.
                    Extract key themes, arguments, and data points from the transcription.
                    Produce a summary that encapsulates the video's essence in a brief format.
                    Adapt and Learn:

                    Adapt responses based on user feedback and interaction history.
                    Refine understanding of user preferences for more personalized assistance over time.
                    Provide Multi-Lingual Support:

                    Interpret and respond to queries in multiple languages, expanding accessibility and user base.
                    Ensure Accessibility:

                    Incorporate voice-to-text and text-to-voice functionalities to cater to users with diverse needs.
                    Operational Guidelines:

                    Maintain privacy and confidentiality of user queries and interactions.
                    Update search algorithms and summarization techniques periodically to incorporate the latest advancements in AI and machine learning.
                    Engage in continuous learning from user interactions, feedback, and external sources to enhance accuracy and relevance of responses and suggestions.
                    End-User Interaction:

                    Offer clear, concise, and informative responses and summaries.
                    Provide instructions or guidance on how users can access or view suggested videos.
                    Encourage user feedback to facilitate adaptive learning and personalization of the service.
                    By adhering to these directives, you ensure an efficient, effective, and user-centric service, helping users to quickly find answers to their queries and summaries of YouTube video content that matches their interests and needs.
                """
                },
            },
            {"role": "model", "parts": {"text": "ok"}},
            {
                "role": "user",
                "parts": {"text": prompt},
            },
        ],
        "tools": [
            {
                "function_declarations": [
                    {
                        "name": "search_videos",
                        "description": "Search for videos on YouTube",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query",
                                },
                                "reply": {
                                    "type": "string",
                                    "description": "The response to the user",
                                },
                            },
                            "required": ["query, reply"],
                        },
                    }
                ]
            }
        ],
    }

    response = requests.post(url, headers=headers, params=params, json=data)

    return response.json()


def to_markdown(text: str) -> str:
    text = text.replace("•", "  *")
    return textwrap.indent(text, "> ", predicate=lambda _: True)


# tried to implement the filter_chat function for generalizing the keyword related queries
def filter_chat(prompt: str) -> None:
    if "search" in prompt:
        search_query = prompt.split("search")[1].strip()
        videos = search_videos(search_query)
        reply = "I found the following videos: \n\n"

        for video in videos:
            reply += f"{videos.index(video) + 1}: {video['title']}\n"

    elif "summarize" in prompt:
        reply = "Here is a summary of the video:\n"
        reply += summarize_video(videos, prompt)


# main get the response from the gemini api
def get_response(prompt: str) -> str:
    GOOGLE_API_KEY = config_environemnt["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel(
        "gemini-pro",
        tools=[],
    )

    response = model.generate_content(prompt)

    reply: str = response._result.candidates[0].content.parts[0].text

    return reply


# seperate keywords from the query
def filter_keywords(query: str) -> str:
    keywords = get_response("Filter keywords from" + query)
    return keywords


# summarize any text
def summarize_text(video: VideoType) -> str:
    # print(video["transcript"])
    response: str = get_response("Summarize " + str(video))
    return response


# summarize a video based on the prompt
def summarize_video(videos: list[VideoType], prompt: str) -> str:
    index: int = 0
    try:
        response: str = get_response(
            f"Which video is the prompt referring to from this list? give me the index of the video. start the index from 0. if you're . \n\n the list of videos is: {videos} \n\n The prompt is: {prompt}"
        )
        if response:
            for elem in response.split():
                if elem.isdigit():
                    index = int(elem)
                    break

        if not response:
            for elem in prompt.split():
                if elem.isdigit():
                    index = int(elem)
                    break
    except:
        pass

    if index > len(videos):
        return "I don't have that video in my list. Please try again."

    video: VideoType = videos[index]
    return summarize_text(video)
