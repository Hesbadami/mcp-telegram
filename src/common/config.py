import urllib
from dotenv import load_dotenv
import os

load_dotenv()

MCP_TRANSPORT = os.getenv('MCP_TRANSPORT', 'stdio')

TELEGRAM_CFG = {
    "api_id": int(os.getenv('TELEGRAM_API_ID', 0)),
    "api_hash": os.getenv('TELEGRAM_API_HASH', ''),
    "phone_number": os.getenv('TELEGRAM_PHONE_NUMBER', ''),
    "session_name": os.getenv('TELEGRAM_SESSION_NAME', 'default_session'),
}