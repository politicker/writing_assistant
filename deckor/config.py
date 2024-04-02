import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'default_host'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'default_user'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME', 'default_dbname'),
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't')

# You can add more configuration variables as needed
