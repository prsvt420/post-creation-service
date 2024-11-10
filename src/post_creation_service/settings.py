import os
from dotenv import load_dotenv

dotenv_path: str = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path) if os.path.exists(dotenv_path) else print('No .env file found. ')

# REDDIT
REDDIT_CLIENT_ID: str = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET: str = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_REDIRECT_URI: str = os.environ.get('REDDIT_REDIRECT_URI')
REDDIT_USER_AGENT: str = os.environ.get('REDDIT_USER_AGENT')
REDDIT_USERNAME: str = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD: str = os.environ.get('REDDIT_PASSWORD')

# X / TWITTER
X_API_KEY: str = os.environ.get('X_API_KEY')
X_API_SECRET_KEY: str = os.environ.get('X_API_SECRET_KEY')
X_BEARER_TOKEN: str = os.environ.get('X_BEARER_TOKEN')
X_ACCESS_TOKEN: str = os.environ.get('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET: str = os.environ.get('X_ACCESS_TOKEN_SECRET')
X_CLIENT_ID: str = os.environ.get('X_CLIENT_ID')
X_CLIENT_SECRET: str = os.environ.get('X_CLIENT_SECRET')

# GOOGLE SHEETS
