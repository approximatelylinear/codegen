import os
from pathlib import Path

import dotenv

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv.load_dotenv(Path(THIS_DIR) / 'config/.env')

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
COHERE_API_KEY = os.environ.get('COHERE_API_KEY')