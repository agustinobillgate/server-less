from functions.additional_functions import *
import decimal
from models import Guest

def mk_aktline_btn_help2_1bl(akt_line1_gastnr:int):
    avail_guest = False
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_guest, guest


        return {"avail_guest": avail_guest}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == akt_line1_gastnr)).first()

    if not guest:
        pass
    else:
        avail_guest = True

    return generate_output()