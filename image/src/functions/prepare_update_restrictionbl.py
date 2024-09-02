from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam, Zimkateg, Guest_pr, Guest

def prepare_update_restrictionbl():
    ci_date = None
    room_list_list = []
    ota_list_list = []
    rcode_list_list = []
    cat_flag:bool = False
    queasy = htparam = zimkateg = guest_pr = guest = None

    room_list = ota_list = rcode_list = qsy = None

    room_list_list, Room_list = create_model("Room_list", {"bezeich":str})
    ota_list_list, Ota_list = create_model("Ota_list", {"bezeich":str})
    rcode_list_list, Rcode_list = create_model("Rcode_list", {"bezeich":str})

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, room_list_list, ota_list_list, rcode_list_list, cat_flag, queasy, htparam, zimkateg, guest_pr, guest
        nonlocal qsy


        nonlocal room_list, ota_list, rcode_list, qsy
        nonlocal room_list_list, ota_list_list, rcode_list_list
        return {"ci_date": ci_date, "room-list": room_list_list, "ota-list": ota_list_list, "rcode-list": rcode_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()

    if htparam:
        ci_date = htparam.fdate

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    if cat_flag:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 152)).all():

            room_list = query(room_list_list, filters=(lambda room_list :room_list.bezeich == queasy.char1), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.bezeich = queasy.char1


    else:

        for zimkateg in db_session.query(Zimkateg).all():

            room_list = query(room_list_list, filters=(lambda room_list :room_list.bezeich == zimkateg.kurzbez), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.bezeich = zimkateg.kurzbez

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 159)).all():

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == queasy.number2)).all():

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 2) &  (Qsy.char1 == guest_pr.CODE)).first()

            if qsy:

                rcode_list = query(rcode_list_list, filters=(lambda rcode_list :rcode_list.bezeich == qsy.char1), first=True)

                if not rcode_list:
                    rcode_list = Rcode_list()
                    rcode_list_list.append(rcode_list)

                    rcode_list.bezeich = qsy.char1

    for guest in db_session.query(Guest).filter(
            (Guest.karteityp == 2) &  (Guest.steuernr != "")).all():

        ota_list = query(ota_list_list, filters=(lambda ota_list :ota_list.bezeich == trim(entry(0, guest.steuernr, "|"))), first=True)

        if not ota_list:
            ota_list = Ota_list()
            ota_list_list.append(ota_list)

            ota_list.bezeich = trim(entry(0, guest.steuernr, "|"))

    return generate_output()