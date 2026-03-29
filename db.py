import requests, pathlib
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
import os
load_dotenv()

# url = os.getenv("db_url")
# local_path = pathlib.Path(os.getenv("local_path"))
# db = SQLDatabase.from_uri(f"sqlite:///{local_path}")

db = SQLDatabase.from_uri(os.getenv("DATABASE_URL"))