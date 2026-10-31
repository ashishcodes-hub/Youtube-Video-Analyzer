
import streamlit as st
from pathlib import Path
from urllib.parse import urlparse

from youtube_analyzer import build_youtube_agent
from video import get_youtube_video_id, render_video_and_summary
from pdf_export import create_summary_pdf


# ========================================
# PAGE CONFIGURATION
# ========================================

st.set_page_config(
    page_title="YouTube AI Analyzer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ========================================
# LOAD CSS
# ========================================

CSS_PATH = Path(__file__).resolve().parent / "style.css"

if not CSS_PATH.is_file():
    st.error(
        "style.css file nahi mili. "
        "Please ui.py aur style.css ko same folder mein rakho."
    )
    st.stop()

css = CSS_PATH.read_text(encoding="utf-8")

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# ========================================
# LOAD AI AGENT
# ========================================

@st.cache_resource
def get_agent():
    return build_youtube_agent()


# ========================================
# HERO SECTION
# ========================================

st.markdown(
    """
    <div class="hero-container">
        <h1 class="hero-title">
            Understand Videos<br>
            <span class="hero-gradient">Beyond Watching.</span>
        </h1>

        
    </div>
    """,
    unsafe_allow_html=True
)



# ========================================
# FEATURE CARDS
# ========================================

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Smart Summaries</div>
            <div class="feature-description">
                Understand the main ideas and important concepts
                without manually reviewing the entire video.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">⏱️</div>
            <div class="feature-title">Key Moments</div>
            <div class="feature-description">
                Explore important topics and useful moments
                identified during the video analysis.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Learning Insights</div>
            <div class="feature-description">
                Discover key takeaways and explanations
                to understand video content more effectively.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ========================================
# VIDEO ANALYZER
# ========================================

st.markdown(
    """
    <div class="analyzer-heading">
        🎬 Analyze Your Video
    </div>

    <div class="analyzer-description">
        Enter a public YouTube video link to get started.
    </div>
    """,
    unsafe_allow_html=True
)

video_url = st.text_input(
    "YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    key="youtube_video_url"
)

analyze_button = st.button(
    "🚀 Analyze Video",
    use_container_width=True
)


# ========================================
# URL VALIDATION
# ========================================

def is_valid_youtube_url(url: str) -> bool:
    try:
        parsed = urlparse(url.strip())
        host = (parsed.hostname or "").lower()

        allowed_hosts = {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
            "www.youtube-nocookie.com",
        }

        return (
            parsed.scheme in {"http", "https"}
            and host in allowed_hosts
            and bool(parsed.path.strip("/"))
        )

    except (ValueError, AttributeError):
        return False


# ========================================
# ANALYZE VIDEO
# ========================================

if analyze_button:

    if not video_url.strip():
        st.warning("Please enter YouTube video URL .")

    elif not is_valid_youtube_url(video_url):
        st.error("Enter Valid YouTube video URL.")

    else:
        try:
            with st.spinner(
                "🤖 AI video analyze... Please wait."
            ):
                agent = get_agent()

                response = agent.run(
                    f"Analyze this video: {video_url.strip()}"
                )

            # Get the AI analysis result
            content = getattr(response, "content", None)
            
            if content:
                st.session_state["analysis_result"] = str(content)
                st.session_state["analyzed_video_id"] = (
                    get_youtube_video_id(video_url)
                )
            else:
                st.session_state["analysis_result"] = ""
                st.session_state["analyzed_video_id"] = (
                    get_youtube_video_id(video_url)
                )
                st.info("Agent ne koi text report return nahi ki.")

        except Exception as error:
            st.error(
                "Video analysis complete nahi ho paya. "
                "Please URL aur API configuration check karo."
            )
            st.caption(f"Technical details: {error}")


# # ========================================
# # YOUTUBE VIDEO PLAYER AND ANALYSIS
# # ========================================

# current_video_id = get_youtube_video_id(video_url)

# if current_video_id:
#     saved_video_id = st.session_state.get("analyzed_video_id")
#     saved_summary = st.session_state.get("analysis_result", "")

#     if saved_video_id == current_video_id:
#         render_video_and_summary(
#             current_video_id,
#             saved_summary
#         )
#     else:
#         render_video_and_summary(
#             current_video_id,
#             ""
#         )

# ========================================
# YOUTUBE VIDEO PLAYER AND ANALYSIS
# ========================================

current_video_id = get_youtube_video_id(video_url)

if current_video_id:
    saved_video_id = st.session_state.get("analyzed_video_id")
    saved_summary = st.session_state.get("analysis_result", "")

    if saved_video_id == current_video_id:
        # Video aur summary sirf ek baar render karo
        render_video_and_summary(
            current_video_id,
            saved_summary
        )

        if saved_summary.strip():
            pdf_bytes = create_summary_pdf(
                summary=saved_summary,
                video_title="YouTube Video Analysis"
            )

            st.download_button(
                label="📄 Download Summary as PDF",
                data=pdf_bytes,
                file_name="youtube_summary.pdf",
                mime="application/pdf",
                key="download_summary_pdf"
            )

    else:
        render_video_and_summary(
            current_video_id,
            ""
        )

# ========================================
# FOOTER
# ========================================

st.markdown(
    """
    <div class="app-footer">
        Built with ❤️ using Streamlit and AI
    </div>
    """,
    unsafe_allow_html=True
)
