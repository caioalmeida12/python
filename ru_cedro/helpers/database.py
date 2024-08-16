import mysql.connector

def get_connection(host="localhost", user="root", password="", database="back-rucedro"):
    """
    Retorna uma conexão com o banco de dados MySQL.
    Lança uma exceção se a conexão falhar.
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
    Retorna um dicionário onde a chave é o nome da tabela e o valor é um mapa do tipo [k: string] -> [].
    
    Ex: read_mysql_dataset(conn, ["menu", "scheduling"])

    Retorna:
    {
        "menu": {
            "id": [1, 2, 3, 4],
            "name": ["Bife", "Frango", "Peixe", "Vegetariano"],
            "price": [10.0, 8.0, 7.0, 6.0]
        },
        "scheduling": {
            "id": [1, 2, 3, 4],
            "date": ["2021-10-01", "2021-10-02", "2021-10-03", "2021-10-04"],
            "menu_id": [1, 2, 3, 4]
        }
    }
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