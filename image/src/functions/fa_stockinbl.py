from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_lieferant, Mathis, Fa_op

def fa_stockinbl(ponum:str, billdate:date, todate:date):
    q2_list_list = []
    l_lieferant = mathis = fa_op = None

    q2_list = None

    q2_list_list, Q2_list = create_model("Q2_list", {"lscheinnr":str, "name":str, "location":str, "einzelpreis":decimal, "anzahl":int, "warenwert":decimal, "firma":str, "datum":date, "docu_nr":str, "lief_nr":int, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_list, l_lieferant, mathis, fa_op


        nonlocal q2_list
        nonlocal q2_list_list
        return {"q2-list": q2_list_list}

    if ponum == "":

        fa_op_obj_list = []
        for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                (Fa_op.opart == 1) &  (func.lower(Fa_op.lscheinnr) >= (ponum).lower()) &  (Fa_op.datum >= billdate) &  (Fa_op.datum <= todate) &  (Fa_op.loeschflag <= 1)).all():
            if fa_op._recid in fa_op_obj_list:
                continue
            else:
                fa_op_obj_list.append(fa_op._recid)


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.lscheinnr = fa_op.lscheinnr
            q2_list.name = mathis.name
            q2_list.location = mathis.location
            q2_list.einzelpreis = fa_op.einzelpreis
            q2_list.anzahl = fa_op.anzahl
            q2_list.warenwert = fa_op.warenwert
            q2_list.firma = l_lieferant.firma
            q2_list.datum = fa_op.datum
            q2_list.docu_nr = fa_op.docu_nr
            q2_list.lief_nr = fa_op.lief_nr
            q2_list.rec_id = fa_op._recid


    else:

        fa_op_obj_list = []
        for fa_op, l_lieferant, mathis in db_session.query(Fa_op, L_lieferant, Mathis).join(L_lieferant,(L_lieferant.lief_nr == Fa_op.lief_nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                (Fa_op.opart == 1) &  (func.lower(Fa_op.lscheinnr) == (ponum).lower()) &  (Fa_op.datum >= billdate) &  (Fa_op.datum <= todate) &  (Fa_op.loeschflag <= 1)).all():
            if fa_op._recid in fa_op_obj_list:
                continue
            else:
                fa_op_obj_list.append(fa_op._recid)


            q2_list = Q2_list()
            q2_list_list.append(q2_list)

            q2_list.lscheinnr = fa_op.lscheinnr
            q2_list.name = mathis.name
            q2_list.location = mathis.location
            q2_list.einzelpreis = fa_op.einzelpreis
            q2_list.anzahl = fa_op.anzahl
            q2_list.warenwert = fa_op.warenwert
            q2_list.firma = l_lieferant.firma
            q2_list.datum = fa_op.datum
            q2_list.docu_nr = fa_op.docu_nr
            q2_list.lief_nr = fa_op.lief_nr
            q2_list.rec_id = fa_op._recid

    return generate_output()