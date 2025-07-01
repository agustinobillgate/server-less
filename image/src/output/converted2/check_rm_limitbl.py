#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Htparam

def check_rm_limitbl():

    prepare_cache ([Htparam])

    room_limit = 0
    curr_anz = 0
    zimmer = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_limit, curr_anz, zimmer, htparam

        return {"room_limit": room_limit, "curr_anz": curr_anz}

    def check_rm_limit():

        nonlocal room_limit, curr_anz, zimmer, htparam

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Zimmer)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if htparam.finteger > 0:
            room_limit = htparam.finteger
        curr_anz = 0

        for rbuff in db_session.query(Rbuff).order_by(Rbuff._recid).all():
            curr_anz = curr_anz + 1


    check_rm_limit()

    return generate_output()