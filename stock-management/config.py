import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'inventory_db')
    PORT = int(os.getenv('PORT', 3001))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
