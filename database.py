import mysql.connector

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '12345678',
    'database': 'pemdas_tugas_akhir'
}

def connect_database():
    try:
        connection = mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        print('Error connecting to db:', e)
        return None

    return connection

def close_database(connection):
    if connection and connection.is_connected():
        connection.close()

