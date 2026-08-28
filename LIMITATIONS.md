# Limitations

This page documents what this toolset **cannot** automate via the YouTube Data API v3, and what must be completed manually in YouTube Studio.

---

## ❌ End Screens & Info Cards — Not API-Applicable

The YouTube Data API v3 has **no endpoint for creating or editing End Screens or Info Cards**. These features can only be configured manually in YouTube Studio.

**What the scripts actually do:**

- `sync_end_cards.py` reads every video's duration and **generates a blueprint spec** (element type, target video `F8IBooe3bXY`, start time 00:20 before end, 16:9 safe-zone placement) and writes it to `end_cards_report.json`, alongside Studio deep links.
- It **does NOT apply** end screens to your videos. The output is a plan, not a live change.

**What you must do manually:**

1. Open the Studio editor deep link for each video (e.g., `https://studio.youtube.com/video/Frty5ICAdOo/editor`).
2. Navigate to **End screen**.
3. Add a **Video element** pointing to the featured masterclass (`F8IBooe3bXY`).
4. Set the element start time to **00:20 before the video ends** (min 5s / max 20s) and place it inside the **16:9 safe zone**, avoiding native UI overlays.
5. Info Cards (teaser text, custom messages) are likewise Studio-only.

**Why you may not see an end screen after running the scripts:** it was never set live — only documented. Check `end_cards_report.json` for the spec to apply.

---

## ⚠️ Other Known Gaps

| Capability | API Support | Notes |
| --- | --- | --- |
| Titles, descriptions, tags, privacy | ✅ | `videos.update` |
| Thumbnails | ⚠️ | `thumbnails.set` often returns success; **Shorts** may still show an auto 9:16 frame. After upload, download live `maxresdefault` and compare. If it does not match, upload in Studio. |
| Playlist & video listing | ✅ | `playlists`, `playlistItems`, `videos.list` |
| Posting top-level comments | ✅ | `commentThreads.insert` (`sync_pinned_comments.py`) |
| Pinning/featuring a comment | ❌ | Comment is posted via API; the actual **pin** action must be done in Studio |
| End Screens | ❌ | Blueprint only — apply manually in Studio |
| Info Cards | ❌ | Blueprint only — apply manually in Studio |
| End-screen visual promo graphics | ❌ | Burn promo graphics into the video's end-slate track during editing before upload |

---

## 📌 Bottom Line

Anything that involves **End Screens or Info Cards** stops at the blueprint/dry-run stage by design. The API simply cannot perform these operations — always finish the job in YouTube Studio using the deep links generated in the reports.
