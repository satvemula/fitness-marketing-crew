fitness_marketing_crew

I built this project using the CrewAI framework to automate fitness content marketing.
This AI crew helps me generate fitness-focused social media posts, captions, trend research, and posting strategies — perfect for fitness creators, hybrid athletes, and gym brands.


Features

- A Fitness Trend Researcher agent that finds viral fitness topics and hashtags
- A Fitness Content Creator agent that writes engaging posts, captions, and scripts
- A Social Media Strategist agent that recommends posting schedules and platforms
- Easily customizable YAML configs for agents and tasks
- A resources folder where I keep draft content templates and marketing plans


How I Run It

1. I install the dependencies with:

   poetry install
   # or
   pip install -r requirements.txt

2. I update my OpenAI API key in `.env` or environment variables

3. I run the crew with:

   python marketing-crew/crew.py

4. Then I review the generated fitness content in the console or saved drafts


How I Customize It

-I modified the agents and tasks in `marketing-crew/config/agents.yaml` and `tasks.yaml` to fit my brand voice and niche
- I added fitness content drafts in `marketing-crew/resources/saved_drafts/`
- I extended the crew by adding more agents (like a Graphic Designer or Email Marketer)


References

- This is based on the CrewAI Crash Course by Codebasics: https://github.com/codebasics/crewai-crash-course
- And I used the Google Gemini CrewAI docs as a guide: https://ai.google.dev/gemini-api/docs/crewai-example

