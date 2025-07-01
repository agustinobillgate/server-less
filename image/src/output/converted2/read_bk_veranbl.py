#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran

def read_bk_veranbl(case_type:int, gastno:int, resstat:int, rechno:int, actflag:int):
    t_bk_veran_list = []
    bk_veran = None

    t_bk_veran = None

    t_bk_veran_list, T_bk_veran = create_model_like(Bk_veran)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_veran_list, bk_veran
        nonlocal case_type, gastno, resstat, rechno, actflag


        nonlocal t_bk_veran
        nonlocal t_bk_veran_list

        return {"t-bk-veran": t_bk_veran_list}

    if case_type == 1:

        bk_veran = get_cache (Bk_veran, {"gastnr": [(eq, gastno)],"resstatus": [(le, resstat)]})

        if bk_veran:
            t_bk_veran = T_bk_veran()
            t_bk_veran_list.append(t_bk_veran)

            buffer_copy(bk_veran, t_bk_veran)
    elif case_type == 2:

        bk_veran = get_cache (Bk_veran, {"rechnr": [(eq, rechno)]})

        if bk_veran:
            t_bk_veran = T_bk_veran()
            t_bk_veran_list.append(t_bk_veran)

            buffer_copy(bk_veran, t_bk_veran)
    elif case_type == 3:

        bk_veran = get_cache (Bk_veran, {"rechnr": [(eq, rechno)],"activeflag": [(eq, actflag)]})

        if bk_veran:
            t_bk_veran = T_bk_veran()
            t_bk_veran_list.append(t_bk_veran)

            buffer_copy(bk_veran, t_bk_veran)

    return generate_output()