import os
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # implicit check by google.cloud (and keras)

if __name__ == "__main__":
    print("STORAGE SERVICE...")

    client = storage.Client()

    breakpoint()
