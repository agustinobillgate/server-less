#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def ba_plan_get_guestbl(t_gastnr:int):

    prepare_cache ([Guest])

    avail_guest = False
    guest_gastnr = 0
    recid_guest = 0
    guest_full_name = ""
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_guest, guest_gastnr, recid_guest, guest_full_name, guest
        nonlocal t_gastnr

        return {"avail_guest": avail_guest, "guest_gastnr": guest_gastnr, "recid_guest": recid_guest, "guest_full_name": guest_full_name}


    guest = get_cache (Guest, {"gastnr": [(eq, t_gastnr)]})

    if guest:
        avail_guest = True
        guest_gastnr = guest.gastnr
        recid_guest = guest._recid
        guest_full_name = guest.name + ", " + guest.vorname1 + " " +\
            guest.anrede1 + guest.anredefirma

    return generate_output()