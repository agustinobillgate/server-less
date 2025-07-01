#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Artikel

def check_rpaymentbl(pvilanguage:int, gastnr:int, dept:int):

    prepare_cache ([Guest, Artikel])

    zahlungsart = 0
    msg_str = ""
    lvcarea:string = "check-rpayment"
    guest = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zahlungsart, msg_str, lvcarea, guest, artikel
        nonlocal pvilanguage, gastnr, dept

        return {"zahlungsart": zahlungsart, "msg_str": msg_str}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        zahlungsart = guest.zahlungsart

    if zahlungsart == 0:
        msg_str = translateExtended ("No C/L Payment Articles defined for this Guest.", lvcarea, "")
    else:

        artikel = get_cache (Artikel, {"artnr": [(eq, zahlungsart)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 2:
            msg_str = translateExtended ("No C/L Payment Articles defined for this Guest.", lvcarea, "")
            zahlungsart = 0

    return generate_output()