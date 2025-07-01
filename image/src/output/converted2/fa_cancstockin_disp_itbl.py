#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Mathis, Fa_op

def fa_cancstockin_disp_itbl(from_date:date, to_date:date):

    prepare_cache ([L_lieferant, Mathis, Fa_op])

    q1_list_list = []
    l_lieferant = mathis = fa_op = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"lscheinnr":string, "name":string, "location":string, "einzelpreis":Decimal, "anzahl":int, "warenwert":Decimal, "firma":string, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, l_lieferant, mathis, fa_op
        nonlocal from_date, to_date


        nonlocal q1_list
        nonlocal q1_list_list

        return {"q1-list": q1_list_list}

    fa_op_obj_list = {}
    fa_op = Fa_op()
    l_lieferant = L_lieferant()
    mathis = Mathis()
    for fa_op.lscheinnr, fa_op.einzelpreis, fa_op.anzahl, fa_op.warenwert, fa_op.datum, fa_op._recid, l_lieferant.firma, l_lieferant._recid, mathis.name, mathis.location, mathis._recid in db_session.query(Fa_op.lscheinnr, Fa_op.einzelpreis, Fa_op.anzahl, Fa_op.warenwert, Fa_op.datum, Fa_op._recid, L_lieferant.firma, L_lieferant._recid, Mathis.name, Mathis.location, Mathis._recid).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
             (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date) & (Fa_op.loeschflag == 2)).order_by(Fa_op.docu_nr).all():
        if fa_op_obj_list.get(fa_op._recid):
            continue
        else:
            fa_op_obj_list[fa_op._recid] = True


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.lscheinnr = fa_op.lscheinnr
        q1_list.name = mathis.name
        q1_list.location = mathis.location
        q1_list.einzelpreis =  to_decimal(fa_op.einzelpreis)
        q1_list.anzahl = fa_op.anzahl
        q1_list.warenwert =  to_decimal(fa_op.warenwert)
        q1_list.firma = l_lieferant.firma
        q1_list.datum = fa_op.datum

    return generate_output()