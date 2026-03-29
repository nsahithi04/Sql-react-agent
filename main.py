import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import system_prompt
from langchain.agents import create_agent
from db import db

load_dotenv()

llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0,
    )

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
)

question = input("Enter your question about the database: ")

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):

   step["messages"][-1].pretty_print()
   
    # last_message = step["messages"][-1]

    # if last_message.type == "ai":
    #     if isinstance(last_message.content, list):
    #         print(last_message.content[0]["text"])
    #     else:
    #         print(last_message.content)
