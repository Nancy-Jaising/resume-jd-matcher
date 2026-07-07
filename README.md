# 🧩 Scanline — Resume × JD Matching Tool

An AI-powered tool that compares a resume against a job description the way an ATS would — scoring the match, flagging matched and missing skills, and explaining the reasoning in plain language.

**🔗 Live app:** https://resume-jd-matcher-fqklhtdlmz7aehpejstl9c.streamlit.app/
**📦 GitHub:** https://github.com/Nancy-Jaising/resume-jd-matcher

## What it does

- Upload a resume and a job description (PDF)
- Extracts skills and requirements from both using an LLM
- Computes a **match score (0–100)**
- Shows a clear **matched vs. missing skills** breakdown
- Generates a **narrative explanation** of the score
- Includes a chatbox to ask follow-up questions (e.g. *"which areas can I improve?"*)
- Light and dark mode support

## Tech stack

- **Frontend:** Streamlit
- **AI:** Google Gemini API (`gemini-2.5-flash`)
- **PDF parsing:** pypdf

## Project structure
resume-jd-matcher/
├── app.py              # main Streamlit app
├── theme.py            # purple theme + light/dark mode CSS
├── pdf_utils.py         # PDF text extraction
├── ai_engine.py         # Gemini API calls (scoring + chat)
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── screenshots/         # example output

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the root folder:
GEMINI_API_KEY=your_key_here

Run the app:
```bash
streamlit run app.py
```

## Example output

See the `screenshots/` folder, or the in-app "See example output" section, for a sample run scanning a resume against an AI Engineer Internship JD — scoring **65/100** with a full matched/missing breakdown and explanation.

## Notes

- Score, matched/missing skills, and explanation are all generated live by the LLM based on the uploaded documents — nothing is hardcoded.
- The chatbox reuses the same score from the scan (not recalculated) to stay consistent with the sidebar display.
