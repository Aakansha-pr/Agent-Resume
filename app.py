#================LOAD MODULES=================
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

# To Show Web - App: complete page layout
st.set_page_config(layout = 'wide')

# To Give Title
st.title("AI RESUME GENERATOR")

st.write("""Thia app helps user to build customized Professional
Resume with Latest job apply links""")

st.image("https://raw.githubusercontent.com/Aakansha-pr/Agent-Resume/refs/heads/main/bg.png")

st.sidebar.title("Fill Important details")
st.sidebar.image("https://raw.githubusercontent.com/Aakansha-pr/Agent-Resume/refs/heads/main/bg.png")
#==================API KEYS=================
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API", type = 'password')
GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API", type = 'password')
GROQ_API_KEY = st.sidebar.text_input("Groq-API", type = 'password')

all_API = [TAVILY_API_KEY,GROQ_API_KEY,GOOGLE_API_KEY]
if not all(all_API):
    st.error("Must give API keys")
    st.stop()
elif all(all_API):
    st.success('API KEYS LOADED SUCCESSFULLY')
#=================MODEL=====================
    model = ChatGoogleGenerativeAI(
        model = 'gemini-3.5-flash-lite',
        google_api_key = GOOGLE_API_KEY
    )
else:
    st.info("PASS ALL API-KEYS")

# MULTISELECT OPTION
options = ['Delhi','Mumbai','Pune','Banglore','Gurugram']
location = st.sidebar.multiselect("Select Location",
                                 options = options)

profile_op = ['Data Analysts', 'Data Engineer', 'Gen AI Engineer',
              'Full-Stack Dev', 'Data Scientist']
profile = st.sidebar.multiselect("Select Job Profile",
                                options = profile_op)

# ================GET USER INFO===============
st.markdown("""### GET USER INFO""")
user_info = st.text_area("""Write your Resume Description:""")
#=================MODEL=====================
model = ChatGoogleGenerativeAI(
        model = 'gemini-3.5-flash-lite',
        google_api_key = GOOGLE_API_KEY
    )
#response = model.invoke("hello buddy!")
#response.content[-1]['text']

#================TOOLS====================
def search_latest_news_jobs(query):
  """This function helps to fetch latest news or jobs rerlated article
  using tavily """

  client = TavilyClient(
      api_key = TAVILY_API )
  response = client.search(query)
  return response

#================AGENT CREATION=============
agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs]
)
#agent

#===============AGENT======================
def main_agent(agent,query):
  """This is the main agent or leader agent
  orchestrate sub agents"""

  # giving prompt to create detailed prompt for code generation
  prompt = """You are AI assistant and below given is a
  prompt, your task is to give detailed prompt for this.
  You are a professional Resume Generator where user will
  give their personal info, you have to create detailed
  resume for studentsand professional one, it must be
  with dynamic UI and UX and, with advanced CSS Professional
  Designing in black and pink color. Make sure to give output in HTML format only
  no markdowns allowed
   """

  response = agent.invoke({'messages': [{'role':'user','content':prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']

  # save prompt using file handling

  with open('prompt.txt','w') as f:
    f.write(detailed_prompt)

  user_details = f"""Below given is a user details generate\
  resume based on that, if not given keep: Python Developer
  user details: {query}
  """

  final_prompt = prompt + detailed_prompt + user_details

  # code generation
  response = agent.invoke({'messages': [{'role':'user','content':final_prompt}]})

  code = response['messages'][-1].content[-1]['text']
  return code

#==================Execution==============
#code = main_agent(agent,'AAKANSHA, DATA ANALYST')
#from IPython import display as DISPLAY
#DISPLAY.HTML(code)

#============PROMPT=====================
# fetch latest domain related jobs using tavily
def get_jobs(agent, Location = 'Noida,delhi',
             Profile = 'Data analyst, AI engineer'):
  Location = 'Noida, Delhi'
  Profile = 'Data analyst, AI engineer'


  prompt = f"""based on your given job profile,
  fetch latest jobs or job apply article using linkdln, naukri,indeed, or
  all popular job apply platforms, show results with JOB PROFILE
  NAME,LOCATION,SALARY,COMPANY NAME, SHOW jobs only
  related given {Location} and {Profile} everything in black and pink.
  outputmust be in professional HTML,naukri themes cards with
  dynamic design, show atleast Top 10 - 20 results with direct apply link"""

  response = agent.invoke({'messages': [{'role':'user','content':prompt}]})

  code = response['messages'][-1].content[-1]['text']
  return code

#==============EXECUTE===============
#code = get_jobs(agent)
#DISPLAY.HTML(code)

if st.button("Generate Resume"):
             with st.spinner("Agent Running"):
                 code = main_agent(agent,user_info)
                 st.html(code, width = "stretch",
                         unsafe_allow_javascript = True)
                 st.divider() # to give horizontal div
                 job_code = get_jobs(agent,location,profile)
                 st.html(job_code,width = "stretch",
                        unsafe_allow_javascript = True)
                 
                 
                 
                 
