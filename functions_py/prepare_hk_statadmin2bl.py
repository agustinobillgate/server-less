# using conversion tools version: 1.0.0.117
"""_yusufwijasena_20/11/2025
        _remark_:   - fix room number not found, add new condition + log message
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Htparam


def prepare_hk_statadmin2bl(b_zinr: string):

    prepare_cache([Zimmer, Htparam])

    from_date = None
    zinr = ""
    zimmer = htparam = None

    room = None

    Room = create_buffer("Room", Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, zinr, zimmer, htparam
        nonlocal b_zinr
        nonlocal room

        return {"from_date": from_date, "zinr": zinr}

    room = get_cache(Zimmer, {"zinr": [(eq, b_zinr)]})
    # fix: if when room number not found
    if room:
        zinr = room.zinr
    else:
        print("LOG: room number not found!")

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})
    from_date = htparam.fdate

    return generate_output()
