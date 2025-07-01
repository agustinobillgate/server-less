#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_rart

def ba_npartikelbl(veran_nr:int, bill_date:date):
    bk_list_list = []
    bk_reser = bk_rart = None

    bk_list = None

    bk_list_list, Bk_list = create_model("Bk_list", {"datum":date, "raum":string, "veran_artnr":int, "bezeich":string, "anzahl":int, "preis":Decimal, "amount":Decimal, "von_zeit":string, "bis_zeit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_list_list, bk_reser, bk_rart
        nonlocal veran_nr, bill_date


        nonlocal bk_list
        nonlocal bk_list_list

        return {"bk-list": bk_list_list}

    bk_rart_obj_list = {}
    for bk_rart, bk_reser in db_session.query(Bk_rart, Bk_reser).join(Bk_reser,(Bk_reser.veran_nr == veran_nr) & (Bk_reser.veran_resnr == Bk_rart.veran_resnr) & (Bk_reser.resstatus == 1) & (Bk_reser.datum <= bill_date)).filter(
             (Bk_rart.veran_nr == veran_nr) & (Bk_rart.fakturiert == 0) & (Bk_rart.preis > 0)).order_by(Bk_reser.datum).all():
        if bk_rart_obj_list.get(bk_rart._recid):
            continue
        else:
            bk_rart_obj_list[bk_rart._recid] = True


        bk_list = Bk_list()
        bk_list_list.append(bk_list)

        buffer_copy(bk_rart, bk_list)

    return generate_output()