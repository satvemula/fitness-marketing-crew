🏋️ AI Fitness Marketing Agency (CrewAI)
An autonomous multi-agent AI team designed to research fitness trends, develop marketing strategies, and generate SEO-optimized content for fitness brands. Built using CrewAI and Google Gemini 2.0 Flash.

🤖 The Crew (Agents)
This project orchestrates four autonomous agents working in sequence:

Trend Researcher: Scours the web for the latest fitness trends and competitor analysis.

Marketing Strategist: Develops a high-level strategy and content calendar based on research.

Content Creator: Drafts blogs, social media posts, and video scripts.

SEO Specialist: Optimizes all written content for search engines (keywords, meta descriptions).

🛠️ Tech Stack
Framework: CrewAI

LLM: Google Gemini 2.0 Flash

Search Tools: SerperDev (Google Search API)

Language: Python 3.10+

🚀 Getting Started
1. Installation

Clone the repo and install dependencies:

Bash
pip install -r requirements.txt
2. Environment Setup

Create a .env file in the root directory and add your API keys:

Plaintext
GOOGLE_API_KEY=your_gemini_key
SERPER_API_KEY=your_serper_key
3. Usage

Run the crew to generate a marketing campaign:

Bash
python crew.py
4. Customization

You can adjust the agent personas and task descriptions in the config/ folder:

config/agents.yaml: Defines the backstory and goals of the agents.

config/tasks.yaml: Defines the specific deliverables and expected outputs.

📂 Output
The crew saves its work in the resources/saved_drafts/ directory, organized by:

/blogs: Full markdown articles.

/posts: Social media captions and email drafts.

/reels: Video scripts for TikTok/Reels.

marketing_strategy.md: High-level strategic plan.