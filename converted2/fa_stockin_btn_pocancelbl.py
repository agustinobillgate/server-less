#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_op, Fa_artikel, L_kredit

def fa_stockin_btn_pocancelbl(rec_id:int):

    prepare_cache ([Fa_op, Fa_artikel])

    t_depn_wert = 0
    err_flag = 0
    fa_op = fa_artikel = l_kredit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_depn_wert, err_flag, fa_op, fa_artikel, l_kredit
        nonlocal rec_id

        return {"t_depn_wert": t_depn_wert, "err_flag": err_flag}


    fa_op = get_cache (Fa_op, {"_recid": [(eq, rec_id)]})

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, fa_op.nr)]})

    if fa_artikel.depn_wert != 0:
        t_depn_wert = fa_artikel.depn_wert
        err_flag = 1
    else:

        l_kredit = get_cache (L_kredit, {"name": [(eq, fa_op.lscheinnr)],"lief_nr": [(eq, fa_op.lief_nr)],"opart": [(ge, 1)]})

        if l_kredit:
            err_flag = 2
        else:
            err_flag = 3

    return generate_output()