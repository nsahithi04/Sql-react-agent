import os
import re
import time
from dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
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

max_retries = 3
for attempt in range(1, max_retries + 1):
    try:
        for step in agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            stream_mode="values",
        ):
            last = step["messages"][-1]
            if isinstance(last.content, list):
                for block in last.content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        print("\n" + block["text"])
            else:
                last.pretty_print()
        break
    except ChatGoogleGenerativeAIError as e:
        err = str(e)
        if "RESOURCE_EXHAUSTED" in err:
            if "PerDay" in err or "limit: 0" in err:
                print("\nDaily free tier quota exhausted.")
                print("Options: wait until tomorrow, or enable billing at https://aistudio.google.com")
                break
            match = re.search(r"retry in (\d+)", err)
            wait = int(match.group(1)) + 5 if match else 60
            print(f"\nRate limit hit (attempt {attempt}/{max_retries}). Waiting {wait}s...")
            time.sleep(wait)
        else:
            raise
else:
    print("Max retries exceeded.")