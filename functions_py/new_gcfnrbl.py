#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def new_gcfnrbl():
    curr_gastnr = 0
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_gastnr, guest

        return {"curr_gastnr": curr_gastnr}

    curr_gastnr = 0

    guest = db_session.query(Guest).filter(
             (Guest.gastnr < 0)).first()

    if guest:
        curr_gastnr = - guest.gastnr

        db_session.refresh(guest, with_for_update=True)
        db_session.delete(guest)
        db_session.flush()

        guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)]})

        if guest:
            curr_gastnr = 0

    if curr_gastnr == 0:

        guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

        if guest:
            curr_gastnr = guest.gastnr + 1
        else:
            curr_gastnr = 1

    return generate_output()