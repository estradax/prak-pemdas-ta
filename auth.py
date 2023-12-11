from helper import *
from common import *

class LoginHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print('LOGIN')

        inp, errors = validate_input([
            Input('username', 'any'),
            Input('password', 'any'),
        ])

        if len(errors) > 0:
            print('Invalid input')
            return 

        cursor = app_state.db.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s', (inp['username'],))
        rows = cursor.fetchone()

        if rows is None:
            print('Invalid credentials')
            return

        if rows[3] != inp['password']:
            print('Invalid credentials')
            return           

        app_state.user = User(str(rows[1]), str(rows[2]), str(rows[3]))

class RegisterHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print('REGISTER')

        inp, errors = validate_input([
            Input('name', 'any'),
            Input('username', 'any'),
            Input('password', 'any'),
        ])

        if len(errors) > 0:
            print('Invalid input')
            return 
        
        cursor = app_state.db.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s', (inp['username'],))
        rows = cursor.fetchone()
        if rows is not None:
            print('User exists')
            return
        
        cursor.execute('INSERT INTO users(name, username, password) VALUES (%s, %s, %s)', (inp['name'], inp['username'], inp['password']))
        app_state.db.commit()

class AuthMenuHandler:
    option = {
            '1': Option('Login', LoginHandler()),
            '2': Option('Register', RegisterHandler()),
            '3': Option('Exit', ExitHandler())
    }

    def handle(self, _: AppState):
        print('AUTH MENU')

        print_option(self.option)

        return self.option
