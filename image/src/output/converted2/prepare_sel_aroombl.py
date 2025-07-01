#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Zimmer, Res_line, Guest

def prepare_sel_aroombl():

    prepare_cache ([Htparam, Zimmer, Res_line, Guest])

    room_list = []
    ci_date:date = get_current_date()
    htparam = zimmer = res_line = guest = None

    room = None

    room_list, Room = create_model("Room", {"zinr":string, "gname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list, ci_date, htparam, zimmer, res_line, guest


        nonlocal room
        nonlocal room_list

        return {"room": room_list}

    def create_room1():

        nonlocal room_list, ci_date, htparam, zimmer, res_line, guest


        nonlocal room
        nonlocal room_list

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            room = Room()
            room_list.append(room)

            room.zinr = zimmer.zinr

            res_line = get_cache (Res_line, {"zinr": [(eq, zimmer.zinr)],"active_flag": [(eq, 1)],"resstatus": [(ne, 12)],"ankunft": [(le, ci_date)],"abreise": [(ge, ci_date)]})

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    room.gname = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam.fdate != None:
        ci_date = htparam.fdate
    create_room1()

    return generate_output()