from dotenv import load_dotenv
import mysql.connector
import os
import pandas as pd

load_dotenv()

def get_mysql_connection():
    """
    Retorna uma conexão com o banco de dados MySQL.

    :returns: Um objeto de conexão MySQL.
    :rtype: mysql.connector.connection.MySQLConnection
    :raises Exception: Se a conexão falhar.
    """

    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_DATABASE")
    )
    
    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        print(f"Conexão bem-sucedida ao banco de dados {os.getenv('DB_DATABASE')}!")
    else:
        # Matar o processo se a conexão falhar
        raise Exception("Falha na conexão.")
    
    return conn

import pandas as pd

def get_column_data(cursor, table_name, *columns, where=None, **kwargs):
    """
    Retorna as colunas de uma tabela.

    :param cursor: O cursor da conexão.
    :type cursor: mysql.connector.cursor.MySQLCursor
    :param table_name: O nome da tabela.
    :type table_name: str
    :param columns: As colunas a serem retornadas. Se vazio, retorna todas.
    :type columns: str
    :param where: Condição para filtrar os dados.
    :type where: str, optional
    :returns: Os dados contidos nas colunas.
    :rtype: pandas.core.frame.DataFrame
    """
    
    if not columns:
        columns = "*"
    else:
        columns = ", ".join(columns)

    query = f"SELECT {columns} FROM {table_name}"
    if where:
        query += f" WHERE {where}"

    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(result, columns=columns)

    return df