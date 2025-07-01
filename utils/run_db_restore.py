import os
from pathlib import Path
from dotenv import load_dotenv
from db_restore import DbRestore
import logging

LOCAL_ENV_PATH = Path(os.getcwd()) / "local.env"
logging.info(f"Checking for local.env file at: {LOCAL_ENV_PATH}")
if Path.is_file(LOCAL_ENV_PATH):
    load_dotenv(LOCAL_ENV_PATH, override=False)
    DbRestore().full_db_restore()
else:
    logging.info("No local.env file found. Skipping database restore.")
