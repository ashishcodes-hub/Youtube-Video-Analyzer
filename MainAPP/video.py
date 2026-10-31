import html
import json
import re
from urllib.parse import urlparse, parse_qs
import streamlit as st


def get_youtube_video_id(url):
    """YouTube URL se video ID nikalta hai."""

    if not url:
        return None

    try:
        parsed = urlparse(url.strip())
        host = (parsed.hostname or "").lower()
        video_id = None

        # Example: https://youtu.be/VIDEO_ID
        if host == "youtu.be":
            video_id = parsed.path.strip("/").split("/")[0]

        # Standard YouTube URLs
        elif host in {
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtube-nocookie.com",
            "www.youtube-nocookie.com",
        }:
            if parsed.path == "/watch":
                video_id = parse_qs(parsed.query).get("v", [None])[0]

            else:
                parts = parsed.path.strip("/").split("/")

                if (
                    len(parts) >= 2
                    and parts[0] in {"embed", "shorts", "live"}
                ):
                    video_id = parts[1]

        # YouTube video ID normally 11 characters ka hota hai.
        if video_id and re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
            return video_id

    except (ValueError, AttributeError):
        pass

    return None

def render_video_and_summary(video_id, summary=""):
    """Display a YouTube player with a beautifully formatted Markdown summary."""

    import json
    import re
    import streamlit as st

    if not video_id or not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        return

    import re
    import html
    def make_clickable_timestamps(summary):
        """Convert timestamps in the summary into clickable HTML links."""

        safe_summary = html.escape(str(summary or ""))

        pattern = r"(?<!\d)(?:(\d{1,2}):)?([0-5]?\d):([0-5]\d)(?!\d)"

        def replace_timestamp(match):
            hours = int(match.group(1)) if match.group(1) else 0
            minutes = int(match.group(2))
            seconds = int(match.group(3))

            total_seconds = hours * 3600 + minutes * 60 + seconds
            timestamp = match.group(0)

            return (
                f'<a href="#video-player" '
                f'class="timestamp" '
                f'data-time="{total_seconds}">'
                f'{timestamp}</a>'
            )

        return re.sub(pattern, replace_timestamp, safe_summary)

    video_id_json = json.dumps(video_id)

    page = r"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/dompurify/dist/purify.min.js"></script>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 12px;
                background: #0b1020;
                color: #e5e7eb;
                font-family: Arial, sans-serif;
            }

            .player {
                width: 100%;
                aspect-ratio: 16 / 9;
                overflow: hidden;
                border-radius: 16px;
                background: #111827;
                border: 1px solid #30394d;
            }

            #player {
                width: 100%;
                height: 100%;
            }

            .report {
                margin-top: 24px;
                padding: 24px;
                background: #111827;
                border: 1px solid #30394d;
                border-radius: 16px;
                line-height: 1.8;
                overflow-wrap: anywhere;
            }

            .report h1 {
                color: #c4b5fd;
                font-size: 28px;
                border-bottom: 2px solid #6366f1;
                padding-bottom: 12px;
            }

            .report h2 {
                color: #a5b4fc;
                font-size: 22px;
                margin-top: 30px;
                padding-bottom: 8px;
                border-bottom: 1px solid #374151;
            }

            .report h3 {
                color: #67e8f9;
                font-size: 18px;
                margin-top: 22px;
            }

            .report p {
                color: #d1d5db;
                margin: 12px 0;
            }

            .report strong {
                color: #f9fafb;
            }

            .report ul,
            .report ol {
                padding-left: 24px;
            }

            .report li {
                margin: 8px 0;
            }

            .report blockquote {
                margin: 16px 0;
                padding: 12px 16px;
                background: #1e293b;
                border-left: 4px solid #818cf8;
                border-radius: 6px;
            }

            .report table {
                display: block;
                width: 100%;
                overflow-x: auto;
                border-collapse: collapse;
                margin: 18px 0;
            }

            .report th,
            .report td {
                padding: 12px;
                border: 1px solid #374151;
                text-align: left;
                min-width: 100px;
            }

            .report th {
                background: #312e81;
                color: #ffffff;
            }

            .report tr:nth-child(even) {
                background: #172033;
            }

            .report hr {
                border: 0;
                border-top: 1px solid #374151;
                margin: 24px 0;
            }

            .report code {
                color: #67e8f9;
                background: #1f2937;
                padding: 3px 6px;
                border-radius: 4px;
            }

            .report a.timestamp {
                color: #a5b4fc;
                font-weight: bold;
                text-decoration: none;
                background: #252447;
                border-radius: 5px;
                padding: 2px 5px;
                cursor: pointer;
                white-space: nowrap;
            }

            .report a.timestamp:hover {
                color: #ffffff;
                background: #4f46e5;
            }

            .report a:not(.timestamp) {
                color: #67e8f9;
            }

            .report em {
                color: #c4b5fd;
            }


            
        </style>
    </head>

    <body>
        <div class="player">
            <div id="player"></div>
        </div>

        <div class="report">
            <div id="summary">Loading analysis...</div>
        </div>

        <script>
            const VIDEO_ID = VIDEO_ID_PLACEHOLDER;
            const RAW_SUMMARY = SUMMARY_PLACEHOLDER;

            let youtubePlayer;

            // Convert a timestamp into seconds.
            function timestampToSeconds(value) {
                const parts = value.split(":").map(Number);

                if (
                    parts.length < 2 ||
                    parts.length > 3 ||
                    parts.some(Number.isNaN)
                ) {
                    return null;
                }

                let seconds;

                if (parts.length === 2) {
                    seconds = parts[0] * 60 + parts[1];
                } else {
                    seconds = (
                        parts[0] * 3600 +
                        parts[1] * 60 +
                        parts[2]
                    );
                }

                return seconds;
            }

            // Render Markdown and make timestamp links clickable.
            
            function renderSummary() {
                const container = document.getElementById("summary");

                if (!RAW_SUMMARY.trim()) {
                    container.innerHTML =
                        "<p>Please! wait for generate your report.</p>";
                    return;
                }

                if (typeof marked === "undefined") {
                    container.textContent = RAW_SUMMARY;
                    return;
                }

                // Markdown ko HTML mein convert karein.
                const renderedHTML = marked.parse(RAW_SUMMARY);

                // HTML ko sanitize karke render karein.
                container.innerHTML = DOMPurify.sanitize(renderedHTML);

                // 1. Markdown links mein maujood timestamps ko clickable banayein.
                container.querySelectorAll("a").forEach(function(link) {
                    const timestamp = link.textContent.trim();

                    if (/^(?:\d{1,2}:)?\d{1,2}:\d{2}$/.test(timestamp)) {
                        const seconds = timestampToSeconds(timestamp);

                        if (seconds !== null) {
                            link.classList.add("timestamp");
                            link.dataset.time = seconds;
                            link.href = "#";
                            link.removeAttribute("target");
                        }
                    }
                });

                // 2. Plain text mein maujood timestamps ko bhi clickable banayein.
                const walker = document.createTreeWalker(
                    container,
                    NodeFilter.SHOW_TEXT
                );

                const textNodes = [];
                let node;

                while ((node = walker.nextNode())) {
                    // Existing links aur code blocks ke andar changes na karein.
                    if (
                        node.parentElement &&
                        !node.parentElement.closest(
                            "a, code, pre, script, style"
                        )
                    ) {
                        textNodes.push(node);
                    }
                }

                const timestampPattern = /(?<![\d:])(?:\d{1,2}:)?\d{1,2}:\d{2}(?![\d:])/g;

                textNodes.forEach(function(textNode) {
                    const text = textNode.nodeValue;
                    timestampPattern.lastIndex = 0;

                    if (!timestampPattern.test(text)) {
                        return;
                    }

                    timestampPattern.lastIndex = 0;

                    const fragment = document.createDocumentFragment();
                    let lastIndex = 0;
                    let match;

                    while ((match = timestampPattern.exec(text)) !== null) {
                        fragment.appendChild(
                            document.createTextNode(
                                text.slice(lastIndex, match.index)
                            )
                        );

                        const timestamp = match[0];
                        const seconds = timestampToSeconds(timestamp);

                        if (seconds !== null) {
                            const link = document.createElement("a");

                            link.href = "#";
                            link.className = "timestamp";
                            link.dataset.time = seconds;
                            link.textContent = timestamp;

                            fragment.appendChild(link);
                        } else {
                            fragment.appendChild(
                                document.createTextNode(timestamp)
                            );
                        }

                        lastIndex = match.index + timestamp.length;
                    }

                    fragment.appendChild(
                        document.createTextNode(text.slice(lastIndex))
                    );

                    textNode.parentNode.replaceChild(fragment, textNode);
                });
            }

            window.onYouTubeIframeAPIReady = function() {
                youtubePlayer = new YT.Player("player", {
                    videoId: VIDEO_ID,
                    playerVars: {
                        playsinline: 1,
                        rel: 0
                    },
                    events: {
                        onReady: function() {
                            console.log("YouTube player ready");
                        }
                    }
                });
            };

            document.addEventListener("click", function(event) {
                const link = event.target.closest("a.timestamp");

                if (!link) return;

                event.preventDefault();

                const seconds = Number(link.dataset.time);

                if (!Number.isFinite(seconds) || seconds < 0) return;

                if (
                    youtubePlayer &&
                    typeof youtubePlayer.seekTo === "function"
                ) {
                    // Player tak screen scroll karein.
                    document.querySelector(".player").scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                    // Video ko selected timestamp par le jayein.
                    youtubePlayer.seekTo(seconds, true);
                    youtubePlayer.playVideo();
                } else {
                    console.error("YouTube player abhi ready nahi hai.");
                }
            });

            renderSummary();
        </script>

        <script src="https://www.youtube.com/iframe_api"></script>
    </body>
    </html>
    """

    page = page.replace("VIDEO_ID_PLACEHOLDER", video_id_json)

    summary_json = json.dumps(str(summary or ""), ensure_ascii=False)
    page = page.replace("SUMMARY_PLACEHOLDER", summary_json)

    page = page.replace("VIDEO_ID_PLACEHOLDER", video_id_json)

    summary_json = json.dumps(str(summary or ""), ensure_ascii=False)
    page = page.replace("SUMMARY_PLACEHOLDER", summary_json)
    

    st.iframe(
        page,
        height=1100,
    )
