import pymysql
from config import Config

# MySQL Connection
def get_db_connection():
    try:
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
