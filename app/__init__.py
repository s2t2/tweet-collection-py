import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", default="impeachment") # OR choose your own project name
APP_ENV = os.getenv("APP_ENV", default="development") # "development" OR "production"
STORAGE_ENV = os.getenv("STORAGE_ENV", default="local") # "local" OR "remote"
