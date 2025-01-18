import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

RAIL_TOKEN = os.environ["RAIL_TOKEN"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]
PUSHOVER_USER = os.environ["PUSHOVER_USER"]
UPRN_DEFAULT = os.environ.get("UPRN_DEFAULT")
