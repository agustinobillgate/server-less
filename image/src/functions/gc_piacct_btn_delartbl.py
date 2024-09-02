from functions.additional_functions import *
import decimal
from models import Reservation, Gc_piacct

def gc_piacct_btn_delartbl(g_nr:int):
    flag = 0
    reservation = gc_piacct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, reservation, gc_piacct


        return {"flag": flag}


    reservation = db_session.query(Reservation).filter(
            (Reservation.resart == g_nr)).first()

    if reservation:
        flag = 1
    else:

        gc_piacct = db_session.query(Gc_piacct).filter(
                (Gc_piacct.nr == g_nr)).first()

        gc_piacct = db_session.query(Gc_piacct).first()
        db_session.delete(gc_piacct)


    return generate_output()