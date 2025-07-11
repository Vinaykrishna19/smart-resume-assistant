---
title: Smart Resume Assistant
emoji: 🌖
colorFrom: blue
colorTo: blue
sdk: docker
pinned: false
license: apache-2.0
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# Smart Resume Assistant 🚀

## Overview

Smart Resume Assistant allows you to:
1. Upload a resume PDF to receive AI-powered improvement suggestions.
2. Upload a resume and job description to see a match score, matched/missing skills, and tailored advice.

## Endpoints

### 🧠 Resume Analysis (No Manual Copy-Paste)

**POST** `/analyze-pdf`

Upload a resume PDF. Returns:
- Summary
- Skills (grouped)
- Education
- Experience
- Project details
- Improvement tips
- Job-fit score

---

### 🎯 Resume to Job Matching

**POST** `/match-files`

Upload:
- `resume_file` (PDF)
- `jd_file` (PDF or `.txt`)

Returns:
- Match score (0.0 to 1.0)
- Matched + missing skills
- Recommendations
- AI-fit summary

---
    
## Setup

1. Create and activate your Python venv
2. Install dependencies:

```bash
pip install -r requirements.txt
