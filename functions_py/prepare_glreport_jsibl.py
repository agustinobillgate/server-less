#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 10/10/2025
# fchar -> htparam.fchar
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Gl_acct, Gl_department

def prepare_glreport_jsibl(lvcarea:string):

    prepare_cache ([Queasy, Htparam, Gl_department])

    end_month = 0
    beg_month = 0
    pbal_flag = False
    to_date = None
    from_date = None
    close_date = None
    close_year = None
    close_month = 0
    pnl_acct = ""
    c_977 = ""
    pr_opt_str = ""
    t_gl_depart_data = []
    t_gl_department_data = []
    queasy = htparam = gl_acct = gl_department = None

    t_gl_depart = t_gl_department = None

    t_gl_depart_data, T_gl_depart = create_model("T_gl_depart", {"nr":int, "bezeich":string})
    t_gl_department_data, T_gl_department = create_model("T_gl_department", {"nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal end_month, beg_month, pbal_flag, to_date, from_date, close_date, close_year, close_month, pnl_acct, c_977, pr_opt_str, t_gl_depart_data, t_gl_department_data, queasy, htparam, gl_acct, gl_department
        nonlocal lvcarea


        nonlocal t_gl_depart, t_gl_department
        nonlocal t_gl_depart_data, t_gl_department_data

        return {"end_month": end_month, "beg_month": beg_month, "pbal_flag": pbal_flag, "to_date": to_date, "from_date": from_date, "close_date": close_date, "close_year": close_year, "close_month": close_month, "pnl_acct": pnl_acct, "c_977": c_977, "pr_opt_str": pr_opt_str, "t-gl-depart": t_gl_depart_data, "t-gl-department": t_gl_department_data}


    queasy = get_cache (Queasy, {"key": [(eq, 140)],"char1": [(eq, lvcarea)]})

    if queasy:
        pr_opt_str = queasy.char3

    htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
    c_977 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 993)]})
    end_month = htparam.finteger
    beg_month = htparam.finteger + 1

    if beg_month > 12:
        beg_month = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 460)]})
    pbal_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    close_month = get_month(to_date)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    close_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate
    close_year = date_mdy(get_month(close_year) , get_day(close_year) , get_year(close_year) + timedelta(days=1))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 979)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

    if gl_acct:
        pnl_acct = htparam.fchar

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        t_gl_depart = T_gl_depart()
        t_gl_depart_data.append(t_gl_depart)

        t_gl_depart.nr = gl_department.nr
        t_gl_depart.bezeich = gl_department.bezeich

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        t_gl_department = T_gl_department()
        t_gl_department_data.append(t_gl_department)

        t_gl_department.nr = gl_department.nr
        t_gl_department.bezeich = gl_department.bezeich

    return generate_output()