#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_zimmerbl import read_zimmerbl
from models import Zimmer

def hk_lostfound_getroombl(zinr:string):
    msg_str = ""
    zimmer = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, zimmer
        nonlocal zinr


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        return {"zinr": zinr, "msg_str": msg_str}


    t_zimmer_list = get_output(read_zimmerbl(1, zinr, None, None))

    t_zimmer = query(t_zimmer_list, first=True)

    if not t_zimmer:
        msg_str = "No such Room Number."

        return generate_output()

    return generate_output()