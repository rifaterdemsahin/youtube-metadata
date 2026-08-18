---
name: sync-first-lines-skool-cta
description: >-
  Ensures the first 2 lines of YouTube video descriptions are dedicated to a Skool community Call-to-Action link.
  Use when the user wants to optimize description above-the-fold click-through rates, format the first 2 lines for Skool promotion, or update video description headers.
---

# Skill: Top 2 Lines Skool CTA Description Syncer

Optimizes the top 2 lines of all YouTube video descriptions for maximum click-through rate (CTR) to the Skool community before the "...more" fold.

## 🎯 Target Link & Channel
- **Target Skool Community**: `https://www.skool.com/delivery-pilot-8938`
- **Target Channel**: `@RifatErdemSahin`

## 🚀 Execution Commands

### 1. Dry Run (Simulated)
```bash
./venv/bin/python update_first_lines_skool.py --dry-run
```

### 2. Live Apply (Targeting All Videos)
```bash
./venv/bin/python update_first_lines_skool.py --apply
```

### 3. Live Apply (Limited Batch)
```bash
./venv/bin/python update_first_lines_skool.py --apply --limit 5
```

### 4. Custom CTA Text
```bash
./venv/bin/python update_first_lines_skool.py --apply --cta "🚀 Join our AI Architect & Builder Community: https://www.skool.com/delivery-pilot-8938"
```

## 📊 Output & Reports
- **Report File**: `first_lines_report.json`
- **Web Interface**: View and monitor on [`skills.html`](file:///Users/rifaterdemsahin/projects/youtube-metadata/skills.html)
