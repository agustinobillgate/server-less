#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})
sbudget_list, Sbudget = create_model("Sbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})

def eg_received_budget_fromgl_webbl(resources_char1:string, tbudget_list:[Tbudget], sbudget_list:[Sbudget]):

    prepare_cache ([Gl_acct])

    msg_str = ""
    i:int = 0
    gl_acct = None

    tbudget = sbudget = buf_gl_acct = None

    Buf_gl_acct = create_buffer("Buf_gl_acct",Gl_acct)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, i, gl_acct
        nonlocal resources_char1
        nonlocal buf_gl_acct


        nonlocal tbudget, sbudget, buf_gl_acct

        return {"tbudget": tbudget_list, "sbudget": sbudget_list, "msg_str": msg_str}


    if resources_char1 != "":

        buf_gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, resources_char1)]})

        if not buf_gl_acct:
            msg_str = "Wrong COA Definition"
        else:
            for i in range(1,12 + 1) :

                tbudget = query(tbudget_list, filters=(lambda tbudget: tbudget.month == i), first=True)
                tbudget.amount =  to_decimal(buf_gl_acct.budget[i - 1])
                pass

                sbudget = query(sbudget_list, filters=(lambda sbudget: sbudget.month == i), first=True)
                sbudget.amount =  to_decimal(buf_gl_acct.budget[i - 1])
                pass
    else:
        msg_str = "COA Not Yet Defined."

    return generate_output()