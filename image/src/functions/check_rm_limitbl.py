from functions.additional_functions import *
import decimal
from models import Zimmer, Htparam

def check_rm_limitbl():
    room_limit = 0
    curr_anz = 0
    zimmer = htparam = None

    rbuff = None

    Rbuff = Zimmer

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_limit, curr_anz, zimmer, htparam
        nonlocal rbuff


        nonlocal rbuff
        return {"room_limit": room_limit, "curr_anz": curr_anz}

    def check_rm_limit():

        nonlocal room_limit, curr_anz, zimmer, htparam
        nonlocal rbuff


        nonlocal rbuff


        Rbuff = Zimmer

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 975)).first()

        if htparam.finteger > 0:
            room_limit = htparam.finteger
        curr_anz = 0

        for rbuff in db_session.query(Rbuff).all():
            curr_anz = curr_anz + 1

    check_rm_limit()

    return generate_output()