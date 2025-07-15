#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_func, Bk_raum

def prepare_copy_bares_webbl(resnr:int, reslinnr:int):

    prepare_cache ([Bk_reser, Bk_func, Bk_raum])

    datum = None
    ftime = ""
    ttime = ""
    from_date = None
    to_date = None
    gname = ""
    raum = ""
    raum1 = ""
    statsort = 0
    room_list_data = []
    bk_reser = bk_func = bk_raum = None

    room_list = None

    room_list_data, Room_list = create_model("Room_list", {"room_id":string, "room_name":string, "prep_time":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, ftime, ttime, from_date, to_date, gname, raum, raum1, statsort, room_list_data, bk_reser, bk_func, bk_raum
        nonlocal resnr, reslinnr


        nonlocal room_list
        nonlocal room_list_data

        return {"datum": datum, "ftime": ftime, "ttime": ttime, "from_date": from_date, "to_date": to_date, "gname": gname, "raum": raum, "raum1": raum1, "statsort": statsort, "room-list": room_list_data}

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, reslinnr)]})

    if bk_reser:

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, reslinnr)]})

        if bk_func:
            statsort = bk_reser.resstatus

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

        if bk_raum:
            datum = bk_reser.datum
            ftime = bk_reser.von_zeit
            ttime = bk_reser.bis_zeit
            raum = bk_raum.bezeich
            raum1 = bk_raum.raum
            from_date = datum + timedelta(days=1)
            to_date = from_date
            gname = bk_func.bestellt__durch

            for bk_raum in db_session.query(Bk_raum).order_by(Bk_raum._recid).all():
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.room_id = bk_raum.raum
                room_list.room_name = bk_raum.bezeich
                room_list.prep_time = bk_raum.vorbereit

    return generate_output()