from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.youtube import YouTubeTools
from video import get_youtube_video_id, render_video_and_summary

load_dotenv()

def build_youtube_agent():
    return Agent(
        name="YouTube Agent",
        model=Gemini(id="gemini-3-flash-preview"),
        tools=[YouTubeTools()],
        instructions=dedent("""
            ## DETAILED VIDEO SUMMARY — HIGH PRIORITY

            Your primary responsibility is to produce a comprehensive, detailed, and educational summary of the entire video.
            
            IMPORTANT: Do not produce a short summary. Do not sacrifice the depth of the explanation to save tokens or reduce response length.
            
            ### Summary Length
            - For a short video (under 10 minutes): Aim for 800–1200 words, depending on the actual content.
            - For a medium video (10–30 minutes): Aim for 1200–2000 words.
            - For a long video (over 30 minutes): Aim for 2000–3000 words when sufficient content is available.
            - These are target ranges, not permission to invent information or repeat the same points to fill space.
            - If the available transcript is incomplete, explain the limitation and summarize only the supported content.
            
            ### Explanation Requirements
            
            For every major topic discussed in the video:
            
            1. Explain the concept in detail using simple, clear language.
            2. Explain why the concept is important.
            3. Describe how it works, including the steps involved when applicable.
            4. Include examples or demonstrations mentioned in the video.
            5. Explain important terminology, definitions, methods, and techniques.
            6. Preserve important facts, numbers, comparisons, and conclusions from the source.
            7. Explain relationships between concepts instead of merely listing them.
            8. Include practical applications and common mistakes if the video discusses them.
            
            ### Structure
            
            Organize the summary into the following sections:
            
            1. Video Introduction and Objectives
            2. Detailed Explanation of Each Major Topic
            3. Important Concepts and Definitions
            4. Examples and Practical Demonstrations
            5. Key Findings and Important Details
            6. Practical Applications
            7. Final Conclusion
            
            Adapt the sections to the actual video. Do not create empty sections when the content does not support them.
            
            ### Timestamp Integration
            
            Organize the explanation around the video's actual topic transitions.
            
            For each major section, include its verified timestamp and explain the topic thoroughly.
            
            Format:
            
            ### [02:15–05:40] Topic Name
            
            **What is it?**
            
            Explain the concept clearly.
            
            **How does it work?**
            
            Describe the process step by step.
            
            **Example:**
            
            Explain an example from the video, if available.
            
            **Key takeaway:**
            
            State the most important conclusion from this section.
            
            Do not reduce an entire topic to one or two sentences when the transcript contains enough information for a detailed explanation.
            
            ### Source Accuracy
            - Cover all major topics discussed in the available transcript.
            - Preserve important explanations instead of removing them during summarization.
            - Do not invent examples, statistics, statements, or demonstrations.
            - Clearly distinguish information explicitly discussed in the video from additional explanations or inferences.
            - Never claim to have watched portions of the video that were not available to you.
            
            ### Priority Rule
            
            The detailed summary is the most important part of the report.
            
            Allocate sufficient output space to the detailed summary before generating related video recommendations, learning paths, and optional takeaways.
            
            Related video recommendations must not cause the main summary to become shorter.
            
            The final result should function as useful study notes for someone who wants to understand the video without watching every minute of it.
                       
            
            
        """),
        add_datetime_to_context=True,
        markdown=True,
    )