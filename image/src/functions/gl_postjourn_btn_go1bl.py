from functions.additional_functions import *
import decimal
from datetime import date
from functions.gl_postjourn_btn_gobl import gl_postjourn_btn_gobl

g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "acct_fibukonto":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bemerk":str, "bezeich":str, "duplicate":bool, "tax_code":str, "tax_amount":str, "tot_amt":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
# "datum": "01/17/24",
def gl_postjourn_btn_go1bl(g_list_list:[G_list], pvilanguage:int, curr_step:int, bezeich:str, credits:decimal, debits:decimal, remains:decimal, refno:str, datum:date, adjust_flag:bool, journaltype:int):
    curr_jnr = 0
    msg_str = ""
    error_flag = False
    msg_str1 = ""
    lvcarea:str = "gl_postjourn"
    g_list = None
    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_jnr, msg_str, error_flag, msg_str1, lvcarea
        nonlocal g_list
        global g_list_list
        return {"curr_jnr": curr_jnr, "msg_str": msg_str, "error_flag": error_flag, "msg_str1": msg_str1}

    if curr_step == 1:

        if datum == None or refno == "":
            msg_str1 = translateExtended ("Unfilled field(s) detected.", lvcarea, "")

            return generate_output()
        else:
            curr_jnr, msg_str, error_flag = get_output(gl_postjourn_btn_gobl(g_list, pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype))

    if curr_step == 2:

        g_list = query(g_list_list, first=True)

        if not g_list:
            msg_str1 = translateExtended ("Journal Transaction not yet entered.", lvcarea, "")

            return generate_output()

        if remains != 0:
            msg_str1 = translateExtended ("Journal Transaction not yet balanced.", lvcarea, "")

            return generate_output()
        else:
            curr_jnr, msg_str, error_flag = get_output(gl_postjourn_btn_gobl(g_list, pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype))

    return generate_output()