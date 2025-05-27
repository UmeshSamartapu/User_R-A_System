from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRY_SECONDS = int(os.getenv("JWT_EXPIRY_SECONDS", 5400))