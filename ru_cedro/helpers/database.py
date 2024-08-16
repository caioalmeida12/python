import mysql.connector

def get_mysql_connection(host="localhost", user="root", password="", database="back-rucedro"):
    """
    Retorna uma conexão com o banco de dados MySQL.

    :param host: O endereço do servidor MySQL. Padrão é "localhost".
    :type host: str
    :param user: O nome de usuário para autenticação. Padrão é "root".
    :type user: str
    :param password: A senha para autenticação. Padrão é uma string vazia.
    :type password: str
    :param database: O nome do banco de dados. Padrão é "back-rucedro".
    :type database: str
    :returns: Um objeto de conexão MySQL.
    :rtype: mysql.connector.connection.MySQLConnection
    :raises Exception: Se a conexão falhar.

    :example:
    conn = get_mysql_connection(host="localhost", user="root", password="", database="back-rucedro")
    """
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    # Verifica se a conexão foi bem-sucedida
    if conn.is_connected():
        print(f"Conexão bem-sucedida ao banco de dados {database}!")
    else:
        # Matar o processo se a conexão falhar
        raise Exception("Falha na conexão.")
    
    return conn

def read_mysql_dataset(conn, table_names):
    """
    Lê os datasets MySQL e retorna todas as colunas de cada tabela especificada.

    :param conn: A conexão com o banco de dados MySQL.
    :type conn: mysql.connector.connection.MySQLConnection
    :param table_names: Uma lista de nomes de tabelas para ler os dados.
    :type table_names: list
    :returns: Um dicionário onde a chave é o nome da tabela e o valor é um dicionário com as colunas e seus respectivos dados.
    :rtype: dict

    :example:
    datasets = read_mysql_dataset(conn, ["menu", "scheduling"])
    """
    cursor = conn.cursor()
    datasets = {}
    
    for table_name in table_names:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Obter os nomes das colunas
        columns = [desc[0] for desc in cursor.description]
        
        # Inicializar o dicionário para a tabela
        table_data = {column: [] for column in columns}
        
        # Preencher o dicionário com os dados
        for row in result:
            for column, value in zip(columns, row):
                table_data[column].append(value)
        
        datasets[table_name] = table_data
    
    cursor.close()
    return datasets