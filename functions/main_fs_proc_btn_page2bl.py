#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import B_storno

def main_fs_proc_btn_page2bl(b1_resnr:int, b1_resline:int, curr_gastnr:int):

    prepare_cache ([B_storno])

    avail_b_storno = False
    tt_grund_data = []
    i:int = 0
    b_storno = None

    tt_grund = None

    tt_grund_data, Tt_grund = create_model("Tt_grund", {"curr_i":int, "grund":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_b_storno, tt_grund_data, i, b_storno
        nonlocal b1_resnr, b1_resline, curr_gastnr


        nonlocal tt_grund
        nonlocal tt_grund_data

        return {"avail_b_storno": avail_b_storno, "tt-grund": tt_grund_data}

    b_storno = get_cache (B_storno, {"bankettnr": [(eq, b1_resnr)],"breslinnr": [(eq, b1_resline)],"gastnr": [(eq, curr_gastnr)]})

    if b_storno:
        avail_b_storno = True
        for i in range(1,10 + 1) :
            tt_grund = Tt_grund()
            tt_grund_data.append(tt_grund)

            tt_grund.curr_i = i
            tt_grund.grund = b_storno.grund[i - 1]

    return generate_output()