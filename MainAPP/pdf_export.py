from html import escape

import markdown
from playwright.sync_api import sync_playwright


def create_summary_pdf(
    summary: str,
    video_title: str = "YouTube Video Analysis"
) -> bytes:

    # Convert AI-generated Markdown into HTML
    summary_html = markdown.markdown(
        str(summary or ""),
        extensions=[
            "extra",
            "sane_lists",
            "nl2br",
        ]
    )

    safe_title = escape(video_title)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">

        <title>{safe_title}</title>

        <style>
            @page {{
                size: A4;
            }}

            * {{
                box-sizing: border-box;
            }}

            html {{
                background: #080d1b;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 11pt;
                line-height: 1.75;
                color: #f8fafc;

                background:
                    radial-gradient(
                        ellipse at top left,
                        #20245a 0%,
                        transparent 45%
                    ),
                    linear-gradient(
                        135deg,
                        #080d1b 0%,
                        #111827 55%,
                        #0b1020 100%
                    );

                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}

            .page-container {{
                padding: 12px 4px 24px;
            }}

            /* PDF HEADER */

            .header {{
                padding: 28px 26px;
                margin-bottom: 24px;

                border: 1px solid #5145a8;
                border-radius: 18px;

                background: linear-gradient(
                    120deg,
                    #20245a,
                    #43318a,
                    #6d28d9
                );

                break-inside: avoid;
            }}

            .brand {{
                color: #ddd6fe;
                font-size: 9pt;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 12px;
            }}

            .header h1 {{
                color: #ffffff;
                font-size: 25pt;
                font-weight: 800;
                line-height: 1.25;
                margin: 0 0 12px;
                overflow-wrap: anywhere;
            }}

            .header p {{
                color: #e0e7ff;
                font-size: 10pt;
                margin: 0;
            }}

            /* SUMMARY CARD */

            .summary-card {{
                padding: 24px;

                border: 1px solid #374151;
                border-radius: 16px;

                background: #111827;
            }}

            .section-label {{
                color: #c4b5fd;
                font-size: 9pt;
                font-weight: bold;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin-bottom: 18px;
            }}

            /* HEADINGS */

            h1, h2, h3, h4 {{
                color: #c4b5fd;
                line-height: 1.4;
                overflow-wrap: anywhere;
            }}

            h1 {{
                font-size: 22pt;
            }}

            h2 {{
                font-size: 16pt;
                font-weight: 800;

                margin-top: 26px;
                margin-bottom: 12px;
                padding: 10px 12px;

                background: #20245a;
                border-left: 4px solid #818cf8;
                border-radius: 5px;

                break-after: avoid;
            }}

            h3 {{
                color: #a5b4fc;
                font-size: 13pt;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 8px;

                break-after: avoid;
            }}

            h4 {{
                color: #c4b5fd;
                font-size: 11pt;
                font-weight: bold;

                break-after: avoid;
            }}

            /* PARAGRAPHS */

            p {{
                color: #e2e8f0;
                margin: 9px 0 13px;
                overflow-wrap: anywhere;
                orphans: 3;
                widows: 3;
            }}

            strong, b {{
                color: #ffffff;
                font-weight: 800;
            }}

            em {{
                color: #c4b5fd;
            }}

            /* LISTS */

            ul, ol {{
                padding-left: 25px;
                margin: 10px 0 17px;
            }}

            li {{
                color: #e2e8f0;
                padding-left: 4px;
                margin-bottom: 7px;
                overflow-wrap: anywhere;
            }}

            li::marker {{
                color: #a78bfa;
            }}

            /* QUOTED TEXT */

            blockquote {{
                margin: 18px 0;
                padding: 12px 16px;

                background: #20245a;
                border-left: 4px solid #a78bfa;
                border-radius: 7px;
            }}

            blockquote p {{
                color: #e0e7ff;
                margin: 0;
            }}

            /* CODE */

            code {{
                color: #ddd6fe;
                background: #20245a;
                padding: 2px 5px;
                border-radius: 4px;
                overflow-wrap: anywhere;
            }}

            pre {{
                color: #e2e8f0;
                background: #080d1b;
                border: 1px solid #374151;
                border-radius: 9px;
                padding: 14px;

                white-space: pre-wrap;
                overflow-wrap: anywhere;
                word-break: break-word;

                break-inside: avoid;
            }}

            pre code {{
                color: inherit;
                background: transparent;
                padding: 0;
            }}

            /* LINKS */

            a {{
                color: #a5b4fc;
                text-decoration: underline;
                overflow-wrap: anywhere;
            }}

            /* TABLES */

            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 18px 0;

                font-size: 9pt;
                break-inside: auto;
            }}

            thead {{
                display: table-header-group;
            }}

            th {{
                background: #43318a;
                color: #ffffff;
                font-weight: bold;
                text-align: left;
            }}

            th, td {{
                padding: 9px;
                border: 1px solid #374151;
                overflow-wrap: anywhere;
            }}

            td {{
                color: #e2e8f0;
                background: #111827;
            }}

            tr {{
                break-inside: avoid;
            }}

            /* HORIZONTAL LINE */

            hr {{
                border: 0;
                border-top: 1px solid #374151;
                margin: 24px 0;
            }}

            /* IMAGES */

            img {{
                max-width: 100%;
                height: auto;
            }}

            /* KEEP SHORT CONTENT TOGETHER */

            p, blockquote, img {{
                break-inside: avoid;
            }}

            /* FOOTER */

            .footer {{
                text-align: center;
                color: #8792a8;
                font-size: 9pt;
                margin-top: 24px;
                padding-top: 14px;
                border-top: 1px solid #374151;
            }}
        </style>
    </head>

    <body>
        <main class="page-container">

            <header class="header">
                <div class="brand">
                    YouTube AI Analyzer
                </div>

                <h1>{safe_title}</h1>

                <p>
                    AI-powered video analysis and learning summary
                </p>
            </header>

            <section class="summary-card">
                <div class="section-label">
                    Video Analysis Report
                </div>

                <div class="summary-content">
                    {summary_html}
                </div>
            </section>

            <footer class="footer">
                Generated by YouTube AI Analyzer
            </footer>

        </main>
    </body>
    </html>
    """

    # Render HTML/CSS using Chromium and export to PDF
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page(
                viewport={
                    "width": 1200,
                    "height": 1600
                },
                device_scale_factor=1
            )

            page.set_content(
                html_content,
                wait_until="networkidle"
            )

            pdf_bytes = page.pdf(
                format="A4",
                print_background=True,
                display_header_footer=True,
                header_template="<div></div>",
                footer_template="""
                    <div style="
                        width: 100%;
                        font-size: 8px;
                        color: #8792a8;
                        text-align: center;
                        padding: 0 15mm;
                    ">
                        Page <span class="pageNumber"></span>
                        of <span class="totalPages"></span>
                    </div>
                """,
                margin={
                    "top": "15mm",
                    "bottom": "18mm",
                    "left": "15mm",
                    "right": "15mm"
                }
            )

            return pdf_bytes

        finally:
            browser.close()