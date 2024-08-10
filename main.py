from crewai import Crew, Process
from agents import YoutubeAutomationAgents
from tasks import YoutubeAutomationTasks
from tools.youtube_video_details_tool import YoutubeVideoDetailsTool
from tools.youtube_video_search_tool import YoutubeVideoSearchTool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

#Initialize GPT
OpenAI = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL_NAME)

#1. Create agents
agents = YoutubeAutomationAgents()

youtube_manager = agents.youtube_manager()
research_manager = agents.research_manager(
    youtube_video_search_tool=YoutubeVideoSearchTool(), 
    youtube_video_details_tool=YoutubeVideoDetailsTool()
    )
title_creator = agents.title_creator()
description_creator = agents.description_creator()
email_creator = agents.email_creator()

#Background info about youtube video
video_topic = "Automating Tasks using CrewAI"
video_details = """In this video, we're diving into the innovative ways I'm using CrewAI to automate my YouTube Channel. 
From conducting through research to streamline video preparation, CrewAI is revolutionizing the way how I create content.
But that's not all - I'm also exploring how to harness the power of CrewAI to generate
personalized emails for my subscribers. Join me on this journey as I unlock the potnetial of AI to enhance
my YouTube channel and connect with my audience like never before."""

# 2. Create Tasks
tasks = YoutubeAutomationTasks()

#Setup tasks
manage_youtube_video_creation = tasks.manage_youtube_video_creation(agent=youtube_manager, video_topic=video_topic, video_details=video_details)
manager_youtube_video_research = tasks.manager_youtube_video_research(agent=research_manager, video_topic=video_topic, video_details=video_details)
create_youtube_video_titles = tasks.create_youtube_video_titles(agent=title_creator, video_topic=video_topic, video_details=video_details)
create_youtube_video_description = tasks.create_youtube_video_description(agent=description_creator, video_topic=video_topic, video_details=video_details)
create_youtube_video_email = tasks.create_youtube_video_email(agent=email_creator, video_topic=video_topic, video_details=video_details)

#3. Setup Crew
crew = Crew(
    agents=[youtube_manager, research_manager, title_creator, description_creator, email_creator],
    tasks=[manage_youtube_video_creation, manager_youtube_video_research, create_youtube_video_titles, create_youtube_video_description, create_youtube_video_email],
    process = Process.hierarchical,
    manager_llm=OpenAI
)

#Run the Crew
results = crew.kickoff()

print("Crew Usage", crew.usage_metrics) #The usage metrics of the crew basically helps in tracking of the tokens
print("\nCrew Work Results: \n")
print(results) #The results of the crew work