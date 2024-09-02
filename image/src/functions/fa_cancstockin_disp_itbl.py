from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lieferant, Mathis, Fa_op

def fa_cancstockin_disp_itbl(from_date:date, to_date:date):
    q1_list_list = []
    l_lieferant = mathis = fa_op = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"lscheinnr":str, "name":str, "location":str, "einzelpreis":decimal, "anzahl":int, "warenwert":decimal, "firma":str, "datum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, l_lieferant, mathis, fa_op


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    fa_op_obj_list = []
    for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
            (Fa_op.datum >= from_date) &  (Fa_op.datum <= to_date) &  (Fa_op.loeschflag == 2)).all():
        if fa_op._recid in fa_op_obj_list:
            continue
        else:
            fa_op_obj_list.append(fa_op._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.lscheinnr = fa_op.lscheinnr
        q1_list.name = mathis.name
        q1_list.location = mathis.location
        q1_list.einzelpreis = fa_op.einzelpreis
        q1_list.anzahl = fa_op.anzahl
        q1_list.warenwert = fa_op.warenwert
        q1_list.firma = l_lieferant.firma
        q1_list.datum = fa_op.datum

    return generate_output()