import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'inventory_db')
    PORT = int(os.getenv('PORT', 3001))
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
    AWS_BEDROCK_KEY_ID= os.getenv('AWS_BEDROCK_KEY_ID')
    AWS_BEDROCK_SAK= os.getenv('AWS_BEDROCK_SAK')