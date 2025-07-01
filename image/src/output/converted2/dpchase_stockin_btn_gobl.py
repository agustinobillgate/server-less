#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lieferant, L_artikel, L_op

def dpchase_stockin_btn_gobl():

    prepare_cache ([Htparam, L_lieferant, L_artikel, L_op])

    q2_list_list = []
    billdate:date = None
    heute:date = None
    beg_date:date = None
    htparam = l_lieferant = l_artikel = l_op = None

    q2_list = None

    q2_list_list, Q2_list = create_model("Q2_list", {"docu_nr":string, "lief_nr":int, "loeschflag":int, "lscheinnr":string, "lager_nr":int, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "anzahl":Decimal, "warenwert":Decimal, "firma":string, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_list, billdate, heute, beg_date, htparam, l_lieferant, l_artikel, l_op


        nonlocal q2_list
        nonlocal q2_list_list

        return {"q2-list": q2_list_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate
    heute = billdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    beg_date = date_mdy(get_month(htparam.fdate) , 1, get_year(htparam.fdate))

    l_op_obj_list = {}
    l_op = L_op()
    l_lieferant = L_lieferant()
    l_artikel = L_artikel()
    for l_op.docu_nr, l_op.lief_nr, l_op.loeschflag, l_op.lscheinnr, l_op.lager_nr, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.datum, l_op._recid, l_lieferant.firma, l_lieferant._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.docu_nr, L_op.lief_nr, L_op.loeschflag, L_op.lscheinnr, L_op.lager_nr, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.datum, L_op._recid, L_lieferant.firma, L_lieferant._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
             (L_op.docu_nr == L_op.lscheinnr) & (L_op.datum == billdate) & not_ (L_op.flag) & (L_op.op_art == 1) & (L_op.pos >= 1)).order_by(L_op.docu_nr).all():
        if l_op_obj_list.get(l_op._recid):
            continue
        else:
            l_op_obj_list[l_op._recid] = True


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.docu_nr = l_op.docu_nr
        q2_list.lief_nr = l_op.lief_nr
        q2_list.loeschflag = l_op.loeschflag
        q2_list.lscheinnr = l_op.lscheinnr
        q2_list.lager_nr = l_op.lager_nr
        q2_list.artnr = l_artikel.artnr
        q2_list.bezeich = l_artikel.bezeich
        q2_list.einzelpreis =  to_decimal(l_op.einzelpreis)
        q2_list.anzahl =  to_decimal(l_op.anzahl)
        q2_list.warenwert =  to_decimal(l_op.warenwert)
        q2_list.firma = l_lieferant.firma
        q2_list.datum = l_op.datum

    return generate_output()