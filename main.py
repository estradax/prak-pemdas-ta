import mysql.connector
from common import *
from auth import *
from customer_handler import *
from admin import AdminMenuHandler

class Application:
    def __init__(self, app_state: AppState):
        self.app_state = app_state

        self.auth_menu_handler = AuthMenuHandler()
        self.menu_handler = MenuHandler()
        self.admin_menu_handler = AdminMenuHandler()

    def run(self):
        option = {}
        while self.app_state.running:
            if not self.app_state.user:
                option = self.auth_menu_handler.handle(self.app_state)
            else:
                if self.app_state.user.username == 'admin':
                    option = self.admin_menu_handler.handle(self.app_state)
                else:
                    option = self.menu_handler.handle(self.app_state)

            if self.app_state.user:
                x = input(f'{self.app_state.user.name}>> ')
            else:
                x = input('>> ')

            func = option.get(x)
            if func:
                func.handler.handle(self.app_state)
            else:
               log_info('invalid input') 
            
if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(**{
            'host': '127.0.0.1',
            'user': 'root',
            'password': '12345678',
            'database': 'pemdas_tugas_akhir'
        })
    except mysql.connector.Error as e:
        print('failed connect to database', e)
        exit(1)

    app_state = AppState(connection)

    app = Application(app_state)
    app.run()
