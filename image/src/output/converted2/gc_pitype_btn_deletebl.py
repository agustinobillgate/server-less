from functions.additional_functions import *
import decimal
from models import Reservation, Gc_pitype

def gc_pitype_btn_deletebl(nr:int):
    success_flag = False
    reservation = gc_pitype = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, reservation, gc_pitype
        nonlocal nr


        return {"success_flag": success_flag}


    reservation = db_session.query(Reservation).filter(
             (Reservation.resart == nr)).first()

    if reservation:
        success_flag = False

        return generate_output()
    else:

        gc_pitype = db_session.query(Gc_pitype).filter(
                 (Gc_pitype.nr == nr)).first()
        db_session.delete(gc_pitype)
        success_flag = True

    return generate_output()