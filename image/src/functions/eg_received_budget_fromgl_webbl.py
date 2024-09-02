from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct

def eg_received_budget_fromgl_webbl(resources_char1:str, tbudget:[Tbudget], sbudget:[Sbudget]):
    msg_str = ""
    i:int = 0
    gl_acct = None

    tbudget = sbudget = buf_gl_acct = None

    tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":str, "amount":decimal})
    sbudget_list, Sbudget = create_model("Sbudget", {"res_nr":int, "year":int, "month":int, "strmonth":str, "amount":decimal})

    Buf_gl_acct = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, i, gl_acct
        nonlocal buf_gl_acct


        nonlocal tbudget, sbudget, buf_gl_acct
        nonlocal tbudget_list, sbudget_list
        return {"msg_str": msg_str}


    if resources_char1 != "":

        buf_gl_acct = db_session.query(Buf_gl_acct).filter(
                (func.lower(Buf_gl_acct.fibukonto) == (resources_char1).lower())).first()

        if not buf_gl_acct:
            msg_str = "Wrong COA Definition"
        else:
            for i in range(1,12 + 1) :

                tbudget = query(tbudget_list, filters=(lambda tbudget :tbudget.MONTH == i), first=True)
                tbudget.amount = buf_gl_acct.budget[i - 1]

                tbudget = query(tbudget_list, current=True)

                sbudget = query(sbudget_list, filters=(lambda sbudget :sbudget.MONTH == i), first=True)
                sbudget.amount = buf_gl_acct.budget[i - 1]

                sbudget = query(sbudget_list, current=True)
    else:
        msg_str = "COA Not Yet Defined."

    return generate_output()