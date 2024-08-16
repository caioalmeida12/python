
import sys
 
sys.path.append('../ru_cedro')
from helpers import database

# Conectar ao banco de dados
conn = database.get_connection()

# Verifica se a conexão foi bem-sucedida
if conn.is_connected():
    print("Conexão bem-sucedida no use_connection.py!")
else:
    # Matar o processo se a conexão falhar
    raise Exception("Falha na conexão.")

# Obter os dados da tabela "campus"
data = database.read_mysql_dataset(conn, ["campus", "menu"])
