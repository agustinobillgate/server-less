from functions.additional_functions import *
import decimal
from models import Guest, Artikel

def check_rpaymentbl(pvilanguage:int, gastnr:int, dept:int):
    zahlungsart = 0
    msg_str = ""
    lvcarea:str = "check-rpayment"
    guest = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zahlungsart, msg_str, lvcarea, guest, artikel
        nonlocal pvilanguage, gastnr, dept


        return {"zahlungsart": zahlungsart, "msg_str": msg_str}


    guest = db_session.query(Guest).filter(
             (Guest.gastnr == gastnr)).first()

    if guest:
        zahlungsart = guest.zahlungsart

    if zahlungsart == 0:
        msg_str = translateExtended ("No C/L Payment Articles defined for this Guest.", lvcarea, "")
    else:

        artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == zahlungsart) & (Artikel.departement == 0)).first()

        if not artikel or artikel.artart != 2:
            msg_str = translateExtended ("No C/L Payment Articles defined for this Guest.", lvcarea, "")
            zahlungsart = 0

    return generate_output()