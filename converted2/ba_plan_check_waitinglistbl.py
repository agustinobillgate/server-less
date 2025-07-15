#using conversion tools version: 1.0.0.27

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bk_veran, Guest, Bk_reser

def ba_plan_check_waitinglistbl(datum:date, raum:str, von_zeit:str, bis_zeit:str, resstatus:int):
    avail_resline = False
    q3_list_list = []
    bk_veran = guest = bk_reser = None

    q3_list = mainres = gast = resline = None

    q3_list_list, Q3_list = create_model("Q3_list", {"veran_nr":int, "name":str, "von_zeit":str, "bis_zeit":str, "raum":str, "rec_id":int})

    Mainres = create_buffer("Mainres",Bk_veran)
    Gast = create_buffer("Gast",Guest)
    Resline = create_buffer("Resline",Bk_reser)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_resline, q3_list_list, bk_veran, guest, bk_reser
        nonlocal datum, raum, von_zeit, bis_zeit, resstatus
        nonlocal mainres, gast, resline


        nonlocal q3_list, mainres, gast, resline
        nonlocal q3_list_list

        return {"avail_resline": avail_resline, "q3-list": q3_list_list}

    resline = db_session.query(Resline).filter(
             (Resline.datum == datum) & (func.lower(Resline.raum) == (raum).lower()) & (Resline.resstatus <= 2) & not_ (Resline.bis_zeit <= Resline.von_zeit) & not_ (Resline.von_zeit >= Resline.bis_zeit)).first()

    if resline:

        return generate_output()

    resline = db_session.query(Resline).filter(
             (Resline.datum == datum) & (func.lower(Resline.raum) == (raum).lower()) & (Resline.resstatus == 3) & not_ (Resline.bis_zeit <= Resline.von_zeit) & not_ (Resline.von_zeit >= Resline.bis_zeit)).first()

    if not resline:

        return generate_output()
    avail_resline = True

    resline_obj_list = []
    for resline, mainres, gast in db_session.query(Resline, Mainres, Gast).join(Mainres,(Mainres.veran_nr == Resline.veran_nr)).join(Gast,(Gast.gastnr == Mainres.gastnr)).filter(
             (Resline.datum == datum) & (func.lower(Resline.raum) == (raum).lower()) & (Resline.resstatus == 3) & not_ (Resline.bis_zeit <= Resline.von_zeit) & not_ (Resline.von_zeit >= Resline.bis_zeit)).order_by(Resline.veran_nr).all():
        if resline._recid in resline_obj_list:
            continue
        else:
            resline_obj_list.append(resline._recid)


        q3_list = Q3_list()
        q3_list_list.append(q3_list)

        q3_list.veran_nr = resline.veran_nr
        q3_list.name = gast.name
        q3_list.von_zeit = resline.von_zeit
        q3_list.bis_zeit = resline.bis_zeit
        q3_list.raum = resline.raum
        q3_list.rec_id = resline._recid

    return generate_output()