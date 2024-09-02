from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Guest, Zimkateg

def bill_detailbl(resno:int, reslinno:int):
    b_detail_list = []
    nama:str = ""
    room:str = ""
    arr:date = ""
    dep:date = ""
    res_line = guest = zimkateg = None

    b_detail = None

    b_detail_list, B_detail = create_model("B_detail", {"resno":decimal, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "nama":str, "rt":str, "arg":str, "room":str, "arr":date, "dep":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_detail_list, nama, room, arr, dep, res_line, guest, zimkateg


        nonlocal b_detail
        nonlocal b_detail_list
        return {"b-detail": b_detail_list}


    b_detail_list.clear()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 12)).first()

    if res_line:
        arr = res_line.ankunf
        dep = res_line.abreise

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        if guest:
            nama = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            room = zimkateg.kurzbez
        b_detail = B_detail()
        b_detail_list.append(b_detail)

        b_detail.resno = res_line.resnr
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