from youtube import search_videos, VideoType
from gemini import get_response, to_markdown, summarize_video
import typer

app = typer.Typer()


@app.command()
def chat():
    videos: list[VideoType] = []
    try:
        while True:
            message: str = typer.prompt("You: ")
            response: str = ""

            if "search" in message:
                search_query = message.split("search")[1].strip()
                videos = search_videos(search_query)
                reply = "I found the following videos: \n\n"

                for video in videos:
                    reply += f"{videos.index(video) + 1}: {video['title']}\n"

                response = reply

            elif "summarize" in message:
                reply = "Here is a summary of the video:\n"
                reply += summarize_video(videos, message)

                response = to_markdown(reply)

            else:
                response = get_response(message)

            if response:
                typer.echo(response)

            typer.echo(
                "I am sorry, I could not understand your query. Please try again."
            )

    except Exception as e:
        typer.echo(f"An error occurred: {e}")


if __name__ == "__main__":
    app()
