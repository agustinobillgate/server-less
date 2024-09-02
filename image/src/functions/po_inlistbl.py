from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_lieferant, L_artikel

def po_inlistbl(lief_nr:int, docu_nr:str, from_date:date, to_date:date):
    l_lieferant_firma = ""
    t_l_op_list = []
    l_op = l_lieferant = l_artikel = None

    t_l_op = None

    t_l_op_list, T_l_op = create_model_like(L_op, {"l_artikel_artnr":int, "l_artikel_bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_lieferant_firma, t_l_op_list, l_op, l_lieferant, l_artikel


        nonlocal t_l_op
        nonlocal t_l_op_list
        return {"l_lieferant_firma": l_lieferant_firma, "t-l-op": t_l_op_list}

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    l_lieferant_firma = l_lieferant.firma

    l_op_obj_list = []
    for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
            (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.op_art == 1) &  (L_op.lief_nr == lief_nr) &  (func.lower(L_op.(docu_nr).lower()) == (docu_nr).lower())).all():
        if l_op._recid in l_op_obj_list:
            continue
        else:
            l_op_obj_list.append(l_op._recid)


        t_l_op = T_l_op()
        t_l_op_list.append(t_l_op)

        buffer_copy(l_op, t_l_op)
        t_l_op.l_artikel_artnr = l_artikel.artnr
        t_l_op.l_artikel_bezeich = l_artikel.bezeich

    return generate_output()