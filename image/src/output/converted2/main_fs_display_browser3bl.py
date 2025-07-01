#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_veran, Bk_func

def main_fs_display_browser3bl(b1_resnr:int, b1_resline:int, show_all:bool, rsvsort:int, recid_bk_veran:int):

    prepare_cache ([Bk_reser, Bk_veran, Bk_func])

    q3_list_list = []
    bk_reser = bk_veran = bk_func = None

    bk_rsv = q3_list = None

    q3_list_list, Q3_list = create_model("Q3_list", {"bk_func_recid":int, "bk_rsv_recid":int, "veran_seite":int, "veran_resnr":int, "raum":string, "datum":date, "bis_datum":date, "resstatus":int, "kartentext":[string,8], "sonstiges":[string,8], "veran_nr":int, "von_zeit":string, "bis_zeit":string})

    Bk_rsv = create_buffer("Bk_rsv",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q3_list_list, bk_reser, bk_veran, bk_func
        nonlocal b1_resnr, b1_resline, show_all, rsvsort, recid_bk_veran
        nonlocal bk_rsv


        nonlocal bk_rsv, q3_list
        nonlocal q3_list_list

        return {"q3-list": q3_list_list}

    def create_q3_list():

        nonlocal q3_list_list, bk_reser, bk_veran, bk_func
        nonlocal b1_resnr, b1_resline, show_all, rsvsort, recid_bk_veran
        nonlocal bk_rsv


        nonlocal bk_rsv, q3_list
        nonlocal q3_list_list

        i:int = 0
        q3_list = Q3_list()
        q3_list_list.append(q3_list)

        q3_list.bk_func_recid = bk_func._recid
        q3_list.bk_rsv_recid = bk_rsv._recid
        q3_list.veran_seite = bk_rsv.veran_seite
        q3_list.veran_resnr = bk_rsv.veran_resnr
        q3_list.raum = bk_rsv.raum
        q3_list.datum = bk_func.datum
        q3_list.bis_datum = bk_func.bis_datum
        q3_list.resstatus = bk_func.resstatus
        q3_list.veran_nr = bk_func.veran_nr
        q3_list.von_zeit = bk_rsv.von_zeit
        q3_list.bis_zeit = bk_rsv.bis_zeit


        for i in range(1,8 + 1) :
            q3_list.kartentext[i - 1] = bk_func.kartentext[i - 1]
            q3_list.sonstiges[i - 1] = bk_func.sonstiges[i - 1]


    bk_veran = get_cache (Bk_veran, {"_recid": [(eq, recid_bk_veran)]})

    if b1_resnr != 0 and not show_all:

        bk_func_obj_list = {}
        bk_func = Bk_func()
        bk_rsv = Bk_reser()
        for bk_func._recid, bk_func.datum, bk_func.bis_datum, bk_func.resstatus, bk_func.veran_nr, bk_func.kartentext, bk_func.sonstiges, bk_rsv._recid, bk_rsv.veran_seite, bk_rsv.veran_resnr, bk_rsv.raum, bk_rsv.von_zeit, bk_rsv.bis_zeit in db_session.query(Bk_func._recid, Bk_func.datum, Bk_func.bis_datum, Bk_func.resstatus, Bk_func.veran_nr, Bk_func.kartentext, Bk_func.sonstiges, Bk_rsv._recid, Bk_rsv.veran_seite, Bk_rsv.veran_resnr, Bk_rsv.raum, Bk_rsv.von_zeit, Bk_rsv.bis_zeit).join(Bk_rsv,(Bk_rsv.veran_nr == Bk_func.veran_nr) & (Bk_rsv.veran_resnr == Bk_func.veran_seite)).filter(
                 (Bk_func.veran_nr == b1_resnr) & (Bk_func.veran_seite == b1_resline)).order_by(Bk_rsv.veran_resnr).all():
            if bk_func_obj_list.get(bk_func._recid):
                continue
            else:
                bk_func_obj_list[bk_func._recid] = True


            create_q3_list()

    elif b1_resnr != 0 and show_all:

        bk_func_obj_list = {}
        bk_func = Bk_func()
        bk_rsv = Bk_reser()
        for bk_func._recid, bk_func.datum, bk_func.bis_datum, bk_func.resstatus, bk_func.veran_nr, bk_func.kartentext, bk_func.sonstiges, bk_rsv._recid, bk_rsv.veran_seite, bk_rsv.veran_resnr, bk_rsv.raum, bk_rsv.von_zeit, bk_rsv.bis_zeit in db_session.query(Bk_func._recid, Bk_func.datum, Bk_func.bis_datum, Bk_func.resstatus, Bk_func.veran_nr, Bk_func.kartentext, Bk_func.sonstiges, Bk_rsv._recid, Bk_rsv.veran_seite, Bk_rsv.veran_resnr, Bk_rsv.raum, Bk_rsv.von_zeit, Bk_rsv.bis_zeit).join(Bk_rsv,(Bk_rsv.veran_nr == Bk_func.veran_nr) & (Bk_rsv.veran_resnr == Bk_func.veran_seite)).filter(
                 (Bk_func.veran_nr == b1_resnr) & (Bk_func.resstatus == rsvsort)).order_by(Bk_rsv.veran_resnr).all():
            if bk_func_obj_list.get(bk_func._recid):
                continue
            else:
                bk_func_obj_list[bk_func._recid] = True


            create_q3_list()
    else:

        bk_func_obj_list = {}
        bk_func = Bk_func()
        bk_rsv = Bk_reser()
        for bk_func._recid, bk_func.datum, bk_func.bis_datum, bk_func.resstatus, bk_func.veran_nr, bk_func.kartentext, bk_func.sonstiges, bk_rsv._recid, bk_rsv.veran_seite, bk_rsv.veran_resnr, bk_rsv.raum, bk_rsv.von_zeit, bk_rsv.bis_zeit in db_session.query(Bk_func._recid, Bk_func.datum, Bk_func.bis_datum, Bk_func.resstatus, Bk_func.veran_nr, Bk_func.kartentext, Bk_func.sonstiges, Bk_rsv._recid, Bk_rsv.veran_seite, Bk_rsv.veran_resnr, Bk_rsv.raum, Bk_rsv.von_zeit, Bk_rsv.bis_zeit).join(Bk_rsv,(Bk_rsv.veran_nr == Bk_func.veran_nr) & (Bk_rsv.veran_resnr == Bk_func.veran_seite)).filter(
                 (Bk_func.veran_nr == bk_veran.veran_nr) & (Bk_func.resstatus == rsvsort)).order_by(Bk_rsv.veran_resnr).all():
            if bk_func_obj_list.get(bk_func._recid):
                continue
            else:
                bk_func_obj_list[bk_func._recid] = True


            create_q3_list()

    return generate_output()