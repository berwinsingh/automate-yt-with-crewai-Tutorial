from agents import YouTubeAuthomationAgents
from tasks import YouTubeAuthomationTasks

#1. Create agents
agents = YouTubeAuthomationAgents()

#Stup agents
youtube_manager = agents.youtube_manager()
research_manager = agents.research_manager()
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
tasks = YouTubeAuthomationTasks()

#Setup tasks
manage_youtube_video_creation = tasks.manage_youtube_video_creation(agent=youtube_manager, video_topic=video_topic, video_details=video_details)
manager_youtube_video_research = tasks.manager_youtube_video_research(agent=research_manager, video_topic=video_topic)
create_youtube_video_titles = tasks.create_youtube_video_titles(agent=title_creator, video_topic=video_topic)
create_youtube_video_description = tasks.create_youtube_video_description(agent=description_creator, video_topic=video_topic)
create_youtube_video_email = tasks.create_youtube_video_email(agent=email_creator, video_topic=video_topic)

#3. Create Tools