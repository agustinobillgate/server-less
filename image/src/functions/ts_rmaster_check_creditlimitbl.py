from functions.additional_functions import *
import decimal
from models import Htparam, Guest

def ts_rmaster_check_creditlimitbl(bill_gastnr:int):
    klimit = 0
    htparam = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, htparam, guest


        return {"klimit": klimit}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 68)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bill_gastnr)).first()

    if guest.kreditlimit != 0:
        klimit = guest.kreditlimit
    else:

        if htparam.fdecimal != 0:
            klimit = htparam.fdecimal
        else:
            klimit = htparam.finteger

    return generate_output()