#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import B_storno

def main_fs_proc_btn_chgbl(b1_resnr:int, b1_resline:int, curr_gastnr:int):
    t_b_storno_data = []
    b_storno = None

    t_b_storno = None

    t_b_storno_data, T_b_storno = create_model_like(B_storno)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_b_storno_data, b_storno
        nonlocal b1_resnr, b1_resline, curr_gastnr


        nonlocal t_b_storno
        nonlocal t_b_storno_data

        return {"t-b-storno": t_b_storno_data}

    for b_storno in db_session.query(B_storno).filter(
             (B_storno.bankettnr == b1_resnr) & (B_storno.breslinnr == b1_resline) & (B_storno.gastnr == curr_gastnr)).order_by(B_storno._recid).all():
        t_b_storno = T_b_storno()
        t_b_storno_data.append(t_b_storno)

        buffer_copy(b_storno, t_b_storno)

    return generate_output()