from functions.additional_functions import *
import decimal
from datetime import date
from functions.hk_roomplan_create_browsebl import hk_roomplan_create_browsebl
from models import Htparam

def prepare_hk_roomplanbl(from_room:str):
    curr_date = None
    room_list_list = []
    htparam = None

    room_list = None

    room_list_list, Room_list = create_model("Room_list", {"zistatus":int, "ststr":str, "build":str, "build_flag":str, "recid1":[int, 17], "etage":int, "zinr":str, "c_char":str, "i_char":str, "zikatnr":int, "rmcat":str, "connec":str, "avtoday":str, "gstatus":[int, 17], "bcol":[int, 17], "fcol":[int, 17], "room":[str, 17]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, room_list_list, htparam


        nonlocal room_list
        nonlocal room_list_list
        return {"curr_date": curr_date, "room-list": room_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    curr_date = htparam.fdate
    room_list_list = get_output(hk_roomplan_create_browsebl(False, from_room, curr_date, curr_date))

    return generate_output()