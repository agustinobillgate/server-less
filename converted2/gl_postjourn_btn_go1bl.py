#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_postjourn_btn_gobl import gl_postjourn_btn_gobl

g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "acct_fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "bemerk":string, "bezeich":string, "duplicate":bool, "tax_code":string, "tax_amount":string, "tot_amt":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_postjourn_btn_go1bl(g_list_data:[G_list], pvilanguage:int, curr_step:int, bezeich:string, credits:[Decimal], debits:[Decimal], remains:[Decimal], refno:string, datum:date, adjust_flag:bool, journaltype:int):
    curr_jnr = 0
    msg_str = ""
    error_flag = False
    msg_str1 = ""
    lvcarea:string = "gl-postjourn"

    g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_jnr, msg_str, error_flag, msg_str1, lvcarea
        nonlocal pvilanguage, curr_step, bezeich, refno, datum, adjust_flag, journaltype


        nonlocal g_list

        return {"curr_jnr": curr_jnr, "msg_str": msg_str, "error_flag": error_flag, "msg_str1": msg_str1}

    if curr_step == 1:

        if datum == None or refno == "":
            msg_str1 = translateExtended ("Unfilled field(s) detected.", lvcarea, "")

            return generate_output()
        else:
            curr_jnr, msg_str, error_flag = get_output(gl_postjourn_btn_gobl(g_list_data, pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype))

    if curr_step == 2:

        g_list = query(g_list_data, first=True)

        if not g_list:
            msg_str1 = translateExtended ("Journal Transaction not yet entered.", lvcarea, "")

            return generate_output()

        if remains != 0:
            msg_str1 = translateExtended ("Journal Transaction not yet balanced.", lvcarea, "")

            return generate_output()
        else:
            curr_jnr, msg_str, error_flag = get_output(gl_postjourn_btn_gobl(g_list_data, pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype))

    return generate_output()