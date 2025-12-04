#using conversion tools version: 1.0.0.117

# -------------------------------------------
# Rulita, 10-09-2025 
# TiketID : 5BE11A
# Issue recompile program 
# -------------------------------------------

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import L_op

def storereq_list_btn_exit2bl(t_list_s_recid:int, flager:int, tlager:int):

    prepare_cache ([L_op])

    l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op
        nonlocal t_list_s_recid, flager, tlager

        return {}


    # l_op = get_cache (L_op, {"_recid": [(eq, t_list_s_recid)]})
    l_op = db_session.query(L_op).filter(
             (L_op._recid == t_list_s_recid)).with_for_update().first()

    if l_op:
        # pass
        l_op.lager_nr = flager
        l_op.pos = tlager
        # pass
        # pass
        db_session.refresh(l_op, with_for_update=True)

    return generate_output()