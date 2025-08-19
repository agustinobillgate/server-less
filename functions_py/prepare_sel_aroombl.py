#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Zimmer, Res_line, Guest

def prepare_sel_aroombl():

    prepare_cache ([Htparam, Zimmer, Res_line, Guest])

    room_data = []
    ci_date:date = get_current_date()
    htparam = zimmer = res_line = guest = None

    room = None

    room_data, Room = create_model("Room", {"zinr":string, "gname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_data, ci_date, htparam, zimmer, res_line, guest


        nonlocal room
        nonlocal room_data

        return {"room": room_data}

    def create_room1():

        nonlocal room_data, ci_date, htparam, zimmer, res_line, guest
        nonlocal room

        for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():
            room = Room()
            room_data.append(room)

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