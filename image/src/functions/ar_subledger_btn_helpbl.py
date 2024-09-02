from functions.additional_functions import *
import decimal
from models import Guest

def ar_subledger_btn_helpbl(gastno:int):
    guest_name = ""
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, guest


        return {"guest_name": guest_name}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()
    guest_name = guest.name

    return generate_output()