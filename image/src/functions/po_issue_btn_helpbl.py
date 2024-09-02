from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Htparam

def po_issue_btn_helpbl(cost_acct:str):
    cost_center = ""
    jobnr = 0
    flag = 0
    avail_glacct = False
    gl_acct = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_center, jobnr, flag, avail_glacct, gl_acct, htparam


        return {"cost_center": cost_center, "jobnr": jobnr, "flag": flag, "avail_glacct": avail_glacct}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if gl_acct:
        avail_glacct = True
        cost_center = gl_acct.bezeich
        jobnr = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 933)).first()

        if gl_acct.main_nr == htparam.finteger and gl_acct.main_nr != 0:
            flag = 1

        return generate_output()