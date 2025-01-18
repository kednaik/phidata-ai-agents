import os
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.python import PythonTools
from phi.tools.wikipedia import WikipediaTools
from phi.tools.youtube_tools import YouTubeTools
from phi.run.response import RunEvent, RunResponse
import streamlit as st


os.environ['GRQ_API_KEY'] = st.secrets.get('GROQ_API_KEY')


web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for information",
    model=Groq(id='llama-3.1-70b-versatile'),
    tools=[DuckDuckGo()],
    instructions=['Always include sources and references in your search results.'],
    show_tool_calls=True,
    markdown=True
)

financial_agent = Agent(
    name="Financial Agent",
    role="Get financial data",
    model=Groq(id='llama-3.1-70b-versatile'),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True)],
    instructions=['Use tables to display the data'],
    show_tool_calls=True,
    markdown=True
)

python_agent = Agent(tools=[PythonTools()], 
                     show_tool_calls=True,
                     role='To generate python code',
                     model=Groq(id='llama-3.1-70b-versatile'),
                    markdown=True)

wikipedia_agent = Agent(tools=[WikipediaTools()], 
                        show_tool_calls=True, 
                        role='To get information from wikipedia',
                        model=Groq(id='llama-3.1-70b-versatile'),
                        markdown=True)

youtube_agent = Agent(
    tools=[YouTubeTools()],
    model=Groq(id="llama-3.1-70b-versatile"),
    role="Get captions and metadata of a YouTube video and answer questions",
    show_tool_calls=True,
    description="You are a YouTube agent. Obtain the captions of a YouTube video and answer questions."
)


multi_ai_agent = Agent(
    team=[web_search_agent, financial_agent, python_agent, wikipedia_agent, youtube_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=['Always include sources and references in your search results.', 'Use tables to display the data'],
    show_tool_calls=True,
    markdown=True,
    add_chat_history_to_messages=True
)

# multi_ai_agent.print_response("Search information for NVDA stock", stream=True)

def as_stream(response):
  for chunk in response:
    if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
      if chunk.event == RunEvent.run_response:
        yield chunk.content

# multi_ai_agent.print_response("Write a python script for fibonacci series and display the result till the 10th number",stream=True)

# multi_ai_agent.print_response('Summarize analyst recommendations and share the latest news for NVDA stock', stream=True)