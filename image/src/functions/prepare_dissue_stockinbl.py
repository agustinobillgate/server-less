from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_lieferant, L_artikel, L_op

def prepare_dissue_stockinbl():
    billdate = None
    q2_list_list = []
    htparam = l_lieferant = l_artikel = l_op = None

    q2_list = None

    q2_list_list, Q2_list = create_model("Q2_list", {"lief_nr":int, "docu_nr":str, "lscheinnr":str, "lager_nr":int, "artnr":int, "bezeich":str, "einzelpreis":decimal, "anzahl":decimal, "warenwert":decimal, "firma":str, "datum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, q2_list_list, htparam, l_lieferant, l_artikel, l_op


        nonlocal q2_list
        nonlocal q2_list_list
        return {"billdate": billdate, "q2-list": q2_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    l_op_obj_list = []
    for l_op, l_lieferant, l_artikel in db_session.query(L_op, L_lieferant, L_artikel).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_op.pos > 0) &  (L_op.op_art == 1)).filter(
            (L_op.docu_nr == L_op.lscheinnr) &  (L_op.datum == billdate) &  (L_op.loeschflag == 0) &  (L_op.flag) &  (L_op.pos >= 1)).all():
        if l_op._recid in l_op_obj_list:
            continue
        else:
            l_op_obj_list.append(l_op._recid)


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.lief_nr = l_op.lief_nr
        q2_list.docu_nr = l_op.docu_nr
        q2_list.lscheinnr = l_op.lscheinnr
        q2_list.lager_nr = l_op.lager_nr
        q2_list.artnr = l_artikel.artnr
        q2_list.bezeich = l_artikel.bezeich
        q2_list.einzelpreis = l_op.einzelpreis
        q2_list.anzahl = l_op.anzahl
        q2_list.warenwert = l_op.warenwert
        q2_list.firma = l_lieferant.firma
        q2_list.datum = l_op.datum

    return generate_output()