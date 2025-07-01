#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_lieferant, L_artikel

def po_inlistbl(lief_nr:int, docu_nr:string, from_date:date, to_date:date):

    prepare_cache ([L_lieferant, L_artikel])

    l_lieferant_firma = ""
    t_l_op_list = []
    l_op = l_lieferant = l_artikel = None

    t_l_op = None

    t_l_op_list, T_l_op = create_model_like(L_op, {"l_artikel_artnr":int, "l_artikel_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_lieferant_firma, t_l_op_list, l_op, l_lieferant, l_artikel
        nonlocal lief_nr, docu_nr, from_date, to_date


        nonlocal t_l_op
        nonlocal t_l_op_list

        return {"l_lieferant_firma": l_lieferant_firma, "t-l-op": t_l_op_list}

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    l_lieferant_firma = l_lieferant.firma

    l_op_obj_list = {}
    for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
             (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 1) & (L_op.lief_nr == lief_nr) & (L_op.docu_nr == (docu_nr).lower())).order_by(L_op.datum, L_op.artnr).all():
        if l_op_obj_list.get(l_op._recid):
            continue
        else:
            l_op_obj_list[l_op._recid] = True


        t_l_op = T_l_op()
        t_l_op_list.append(t_l_op)

        buffer_copy(l_op, t_l_op)
        t_l_op.l_artikel_artnr = l_artikel.artnr
        t_l_op.l_artikel_bezeich = l_artikel.bezeich

    return generate_output()