#using conversion tools version: 1.0.0.119

# ================================
# Rulita, 10-11-2025 | 36D1D2
# New compile program
# ================================
# Rd, 25/11/2025, with_for_update
# ================================
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Queasy

def mk_resline_btn_stopbl(avail_t_res_line:bool, t_res_line_resnr:int, t_res_line_reslinnr:int, init_time_resline1:int, 
                          init_date_resline1:date, inp_resno:int, inp_resline:int, init_time_resline:int, init_date_resline:date, init_time_rsv:int, init_date_rsv:date):
    flag_ok:bool = False
    a:int = 0
    b:date = None
    check_time_str:string = ""
    check_time_str2:string = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_ok, a, b, check_time_str, check_time_str2, queasy
        nonlocal avail_t_res_line, t_res_line_resnr, t_res_line_reslinnr, init_time_resline1, init_date_resline1, inp_resno, inp_resline, init_time_resline, init_date_resline, init_time_rsv, init_date_rsv

        return {}


    # queasy = get_cache (Queasy, {"key": [(eq, 359)],"number3": [(eq, 1)],"number1": [(eq, t_res_line_resnr)],"number2": [(eq, t_res_line_reslinnr)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 359) & (Queasy.number3 == 1) & (Queasy.number1 == t_res_line_resnr) & (Queasy.number2 == t_res_line_reslinnr)).with_for_update().first()

    if queasy:
        db_session.delete(queasy)
        pass
    check_time_str = "res-line"

    if avail_t_res_line:
        flag_ok, a, b = get_output(check_timebl(2, t_res_line_resnr, t_res_line_reslinnr, check_time_str, init_time_resline1, init_date_resline1))
    flag_ok, a, b = get_output(check_timebl(2, inp_resno, inp_resline, check_time_str, init_time_resline, init_date_resline))
    check_time_str2 = "reservation"
    flag_ok, a, b = get_output(check_timebl(2, inp_resno, None, check_time_str2, init_time_rsv, init_date_rsv))

    return generate_output()