---
name: sync-end-cards-skool
description: >-
  Configures and sets YouTube video End Cards and End Screens promoting the featured Skool Community video and community link.
  Use when the user wants to add end cards, calculate end screen timestamps, set featured community videos, or generate YouTube Studio end-screen links.
---

# Skill: YouTube End Cards & Skool Community Video Promoter

Configures End Cards and End Screens across channel videos to drive viewer engagement and conversions directly to the featured Skool community video (`HUTlnlw3h8o` - *Building an AI Knowledge Engine*) and the Skool community link.

## 🎯 Target Channel & Featured Skool Assets
- **Target Channel**: `@RifatErdemSahin`
- **Featured Skool Video**: `HUTlnlw3h8o` (*Building an AI Knowledge Engine: Turn 46k Obsidian Notes into Clarity*)
- **Skool Community Link**: `https://www.skool.com/delivery-pilot-8938`

## 🚀 Execution Commands

### 1. Dry Run (Preview & Calculation)
```bash
./venv/bin/python sync_end_cards.py --dry-run
```

### 2. Live Apply (Targeting All Videos)
```bash
./venv/bin/python sync_end_cards.py --apply
```

### 3. Custom Featured Video Selection
```bash
./venv/bin/python sync_end_cards.py --apply --featured-video HUTlnlw3h8o
```

## 📊 Output & Reports
- **Report File**: `end_cards_report.json`
- **Web Interface**: View all video end cards and Studio deep links on [`skills.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/skills.html)
