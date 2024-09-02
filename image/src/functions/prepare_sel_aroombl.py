from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Zimmer, Res_line, Guest

def prepare_sel_aroombl():
    room_list = []
    ci_date:date = get_current_date()
    htparam = zimmer = res_line = guest = None

    room = None

    room_list, Room = create_model("Room", {"zinr":str, "gname":str})


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

        for zimmer in db_session.query(Zimmer).all():
            room = Room()
            room_list.append(room)

            room.zinr = zimmer.zinr

            res_line = db_session.query(Res_line).filter(
                    (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus != 12) &  (Res_line.ankunft <= ci_date) &  (Res_line.abreise >= ci_date)).first()

            if res_line:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

                if guest:
                    room.gname = guest.name + " " + guest.vorname1 + ", " + guest.anrede1 + guest.anredefirma

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()

    if htparam.fdate != None:
        ci_date = htparam.fdate
    create_room1()

    return generate_output()