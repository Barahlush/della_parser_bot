import os

import dotenv

dotenv.load_dotenv('.env', verbose=True)
DATABASE_PATH = 'db_files/main.db'
os.makedirs('db_files', exist_ok=True)

TELEGRAM_BOT_API_TOKEN = os.environ.get('TELEGRAM_BOT_API_TOKEN')
