from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def ins_pr_check_cost_acctbl(pvilanguage:int, cost_acct:str):
    msg_str = ""
    lvcarea:str = "ins_pr"
    gl_acct = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, gl_acct


        return {"msg_str": msg_str}


    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (cost_acct).lower())).first()

    if not gl_acct:
        msg_str = translateExtended ("Account Number incorrect.", lvcarea, "")

    if gl_acct and gl_acct.acc_type == 1:
        msg_str = translateExtended ("Wrong Type of Account Number.", lvcarea, "")

    return generate_output()