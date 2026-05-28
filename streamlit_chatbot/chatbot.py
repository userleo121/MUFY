import os
from pathlib import Path
import streamlit as st
from google import genai

# Use safe access to secrets to avoid KeyError in deployed envs
api_key = st.secrets.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="StudyBuddy Match", page_icon="📚", layout="wide")

# Load the HTML file relative to this file so it works when deployed
base_dir = Path(__file__).parent
html_path = base_dir / "studybuddy.html"
if not html_path.exists():
    st.error(f"studybuddy.html not found at {html_path}")
    html_src = ""
else:
    with open(html_path, "r", encoding="utf-8") as f:
        html_src = f.read()

# ── Patch 1: inject the API key so the HTML can call Gemini directly ──
# Replace the empty key initialisation with the real key from secrets
if html_src:
    html_src = html_src.replace(
        'let geminiApiKey = localStorage.getItem("gemini_api_key") || "";',
        f'let geminiApiKey = "{api_key}";'
    )

# ── Patch 2: upgrade model to gemini-2.5-flash (higher free quota) ──
if html_src:
    html_src = html_src.replace(
        "gemini-2.0-flash",
        "gemini-2.5-flash"
    )

# ── Patch 3: hide the API key banner entirely (key is baked in) ──
if html_src:
    html_src = html_src.replace(
        "// Show API key banner if key not set\n  const banner=document.getElementById(\"api-key-banner\");\n  banner.classList.toggle(\"visible\", !geminiApiKey);",
        "document.getElementById(\"api-key-banner\").classList.remove(\"visible\");"
    )

# ── Patch 4: skip the key-check gate in the send handler ──
if html_src:
    html_src = html_src.replace(
        '    // Gemini tutor\n    if(!geminiApiKey){\n      document.getElementById("api-key-banner").classList.add("visible");\n      chatInput.value=txt; chatSend.disabled=false; return;\n    }\n    tutorMessages.push({role:"user",text:txt});',
        '    // Gemini tutor (key injected server-side)\n    tutorMessages.push({role:"user",text:txt});'
    )

st.components.v1.html(html_src, height=900, scrolling=True)