# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#     DATABASE_URL = os.getenv("DATABASE_URL")
#     SECRET_KEY = os.getenv("SECRET_KEY")
    
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    EURI_API_KEY = os.getenv("EURI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")

