from common import BaseHandler, Option, ExitHandler, AppState
from helper import *

class ReadUserHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print_headline('ADMIN MENU | READ USER')

        cursor = app_state.db.cursor() 

        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()

        data = {
                'ID': list(map(lambda x: x[0], rows)),
                'Name': list(map(lambda x: x[1], rows)),
                'Username': list(map(lambda x: x[2], rows))
        }

        print_table_dataframe(data, 'User:')

class CheckoutReservationHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print_headline('ADMIN MENU | CHECKOUT RESERVATION')

        inp, err = validate_input([
            Input('reservation_id', 'int')
        ])

        if len(err) > 0:
            log_info('invalid input')
            return 

        cursor = app_state.db.cursor() 

        cursor.execute('SELECT * FROM reservations WHERE id = %s', (inp['reservation_id'],))
        rows = cursor.fetchone()

        if rows is None:
            log_info('invalid reservation id')
            return

        cursor.execute('DELETE FROM reservations WHERE id = %s', (inp['reservation_id'],))

        app_state.db.commit()

class CreateRoomHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print_headline('ADMIN MENU | CREATE ROOM')

        inp, err = validate_input([
            Input('public_id', 'any'),
            Input('capacity', 'int'),
            Input('price', 'int')
        ])

        if len(err) > 0:
            log_info('invalid input')
            return 

        cursor = app_state.db.cursor()

        cursor.execute('INSERT INTO rooms(public_id, capacity, price) VALUES(%s, %s, %s)', (inp['public_id'], inp['capacity'], inp['price']))

        app_state.db.commit()

class ReadRoomHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print_headline('ADMIN MENU | READ ROOM')

        cursor = app_state.db.cursor() 

        cursor.execute('SELECT * FROM rooms')
        rows = cursor.fetchall()

        data = {
                'ID': list(map(lambda x: x[0], rows)),
                'Public ID': list(map(lambda x: x[1], rows)),
                'Capacity': list(map(lambda x: x[2], rows)),
                'Price': list(map(lambda x: x[3], rows)),
        }

        print_table_dataframe(data, 'Room:')

class ReadReservationHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print_headline('ADMIN MENU | READ RESERVATION')

        cursor = app_state.db.cursor() 

        cursor.execute('SELECT * FROM reservations JOIN users ON reservations.user_id = users.id JOIN rooms ON reservations.room_id = rooms.id')
        rows = cursor.fetchall()

        data = {
                'ID': list(map(lambda x: x[0], rows)),
                'Room': list(map(lambda x: f'{x[9]} ({x[8]})', rows)),
                'Price': list(map(lambda x: x[11], rows)),
                'User': list(map(lambda x: f'{x[5]} ({x[6]})', rows)),
                'Day Count': list(map(lambda x: x[3], rows)),
                'Grand Total': list(map(lambda x: float(x[11]) * float(x[3]), rows)) # pyright: ignore
        }

        print_table_dataframe(data, 'Reservation:')

class AdminMenuHandler(BaseHandler):
    option = {
            '1': Option('Read User', ReadUserHandler()),
            '2': Option('Create Room', CreateRoomHandler()),
            '3': Option('Read Room', ReadRoomHandler()),
            '4': Option('Read Reservation', ReadReservationHandler()),
            '5': Option('Checkout Reservation', CheckoutReservationHandler()),
            '6': Option('Exit', ExitHandler())
    }

    def handle(self, _: AppState):
        print_headline('ADMIN MENU')

        print_option(self.option)

        return self.option
