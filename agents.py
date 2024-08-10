from crewai import Agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

openai = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL_NAME)

#Defining human tools to be used in the email creator agent for feedback
human_tools = load_tools(["human"])

class YoutubeAutomationAgents():
    def youtube_manager(self):
        return Agent(
            role="Youtube Manager",
            goal="""Oversee the YouTube prepration process including market research, title ideation, description, and email announcement creation required to make a YouTube Video""",
            #Here we have defined a process in a streamlined way to ensure proper steps are followed to create a successful YouTube video.
            backstory="""As a methodical and detailed oriented managar, you are responsible for overseeing the preperation of YouTube videos.
                When creating YouTube videos, you follow the following process to create a video that has a high chance of success:
                1. Search YouTube to find a minimum of 15 other videos on the same topic and analyze their titles and descriptions.
                2. Create a list of 10 potential titles that are less than 70 characters and should have a high click-through-rate.
                    -  Make sure you pass the list of 1 videos to the title creator 
                        so that they can use the information to create the titles.
                3. Write a description for the YouTube video.
                4. Write an email that can be sent to all subscribers to promote the new video.""",
            llm = openai,
            allow_delegation=True,
            verbose=True,
        )
    
    def research_manager(self, youtube_video_search_tool, youtube_video_details_tool):
        #This manager is going go off and research on our YouTube videos
        return Agent(
            role="YouTube Research Manager",
            goal="""For a given topic and description for a new YouTube video, find a minimum of 15 high-performing videos 
                on the same topic with the ultimate goal of populating the research table which will be used by 
                other agents to help them generate titles  and other aspects of the new YouTube video 
                that we are planning to create.""",
            backstory="""As a methodical and detailed research managar, you are responsible for overseeing researchers who 
                actively search YouTube to find high-performing YouTube videos on the same topic.""",
            llm = openai,
            allow_delegation=True,
            tools = [youtube_video_search_tool, youtube_video_details_tool]
        )
    
    def title_creator(self):
        return Agent(
            role="Title Creator",
            goal="""Create 10 potential titles for a given YouTube video topic and description. 
                You should also use previous research to help you generate the titles.
                The titles should be less than 70 characters and should have a high click-through-rate.""",
            backstory="""As a Title Creator, you are responsible for creating 10 potential titles for a given 
                YouTube video topic and description.""",
            verbose=True,
            llm = openai,
        )

    def description_creator(self):
        return Agent(
            role="Description Creator",
            goal="""Create a description for a given YouTube video topic and description.""",
            backstory="""As a Description Creator, you are responsible for creating a description for a given 
                YouTube video topic and description.""",
            verbose=True,
            llm = openai,
        )
    
    def email_creator(self):
         return Agent(
            role="Email Creator",
            goal="""Create an email to send to the marketing team to promote the new YouTube video.""",
            backstory="""As an Email Creator, you are responsible for creating an email to send to the marketing team 
                to promote the new YouTube video.
                
                It is vital that you ONLY ask for human feedback after you've created the email.
                Do NOT ask the human to create the email for you.
                """,
            verbose=True,
            tools=human_tools, #This tool adds a human in between which ensures that until the email is approved it isn't sent.
            llm = openai,
        )