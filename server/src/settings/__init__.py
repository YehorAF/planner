import os
import dotenv

dotenv.load_dotenv()

SQL_DATABASE_URL = os.getenv("SQL_DATABASE_URL")
CACHE_DATABASE_URL = os.getenv("CACHE_DATABASE_URL")