#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Zimkateg

def bill_detailbl(resno:int, reslinno:int):

    prepare_cache ([Res_line, Guest, Zimkateg])

    b_detail_data = []
    nama:string = ""
    room:string = ""
    arr:date = ""
    dep:date = ""
    res_line = guest = zimkateg = None

    b_detail = None

    b_detail_data, B_detail = create_model("B_detail", {"resno":Decimal, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "nama":string, "rt":string, "arg":string, "room":string, "arr":date, "dep":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_detail_data, nama, room, arr, dep, res_line, guest, zimkateg
        nonlocal resno, reslinno


        nonlocal b_detail
        nonlocal b_detail_data

        return {"b-detail": b_detail_data}


    b_detail_data.clear()

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"resstatus": [(ne, 9),(ne, 12)]})

    if res_line:
        arr = res_line.ankunft
        dep = res_line.abreise

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            nama = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            room = zimkateg.kurzbez
        b_detail = B_detail()
        b_detail_data.append(b_detail)

        b_detail.resno =  to_decimal(res_line.resnr)
        b_detail.nama = nama
        b_detail.room = res_line.zinr
        b_detail.rt = room
        b_detail.arr = arr
        b_detail.dep = dep
        b_detail.kind1 = res_line.kind1
        b_detail.kind2 = res_line.kind2
        b_detail.erwachs = res_line.erwachs
        b_detail.arg = res_line.arrangement

    return generate_output()