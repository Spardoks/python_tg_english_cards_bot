from dotenv import dotenv_values, load_dotenv

config = dotenv_values(".env")
load_dotenv()

TG_TOKEN = config["TG_TOKEN"]

USE_DB = config["USE_DB"]
DB_USER = config["DB_USER"]
DB_PASSWORD = config["DB_PASSWORD"]
DB_IP = "localhost"
DB_PORT = "5432"
DB_NAME = "telecardsdb"
DB_PROTOCOL = "postgresql+psycopg2"
DSN = f"{DB_PROTOCOL}://{DB_USER}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"
