
import sys
 
sys.path.append('../ru_cedro')
from helpers import database

conn = database.get_mysql_connection()

data = database.read_mysql_dataset(conn, ["campus", "menu"])
