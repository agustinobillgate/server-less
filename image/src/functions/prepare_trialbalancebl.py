from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam, Gl_acct, Gl_department

def prepare_trialbalancebl(lvcarea:str):
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
    t_gl_depart_list = []
    t_gl_department_list = []
    queasy = htparam = gl_acct = gl_department = None

    t_gl_depart = t_gl_department = None

    t_gl_depart_list, T_gl_depart = create_model("T_gl_depart", {"nr":int, "bezeich":str})
    t_gl_department_list, T_gl_department = create_model("T_gl_department", {"nr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal end_month, beg_month, pbal_flag, to_date, from_date, close_date, close_year, close_month, pnl_acct, c_977, pr_opt_str, t_gl_depart_list, t_gl_department_list, queasy, htparam, gl_acct, gl_department


        nonlocal t_gl_depart, t_gl_department
        nonlocal t_gl_depart_list, t_gl_department_list
        return {"end_month": end_month, "beg_month": beg_month, "pbal_flag": pbal_flag, "to_date": to_date, "from_date": from_date, "close_date": close_date, "close_year": close_year, "close_month": close_month, "pnl_acct": pnl_acct, "c_977": c_977, "pr_opt_str": pr_opt_str, "t-gl-depart": t_gl_depart_list, "t-gl-department": t_gl_department_list}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 140) &  (Queasy.char1 == lvcarea)).first()

    if queasy:
        pr_opt_str = queasy.char3

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 977)).first()
    c_977 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 993)).first()
    end_month = htparam.finteger
    beg_month = htparam.finteger + 1

    if beg_month > 12:
        beg_month = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 460)).first()
    pbal_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    close_month = get_month(to_date)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    close_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    close_year = htparam.fdate
    close_year = date_mdy(get_month(close_year) , get_day(close_year) , get_year(close_year) + 1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 979)).first()

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == htparam.fchar)).first()

    if gl_acct:
        pnl_acct = htparam.fchar

    for gl_department in db_session.query(Gl_department).all():
        t_gl_depart = T_gl_depart()
        t_gl_depart_list.append(t_gl_depart)

        t_gl_depart.nr = gl_department.nr
        t_gl_depart.bezeich = gl_department.bezeich

    for gl_department in db_session.query(Gl_department).all():
        t_gl_department = T_gl_department()
        t_gl_department_list.append(t_gl_department)

        t_gl_department.nr = gl_department.nr
        t_gl_department.bezeich = gl_department.bezeich

    return generate_output()