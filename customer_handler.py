from common import BaseHandler, AppState, Option, ExitHandler
from helper import *
import pandas as pd

class MakeReservationHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print_headline('MENU | MAKE RESERVATION')

        cursor = app_state.db.cursor()

        cursor.execute('SELECT * FROM rooms WHERE id NOT IN (SELECT room_id FROM reservations)')
        rows = cursor.fetchall()

        data = {
                'id': list(map(lambda x: x[0], rows)),
                'public_id': list(map(lambda x: x[1], rows)),
                'bed_count': list(map(lambda x: x[2], rows)),
                'price': list(map(lambda x: x[3], rows))
        }

        df = pd.DataFrame(data)
        if len(df) < 1:
            log_info('no rooms avaiable', False)
            return

        print('Avaiable rooms:')
        print(df)
        print()

        inp, errors = validate_input([
            Input('room_id', 'int'),
            Input('day_count', 'int'),
        ])

        if len(errors) > 0:
            log_info('invalid input')
            return 

        cursor.execute('SELECT * FROM reservations WHERE room_id = %s', (inp['room_id'],)) 
        rows = cursor.fetchall()
        if len(rows) > 0:
            log_info('room is not avaiable')
            return

        assert app_state.user is not None

        cursor.execute('INSERT INTO reservations(room_id, user_id, day_count) VALUES(%s, %s, %s)', (inp['room_id'], app_state.user.id, inp['day_count']))

        app_state.db.commit()

        cursor.execute('SELECT * FROM reservations JOIN users ON reservations.user_id = users.id JOIN rooms ON reservations.room_id = rooms.id WHERE reservations.id = %s', (cursor.lastrowid,))
        rows = cursor.fetchone()

        assert rows is not None

        print()
        print('Invoice')
        print(f'Transaction ID: {rows[0]}')
        print(f'Room          : {rows[9]} ({rows[8]})')
        print(f'Price         : {rows[11]}')
        print(f'User          : {rows[5]} ({rows[6]})')
        print(f'Day Count     : {rows[3]}')
        print(f'Grand Total   : {rows[11]}x{rows[3]} = {float(rows[11]) * float(rows[3])}')

class VerifyReservationHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print('VERIFY RESERVATION')

        inp, errors = validate_input([
            Input('reservation_id', 'int'),
        ])

        if len(errors) > 0:
            print('Invalid input')
            return 

        cursor = app_state.db.cursor()

        cursor.execute('SELECT * FROM reservations WHERE id = %s', (inp['reservation_id'],))
        rows = cursor.fetchone()

        if rows is None:
            print('reservation invalid')
            return

        print('reservation is valid')

class MenuHandler(BaseHandler):
    option = {
            '1': Option('Make Reservation', MakeReservationHandler()),
            '2': Option('Verify Reservation', VerifyReservationHandler()),
            '3': Option('Exit', ExitHandler())
    }

    def handle(self, _: AppState):
        print_headline('MENU')

        print_option(self.option)

        return self.option
