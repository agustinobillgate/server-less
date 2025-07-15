#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_roomplan_create_browsebl import hk_roomplan_create_browsebl
from models import Htparam

def prepare_hk_roomplanbl(from_room:string):

    prepare_cache ([Htparam])

    curr_date = None
    room_list_data = []
    htparam = None

    room_list = None

    room_list_data, Room_list = create_model("Room_list", {"zistatus":int, "ststr":string, "build":string, "build_flag":string, "recid1":[int,17], "etage":int, "zinr":string, "c_char":string, "i_char":string, "zikatnr":int, "rmcat":string, "connec":string, "avtoday":string, "gstatus":[int,17], "bcol":[int,17], "fcol":[int,17], "room":[string,17]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, room_list_data, htparam
        nonlocal from_room


        nonlocal room_list
        nonlocal room_list_data

        return {"curr_date": curr_date, "room-list": room_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate
    room_list_data = get_output(hk_roomplan_create_browsebl(False, from_room, curr_date, curr_date))

    return generate_output()