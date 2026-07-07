import streamlit as st
from pdf_utils import extract_text
from ai_engine import analyze_match, chat_reply
from theme import inject_theme

st.set_page_config(page_title="Scanline — Resume x JD Match", page_icon="🧩", layout="wide")

# ---------- session state ----------
defaults = {
    "dark_mode": True,
    "resume_text": "",
    "jd_text": "",
    "result": None,
    "chat_history": [],   # gemini-format history for the API
    "chat_display": [],   # (role, text) pairs for rendering
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

inject_theme(st.session_state.dark_mode)

# ---------- sidebar: score gauge (read-only) ----------
with st.sidebar:
    st.markdown("### 🧩 Scanline")
    st.toggle("Dark mode", key="dark_mode")
    st.divider()

    st.markdown('<div class="score-label">Match Score</div>', unsafe_allow_html=True)
    if st.session_state.result:
        score = st.session_state.result["score"]
    else:
        score = 0
    st.markdown(f'<div class="score-num">{score}<span style="font-size:18px;">/100</span></div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="gauge-wrap">
            <div class="gauge-fill" style="width:{score}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Auto-generated — updates after each scan.")

# ---------- header / description ----------
st.markdown("## 🧩 Scanline")   
st.markdown(
    "Upload your resume and a job description as PDFs. Scanline reads both the way "
    "an ATS would — scoring the match, flagging what's missing, and explaining why — "
    "so you know where you stand before you apply."
)

with st.expander("👀 See example output"):
    st.caption("A sample run — resume scanned against E2M's AI Engineer Internship JD.")
    ex1, ex2 = st.columns(2)
    with ex1:
        st.image("screenshots/screenshot_1.png", caption="Upload resume + JD", use_container_width=True)
        st.image("screenshots/screenshot_3.png", caption="Match report — matched vs missing", use_container_width=True)
    with ex2:
        st.image("screenshots/screenshot_2.png", caption="Score updates instantly after scan", use_container_width=True)
        st.image("screenshots/screenshot_4.png", caption="Ask Scanline for improvement tips", use_container_width=True)

st.markdown("---")

# ---------- uploads ----------
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("**📄 Resume / CV**")
    resume_file = st.file_uploader("Upload resume PDF", type=["pdf"], key="resume_upload", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("**📋 Job Description**")
    jd_file = st.file_uploader("Upload JD PDF", type=["pdf"], key="jd_upload", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

run = st.button("Run scan →", type="primary", use_container_width=False)

if run:
    if not resume_file or not jd_file:
        st.warning("Upload both the resume and the job description first.")
    else:
        with st.spinner("Scanning…"):
            st.session_state.resume_text = extract_text(resume_file)
            st.session_state.jd_text = extract_text(jd_file)
            try:
                st.session_state.result = analyze_match(st.session_state.resume_text, st.session_state.jd_text)
                st.session_state.chat_history = []
                st.session_state.chat_display = []
                st.rerun()
            except Exception as e:
                st.error(f"Scan failed: {e}")

# ---------- results ----------
if st.session_state.result:
    r = st.session_state.result
    st.markdown("### Match report")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**✓ Matched**")
        if r["matched"]:
            st.markdown("".join(f'<span class="chip-match">{m}</span>' for m in r["matched"]), unsafe_allow_html=True)
        else:
            st.caption("Nothing matched.")
    with c2:
        st.markdown("**✕ Missing**")
        if r["missing"]:
            st.markdown("".join(f'<span class="chip-miss">{m}</span>' for m in r["missing"]), unsafe_allow_html=True)
        else:
            st.caption("Nothing missing.")

    st.markdown("**Why this score**")
    st.markdown(f'<div class="app-card">{r["explanation"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------- chatbox ----------
st.markdown("### 💬 Ask Scanline")
st.caption("Uses your uploaded resume + JD as context — e.g. \"explain my missing points in brief\"")

for role, text in st.session_state.chat_display:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.write(text)

user_msg = st.chat_input("Type a question…")
if user_msg:
    st.session_state.chat_display.append(("user", user_msg))
    with st.chat_message("user"):
        st.write(user_msg)

    with st.chat_message("assistant"):
        with st.spinner("thinking…"):
            reply = chat_reply(
                st.session_state.chat_history,
                user_msg,
                st.session_state.resume_text,
                st.session_state.jd_text,
                st.session_state.result,
            )
            st.write(reply)

    st.session_state.chat_history.append({"role": "user", "parts": [user_msg]})
    st.session_state.chat_history.append({"role": "model", "parts": [reply]})
    st.session_state.chat_display.append(("assistant", reply))