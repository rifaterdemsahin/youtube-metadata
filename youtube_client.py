import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required for managing videos and channel content
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.upload"
]

CREDENTIALS_FILE = os.environ.get("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")
TOKEN_FILE = os.environ.get("YOUTUBE_TOKEN_FILE", "token.json")


def get_youtube_service():
    """Authenticates the user and returns the YouTube Data API service client."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"Warning loading token file: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"OAuth client configuration file '{CREDENTIALS_FILE}' not found. "
                    "Please download it from Google Cloud Console as Desktop App credentials and save as client_secret.json."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def list_channel_videos(max_results=50, page_token=None):
    """List videos uploaded by the authenticated channel."""
    youtube = get_youtube_service()

    # Step 1: Get user's uploads playlist ID
    channels_response = youtube.channels().list(
        mine=True,
        part="contentDetails,snippet"
    ).execute()

    if not channels_response.get("items"):
        return {"error": "No channel found for authenticated user", "videos": []}

    channel_info = channels_response["items"][0]
    uploads_playlist_id = channel_info["contentDetails"]["relatedPlaylists"]["uploads"]

    # Step 2: Fetch playlist items
    playlist_req = youtube.playlistItems().list(
        playlistId=uploads_playlist_id,
        part="snippet,contentDetails",
        maxResults=min(max_results, 50),
        pageToken=page_token
    )
    playlist_response = playlist_req.execute()

    video_ids = [item["contentDetails"]["videoId"] for item in playlist_response.get("items", [])]
    if not video_ids:
        return {
            "channel_title": channel_info["snippet"]["title"],
            "videos": [],
            "next_page_token": playlist_response.get("nextPageToken")
        }

    # Step 3: Get detailed video snippet and status
    videos_response = youtube.videos().list(
        id=",".join(video_ids),
        part="snippet,status,statistics"
    ).execute()

    videos = []
    for item in videos_response.get("items", []):
        snippet = item["snippet"]
        status = item.get("status", {})
        stats = item.get("statistics", {})
        videos.append({
            "id": item["id"],
            "title": snippet.get("title"),
            "description": snippet.get("description"),
            "tags": snippet.get("tags", []),
            "category_id": snippet.get("categoryId"),
            "privacy_status": status.get("privacyStatus"),
            "published_at": snippet.get("publishedAt"),
            "view_count": stats.get("viewCount", "0"),
            "like_count": stats.get("likeCount", "0"),
            "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url")
        })

    return {
        "channel_title": channel_info["snippet"]["title"],
        "videos": videos,
        "next_page_token": playlist_response.get("nextPageToken")
    }


def update_video_metadata(video_id, title=None, description=None, tags=None, category_id=None, privacy_status=None):
    """Updates video title, description, tags, category_id, or privacyStatus."""
    youtube = get_youtube_service()

    # Read existing metadata first
    video_response = youtube.videos().list(
        id=video_id,
        part="snippet,status"
    ).execute()

    if not video_response.get("items"):
        return {"error": f"Video with ID '{video_id}' not found."}

    existing_video = video_response["items"][0]
    snippet = existing_video["snippet"]
    status = existing_video.get("status", {})

    if title is not None:
        snippet["title"] = title
    if description is not None:
        snippet["description"] = description
    if tags is not None:
        snippet["tags"] = tags
    if category_id is not None:
        snippet["categoryId"] = category_id
    if privacy_status is not None:
        status["privacyStatus"] = privacy_status

    update_body = {
        "id": video_id,
        "snippet": snippet
    }
    part_param = "snippet"
    if privacy_status is not None:
        update_body["status"] = status
        part_param = "snippet,status"

    updated = youtube.videos().update(
        part=part_param,
        body=update_body
    ).execute()

    return {
        "success": True,
        "id": updated["id"],
        "title": updated["snippet"]["title"],
        "description": updated["snippet"]["description"],
        "privacy_status": updated.get("status", {}).get("privacyStatus")
    }


def update_video_thumbnail(video_id, image_file_path):
    """Uploads a custom thumbnail image for a video."""
    if not os.path.exists(image_file_path):
        return {"error": f"Image file '{image_file_path}' does not exist."}

    youtube = get_youtube_service()
    media = MediaFileUpload(image_file_path, mimetype="image/jpeg", resumable=True)

    thumb_response = youtube.thumbnails().set(
        videoId=video_id,
        media_body=media
    ).execute()

    return {
        "success": True,
        "video_id": video_id,
        "response": thumb_response
    }


def get_channel_info():
    """Returns the authenticated channel's details."""
    youtube = get_youtube_service()
    res = youtube.channels().list(mine=True, part="snippet,contentDetails").execute()
    if not res.get("items"):
        return None
    item = res["items"][0]
    return {
        "id": item["id"],
        "title": item["snippet"]["title"],
        "custom_url": item["snippet"].get("customUrl", ""),
        "uploads_id": item["contentDetails"]["relatedPlaylists"]["uploads"]
    }


def list_video_comments(video_id, max_results=50):
    """Fetches top-level comments for a given video."""
    youtube = get_youtube_service()
    try:
        req = youtube.commentThreads().list(
            videoId=video_id,
            part="snippet",
            maxResults=min(max_results, 100)
        )
        res = req.execute()
        return res.get("items", [])
    except Exception as e:
        print(f"Error fetching comments for video {video_id}: {e}")
        return []


def create_or_update_video_comment(video_id, comment_text, match_keyword="skool.com"):
    """
    Creates a new top-level comment or updates an existing comment authored by the channel.
    Matches existing comments by author channel ID and optional keyword.
    """
    youtube = get_youtube_service()
    channel = get_channel_info()
    channel_id = channel["id"] if channel else None

    existing_comments = list_video_comments(video_id)
    target_comment_id = None

    for item in existing_comments:
        top_snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
        author_channel = top_snippet.get("authorChannelId", {}).get("value")
        text = top_snippet.get("textOriginal", "")

        # Check if authored by channel owner and matches keyword (or is any comment by owner if keyword matches)
        if author_channel == channel_id and (match_keyword in text.lower() or "skool" in text.lower()):
            target_comment_id = item.get("snippet", {}).get("topLevelComment", {}).get("id")
            break

    if target_comment_id:
        # Update existing comment
        updated = youtube.comments().update(
            part="snippet",
            body={
                "id": target_comment_id,
                "snippet": {
                    "textOriginal": comment_text
                }
            }
        ).execute()
        return {
            "action": "updated",
            "comment_id": target_comment_id,
            "video_id": video_id,
            "text": comment_text
        }
    else:
        # Create new top-level comment
        created = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        ).execute()
        new_id = created.get("id")
        return {
            "action": "created",
            "comment_id": new_id,
            "video_id": video_id,
            "text": comment_text
        }

