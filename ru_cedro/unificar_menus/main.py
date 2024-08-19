import os
import sys

# Adiciona o diretório raiz ao path do sistema
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import database

conn = database.get_mysql_connection()
cursor = conn.cursor()

menus = database.get_column_data(cursor, "menu")

print(menus)