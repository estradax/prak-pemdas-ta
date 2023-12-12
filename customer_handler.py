from common import BaseHandler, AppState, Option, ExitHandler
from helper import *

class MakeReservationHandler(BaseHandler):
    def handle(self, app_state: AppState):
        print('MAKE RESERVATION')
        
        inp, errors = validate_input([
            Input('room_id', 'int'),
            Input('day_count', 'int'),
        ])

        if len(errors) > 0:
            print('Invalid input')
            return 

        assert app_state.user is not None

        cursor = app_state.db.cursor()

        cursor.execute('INSERT INTO reservations(room_id, user_id, day_count) VALUES(%s, %s, %s)', (inp['room_id'], app_state.user.id, inp['day_count']))

        app_state.db.commit()

class VerifyReservationHandler(BaseHandler):
    def handle(self, _: AppState):
        print('VERIFY RESERVATION')

        return super().handle(_)

class MenuHandler(BaseHandler):
    option = {
            '1': Option('Make Reservation', MakeReservationHandler()),
            '2': Option('Verify Reservation', VerifyReservationHandler()),
            '3': Option('Exit', ExitHandler())
    }

    def handle(self, _: AppState):
        print('MENU')

        print_option(self.option)

        return self.option
