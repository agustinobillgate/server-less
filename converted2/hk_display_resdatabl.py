#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_roomplan_disp_resdatabl import hk_roomplan_disp_resdatabl

def hk_display_resdatabl(i:int, curr_date:date, zinr:string, gstatus:int, recid1:int):
    n_edit = ""
    c_edit = ""
    fgcol_n:int = 0
    fgcol_c:int = 0

    t_res_line = None

    t_res_line_data, T_res_line = create_model("T_res_line", {"rec_id":int, "ziwech_zeit":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n_edit, c_edit, fgcol_n, fgcol_c
        nonlocal i, curr_date, zinr, gstatus, recid1


        nonlocal t_res_line
        nonlocal t_res_line_data

        return {"n_edit": n_edit, "c_edit": c_edit}

    if (i > 17) or (i < 0):
        n_edit = ""
        c_edit = ""
    else:

        if i == 0:
            n_edit, c_edit, fgcol_n, fgcol_c, t_res_line_data = get_output(hk_roomplan_disp_resdatabl(i, curr_date, zinr, None, None))
        else:
            n_edit, c_edit, fgcol_n, fgcol_c, t_res_line_data = get_output(hk_roomplan_disp_resdatabl(i, curr_date, zinr, gstatus, recid1))

    return generate_output()