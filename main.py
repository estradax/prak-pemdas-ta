import mysql.connector

class AppState:
    running = True
    is_authenticated = False
    db_connection = None

app_state = AppState()
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
        print('[ERROR] failed connecting to db:', e)
        return None

    return connection

def close_database(app_state):
    if app_state.db_connection and app_state.db_connection.is_connected():
        app_state.db_connection.close()

def login():
    pass

def register():
    pass

def exit_func(app_state):
    app_state.running = False

def unauthenticated_menu():
    print('MENU')

    print('1. Login')
    print('2. Register')
    print('3. Exit')

    option = {
            '1': login,
            '2': register,
            '3': exit_func
    }

    return option

def prompt(option, app_state):
    o = input('>> ')

    func = option.get(o)
    if func:
        func(app_state)
    else:
        print('[WARNING] option is invalid')

if __name__ == '__main__':
    connection = connect_database()
    if not connection:
        app_state.running = False

    app_state.db_connection = connection # pyright: ignore

    option = {}
    while app_state.running:
        if not app_state.is_authenticated:
            option = unauthenticated_menu()

        prompt(option, app_state)

    close_database(app_state)
