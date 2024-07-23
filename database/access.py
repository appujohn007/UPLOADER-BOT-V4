

from config import Config
from database.database import Database

techvj = Database(Config.TECH_VJ_DATABASE_URL, Config.TECH_VJ_SESSION_NAME)
