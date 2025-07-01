#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_restinv_run_helpbl import ts_restinv_run_helpbl
from functions.ts_restinv_run_help_check_billbl import ts_restinv_run_help_check_billbl
from models import H_bill, H_artikel

def ts_restinv_run_help4bl(kpr_time:int, kpr_recid:int, bill_date:date, tischnr:int, curr_dept:int, amount:Decimal):
    fl_code = False
    t_h_bill_tmp_list = []
    t_h_artikel1_list = []
    t_h_bill_list = []
    h_bill = h_artikel = None

    t_h_bill = t_h_artikel1 = t_h_bill_tmp = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel1_list, T_h_artikel1 = create_model_like(H_artikel, {"rec_id":int})
    t_h_bill_tmp_list, T_h_bill_tmp = create_model_like(T_h_bill)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, t_h_bill_tmp_list, t_h_artikel1_list, t_h_bill_list, h_bill, h_artikel
        nonlocal kpr_time, kpr_recid, bill_date, tischnr, curr_dept, amount


        nonlocal t_h_bill, t_h_artikel1, t_h_bill_tmp
        nonlocal t_h_bill_list, t_h_artikel1_list, t_h_bill_tmp_list

        return {"kpr_time": kpr_time, "kpr_recid": kpr_recid, "fl_code": fl_code, "t-h-bill-tmp": t_h_bill_tmp_list, "t-h-artikel1": t_h_artikel1_list, "t-h-bill": t_h_bill_list}


    kpr_time, kpr_recid, fl_code, t_h_artikel1_list, t_h_bill_list = get_output(ts_restinv_run_helpbl(kpr_time, kpr_recid, bill_date, tischnr, curr_dept, amount))
    t_h_bill_tmp_list.clear()
    t_h_bill_tmp_list = get_output(ts_restinv_run_help_check_billbl(3, tischnr, curr_dept))

    return generate_output()