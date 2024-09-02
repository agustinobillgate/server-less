from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl

def mk_resline_btn_stopbl(avail_t_res_line:bool, t_res_line_resnr:int, t_res_line_reslinnr:int, init_time_resline1:int, init_date_resline1:date, inp_resno:int, inp_resline:int, init_time_resline:int, init_date_resline:date, init_time_rsv:int, init_date_rsv:date):
    flag_ok:bool = False
    a:int = 0
    b:date = None
    check_time_str:str = ""
    check_time_str2:str = ""


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_ok, a, b, check_time_str, check_time_str2


        return {}

    check_time_str = "res_line"

    if avail_t_res_line:
        flag_ok, a, b = get_output(check_timebl(2, t_res_line_resnr, t_res_line_reslinnr, check_time_str, init_time_resline1, init_date_resline1))
    flag_ok, a, b = get_output(check_timebl(2, inp_resno, inp_resline, check_time_str, init_time_resline, init_date_resline))
    check_time_str2 = "reservation"
    flag_ok, a, b = get_output(check_timebl(2, inp_resno, None, check_time_str2, init_time_rsv, init_date_rsv))

    return generate_output()