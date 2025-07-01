#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Guest, Bk_veran

def main_fs_display_browser2bl(b1_resnr:int, glist_gastnr:int, rsvsort:int, guestsort:int, to_date:date):

    prepare_cache ([Bk_veran])

    bq_rechnr = 0
    q2_list_list = []
    bk_reser = guest = bk_veran = None

    q2_list = bkres_buff = bkgast = None

    q2_list_list, Q2_list = create_model("Q2_list", {"rechnr":int, "bk_veran_recid":int, "resstatus":int, "veran_nr":int, "anlass":string})

    Bkres_buff = create_buffer("Bkres_buff",Bk_reser)
    Bkgast = create_buffer("Bkgast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bq_rechnr, q2_list_list, bk_reser, guest, bk_veran
        nonlocal b1_resnr, glist_gastnr, rsvsort, guestsort, to_date
        nonlocal bkres_buff, bkgast


        nonlocal q2_list, bkres_buff, bkgast
        nonlocal q2_list_list

        return {"bq_rechnr": bq_rechnr, "q2-list": q2_list_list}

    def create_q2_list():

        nonlocal bq_rechnr, q2_list_list, bk_reser, guest, bk_veran
        nonlocal b1_resnr, glist_gastnr, rsvsort, guestsort, to_date
        nonlocal bkres_buff, bkgast


        nonlocal q2_list, bkres_buff, bkgast
        nonlocal q2_list_list


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.rechnr = bk_veran.rechnr
        q2_list.bk_veran_recid = bk_veran._recid
        q2_list.resstatus = bk_veran.resstatus
        q2_list.veran_nr = bk_veran.veran_nr
        q2_list.anlass = bk_veran.anlass


    if b1_resnr != 0:

        bk_veran_obj_list = {}
        for bk_veran, bkres_buff, bkgast in db_session.query(Bk_veran, Bkres_buff, Bkgast).join(Bkres_buff,(Bkres_buff.veran_nr == Bk_veran.veran_nr) & (Bkres_buff.resstatus == rsvsort)).join(Bkgast,(Bkgast.gastnr == Bk_veran.gastnr) & (Bkgast.karteityp == guestsort)).filter(
                 (Bk_veran.gastnr == glist_gastnr) & (Bk_veran.activeflag == 0) & (Bk_veran.veran_nr == b1_resnr)).order_by(Bk_veran.veran_nr).all():
            if bk_veran_obj_list.get(bk_veran._recid):
                continue
            else:
                bk_veran_obj_list[bk_veran._recid] = True


            create_q2_list()

    else:

        bk_veran_obj_list = {}
        for bk_veran, bkres_buff, bkgast in db_session.query(Bk_veran, Bkres_buff, Bkgast).join(Bkres_buff,(Bkres_buff.veran_nr == Bk_veran.veran_nr) & (Bkres_buff.resstatus == rsvsort)).join(Bkgast,(Bkgast.gastnr == Bk_veran.gastnr) & (Bkgast.karteityp == guestsort)).filter(
                 (Bk_veran.gastnr == glist_gastnr) & (Bk_veran.activeflag == 0) & (Bk_veran.limit_date <= to_date)).order_by(Bk_veran.veran_nr).all():
            if bk_veran_obj_list.get(bk_veran._recid):
                continue
            else:
                bk_veran_obj_list[bk_veran._recid] = True


            create_q2_list()


    if bk_veran:
        bq_rechnr = bk_veran.rechnr

    return generate_output()