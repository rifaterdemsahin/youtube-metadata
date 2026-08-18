---
name: sync-pinned-comments-skool
description: >-
  Creates or updates featured and pinned top-level comments on YouTube videos promoting the Skool community.
  Use when the user wants to pin Skool community promo comments, sync comment calls-to-action, or engage video viewers in the comment section.
---

# Skill: YouTube Pinned & Featured Comments Skool Promoter

Automate creating and updating top-level pinned comments on all YouTube videos for `@RifatErdemSahin` to direct viewers to the Skool Community.

## 🎯 Target Skool Community
- **URL**: `https://www.skool.com/delivery-pilot-8938`
- **Channel**: `@RifatErdemSahin`

## 🚀 Execution Commands

### 1. Dry Run (Simulated)
```bash
./venv/bin/python sync_pinned_comments.py --dry-run
```

### 2. Live Apply (Targeting All Videos)
```bash
./venv/bin/python sync_pinned_comments.py --apply
```

### 3. Live Apply (Limited Batch)
```bash
./venv/bin/python sync_pinned_comments.py --apply --limit 5
```

### 4. Custom Comment Copy
```bash
./venv/bin/python sync_pinned_comments.py --apply --comment "🚀 Join our AI Architect & Builder Community: https://www.skool.com/delivery-pilot-8938"
```

## 📊 Output & Reports
- **Report File**: `pinned_comments_report.json`
- **Web Interface**: View status and details on [`skills.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/skills.html)
