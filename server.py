import asyncio
import json
import os
from mcp.server.fastmcp import FastMCP
import youtube_client

# Initialize MCP server
mcp = FastMCP("youtube-studio")

@mcp.tool()
def check_auth_status() -> str:
    """Check YouTube OAuth authentication status and return channel info."""
    try:
        service = youtube_client.get_youtube_service()
        res = service.channels().list(mine=True, part="snippet").execute()
        if res.get("items"):
            title = res["items"][0]["snippet"]["title"]
            return f"Authenticated successfully as channel: '{title}'"
        return "Authenticated, but no channel found."
    except Exception as e:
        return f"Authentication failed or token missing: {str(e)}"

@mcp.tool()
def list_videos(max_results: int = 50, page_token: str = None) -> str:
    """List videos from your authenticated YouTube channel."""
    try:
        data = youtube_client.list_channel_videos(max_results=max_results, page_token=page_token)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error listing videos: {str(e)}"

@mcp.tool()
def update_video(
    video_id: str,
    title: str = None,
    description: str = None,
    tags: list[str] = None,
    category_id: str = None,
    privacy_status: str = None
) -> str:
    """Update metadata (title, description, tags, category_id, privacy_status) for a specific YouTube video."""
    try:
        res = youtube_client.update_video_metadata(
            video_id=video_id,
            title=title,
            description=description,
            tags=tags,
            category_id=category_id,
            privacy_status=privacy_status
        )
        return json.dumps(res, indent=2)
    except Exception as e:
        return f"Error updating video: {str(e)}"

@mcp.tool()
def set_thumbnail(video_id: str, image_file_path: str) -> str:
    """Upload and set a custom thumbnail for a video."""
    try:
        res = youtube_client.update_video_thumbnail(video_id, image_file_path)
        return json.dumps(res, indent=2)
    except Exception as e:
        return f"Error uploading thumbnail: {str(e)}"

@mcp.tool()
def append_link_to_all_descriptions(
    link_to_append: str,
    custom_prefix: str = "\n\nJoin our community:\n",
    dry_run: bool = True
) -> str:
    """
    Appends a link (e.g. Skool community URL) to all channel video descriptions if not already present.
    Set dry_run=False to actually perform the update.
    """
    try:
        youtube = youtube_client.get_youtube_service()
        # Fetch uploads playlist
        channels = youtube.channels().list(mine=True, part="contentDetails").execute()
        uploads_id = channels["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        updated_videos = []
        skipped_videos = []
        page_token = None

        while True:
            pl_req = youtube.playlistItems().list(
                playlistId=uploads_id,
                part="snippet,contentDetails",
                maxResults=50,
                pageToken=page_token
            )
            pl_res = pl_req.execute()
            video_ids = [item["contentDetails"]["videoId"] for item in pl_res.get("items", [])]

            if not video_ids:
                break

            v_res = youtube.videos().list(id=",".join(video_ids), part="snippet").execute()
            for v in v_res.get("items", []):
                vid = v["id"]
                title = v["snippet"]["title"]
                desc = v["snippet"].get("description", "")

                if link_to_append in desc:
                    skipped_videos.append({"id": vid, "title": title, "reason": "Link already present"})
                else:
                    new_desc = desc + custom_prefix + link_to_append
                    if not dry_run:
                        v["snippet"]["description"] = new_desc
                        youtube.videos().update(part="snippet", body={"id": vid, "snippet": v["snippet"]}).execute()
                    updated_videos.append({"id": vid, "title": title, "status": "Updated" if not dry_run else "Pending (Dry Run)"})

            page_token = pl_res.get("nextPageToken")
            if not page_token:
                break

@mcp.tool()
def sync_pinned_comments(
    comment_text: str = "🚀 Join our AI Architect & Builder Community on Skool: https://www.skool.com/delivery-pilot-8938",
    limit: int = None,
    dry_run: bool = True
) -> str:
    """
    Creates or updates featured/pinned promo comments across channel videos promoting Skool.
    Set dry_run=False to execute live.
    """
    try:
        channel = youtube_client.get_channel_info()
        youtube = youtube_client.get_youtube_service()
        if not channel:
            return "Failed: channel info not found."

        uploads_id = channel["uploads_id"]
        page_token = None
        results = []
        count = 0

        while True:
            pl_req = youtube.playlistItems().list(
                playlistId=uploads_id,
                part="snippet,contentDetails",
                maxResults=min(50, limit) if limit else 50,
                pageToken=page_token
            )
            pl_res = pl_req.execute()
            items = pl_res.get("items", [])
            if not items:
                break

            for item in items:
                if limit and count >= limit:
                    break
                vid = item["contentDetails"]["videoId"]
                title = item["snippet"]["title"]

                comments = youtube_client.list_video_comments(vid, max_results=20)
                owner_comment = None
                for c in comments:
                    top_snippet = c.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                    if top_snippet.get("authorChannelId", {}).get("value") == channel["id"]:
                        owner_comment = {"id": c.get("snippet", {}).get("topLevelComment", {}).get("id"), "text": top_snippet.get("textOriginal", "")}
                        break

                if owner_comment:
                    if owner_comment["text"].strip() == comment_text.strip():
                        status = "already_matching"
                    else:
                        status = "updated" if not dry_run else "would_update"
                        if not dry_run:
                            youtube.comments().update(part="snippet", body={"id": owner_comment["id"], "snippet": {"textOriginal": comment_text}}).execute()
                else:
                    status = "created" if not dry_run else "would_create"
                    if not dry_run:
                        youtube.commentThreads().insert(part="snippet", body={"snippet": {"videoId": vid, "topLevelComment": {"snippet": {"textOriginal": comment_text}}}}).execute()

                results.append({"video_id": vid, "title": title, "status": status})
                count += 1

            if limit and count >= limit:
                break
            page_token = pl_res.get("nextPageToken")
            if not page_token:
                break

        return json.dumps({"dry_run": dry_run, "total": len(results), "results": results}, indent=2)
    except Exception as e:
        return f"Error syncing pinned comments: {str(e)}"


@mcp.tool()
def update_first_lines_skool_cta(
    cta_line: str = "🚀 Join our AI Architect & Builder Community: https://www.skool.com/delivery-pilot-8938",
    limit: int = None,
    dry_run: bool = True
) -> str:
    """
    Updates the top 2 lines of video descriptions to feature the Skool community call-to-action above the fold.
    Set dry_run=False to apply live.
    """
    try:
        from update_first_lines_skool import format_description_with_cta
        channel = youtube_client.get_channel_info()
        youtube = youtube_client.get_youtube_service()
        if not channel:
            return "Failed: channel info not found."

        uploads_id = channel["uploads_id"]
        page_token = None
        results = []
        count = 0

        while True:
            pl_req = youtube.playlistItems().list(
                playlistId=uploads_id,
                part="snippet,contentDetails",
                maxResults=min(50, limit) if limit else 50,
                pageToken=page_token
            )
            pl_res = pl_req.execute()
            items = pl_res.get("items", [])
            if not items:
                break

            video_ids = [it["contentDetails"]["videoId"] for it in items]
            v_res = youtube.videos().list(id=",".join(video_ids), part="snippet").execute()

            for v in v_res.get("items", []):
                if limit and count >= limit:
                    break
                vid = v["id"]
                title = v["snippet"]["title"]
                desc = v["snippet"].get("description", "")
                new_desc = format_description_with_cta(desc, cta_line)

                if new_desc == desc:
                    status = "already_matching"
                else:
                    status = "updated" if not dry_run else "would_update"
                    if not dry_run:
                        v["snippet"]["description"] = new_desc
                        youtube.videos().update(part="snippet", body={"id": vid, "snippet": v["snippet"]}).execute()

                results.append({"video_id": vid, "title": title, "status": status})
                count += 1

            if limit and count >= limit:
                break
            page_token = pl_res.get("nextPageToken")
            if not page_token:
                break

        return json.dumps({"dry_run": dry_run, "total": len(results), "results": results}, indent=2)
    except Exception as e:
        return f"Error updating first lines CTA: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")

