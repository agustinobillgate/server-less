#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Zimkateg, Guest_pr

def prepare_update_restrictionbl():

    prepare_cache ([Queasy, Htparam, Zimkateg, Guest_pr])

    ci_date = None
    room_list_data = []
    ota_list_data = []
    rcode_list_data = []
    cat_flag:bool = False
    queasy = htparam = zimkateg = guest_pr = None

    room_list = ota_list = rcode_list = qsy = None

    room_list_data, Room_list = create_model("Room_list", {"bezeich":string})
    ota_list_data, Ota_list = create_model("Ota_list", {"bezeich":string})
    rcode_list_data, Rcode_list = create_model("Rcode_list", {"bezeich":string})

    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, room_list_data, ota_list_data, rcode_list_data, cat_flag, queasy, htparam, zimkateg, guest_pr
        nonlocal qsy


        nonlocal room_list, ota_list, rcode_list, qsy
        nonlocal room_list_data, ota_list_data, rcode_list_data

        return {"ci_date": ci_date, "room-list": room_list_data, "ota-list": ota_list_data, "rcode-list": rcode_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if cat_flag:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 152)).order_by(Queasy._recid).all():

            room_list = query(room_list_data, filters=(lambda room_list: room_list.bezeich == queasy.char1), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.bezeich = queasy.char1


    else:

        for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

            room_list = query(room_list_data, filters=(lambda room_list: room_list.bezeich == zimkateg.kurzbez), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.bezeich = zimkateg.kurzbez

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 159)).order_by(Queasy._recid).all():

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == queasy.number2)).order_by(Guest_pr._recid).all():

            qsy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

            if qsy:

                rcode_list = query(rcode_list_data, filters=(lambda rcode_list: rcode_list.bezeich == qsy.char1), first=True)

                if not rcode_list:
                    rcode_list = Rcode_list()
                    rcode_list_data.append(rcode_list)

                    rcode_list.bezeich = qsy.char1

    return generate_output()