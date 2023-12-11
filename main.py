from database import *

running = True
is_authenticated = False
connection = None
current_user = None

def login():
    global is_authenticated
    global current_user

    assert connection is not None

    username = input('username: ')
    password = input('password: ')

    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    rows = cursor.fetchone()

    if not rows:
        print('[INFO] credentials is invalid')
        return

    if rows[2] != password:
        print('[INFO] credentials is invalid')
        return

    is_authenticated = True

    current_user = {
            'id': rows[0],
            'username': rows[1],
            'password': rows[2]
    }

    print('[INFO] succesfully authenticated')

def register():
    pass

def exit_func():
    global running
    running = False

def auth_menu():
    print('AUTH MENU')

    print('1. Login')
    print('2. Register')
    print('3. Exit')

    opt = {
            '1': login,
            '2': register,
            '3': exit_func
    }

    return opt

def logout():
    global is_authenticated
    global current_user

    is_authenticated = False
    current_user = None

def menu():
    print('MAIN MENU')

    print('1. Logout')

    opt = {
            '1': logout
    }

    return opt

def prompt(option):
    if current_user is not None:
        x = input(f'{current_user["username"]}>> ')
    else:
        x = input('>> ')
    
    func = option.get(x)
    if func:
        func()
    else:
        print('[INFO] invalid input')

def main():
    global running
    global connection

    connection = connect_database()
    if not connection:
        running = False

    option = {}

    while running:
        if not is_authenticated:
            option = auth_menu()
        else:
            option = menu()

        prompt(option)

    close_database(connection)

if __name__ == '__main__':
    main()
