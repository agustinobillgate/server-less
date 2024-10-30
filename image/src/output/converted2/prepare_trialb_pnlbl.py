from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Gl_acct

def prepare_trialb_pnlbl():
    pbal_flag = False
    to_date = None
    close_date = None
    pnl_acct = ""
    gl_depart_list_list = []
    beg_month:int = 0
    end_month:int = 0
    htparam = gl_acct = None

    gl_depart_list = None

    gl_depart_list_list, Gl_depart_list = create_model("Gl_depart_list", {"nr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pbal_flag, to_date, close_date, pnl_acct, gl_depart_list_list, beg_month, end_month, htparam, gl_acct


        nonlocal gl_depart_list
        nonlocal gl_depart_list_list

        return {"pbal_flag": pbal_flag, "to_date": to_date, "close_date": close_date, "pnl_acct": pnl_acct, "gl-depart-list": gl_depart_list_list}

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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 597)).first()
    close_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 979)).first()

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto == fchar)).first()

    if gl_acct:
        pnl_acct = htparam.fchar

    for gl_depart_list in query(gl_depart_list_list):
        gl_depart_list = Gl_depart_list()
        gl_depart_list_list.append(gl_depart_list)

        gl_depart_list.nr = gl_depart_list.nr
        gl_depart_list.bezeich = gl_depart_list.bezeich

    return generate_output()