#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_linkarbl import gl_linkarbl

def gl_linkar_load_databl(pvilanguage:int, merge_flag:bool, from_date:date, to_date:date, user_init:string, refno:string):
    curr_anz = 0
    msg_str = ""
    g_list_list = []
    s_list_list = []
    acct_error:int = 0
    debit1:Decimal = to_decimal("0.0")
    credit1:Decimal = to_decimal("0.0")
    remain1:Decimal = to_decimal("0.0")
    art_artnr:int = 0
    art_bezeich:string = ""
    lvcarea:string = "gl-linkar-load-data"

    g_list = s_list = None

    g_list_list, G_list = create_model("G_list", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "add_info":string, "counter":int, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    s_list_list, S_list = create_model("S_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_anz, msg_str, g_list_list, s_list_list, acct_error, debit1, credit1, remain1, art_artnr, art_bezeich, lvcarea
        nonlocal pvilanguage, merge_flag, from_date, to_date, user_init, refno


        nonlocal g_list, s_list
        nonlocal g_list_list, s_list_list

        return {"curr_anz": curr_anz, "msg_str": msg_str, "g-list": g_list_list, "s-list": s_list_list}

    curr_anz, acct_error, debit1, credit1, remain1, g_list_list, s_list_list, art_artnr, art_bezeich = get_output(gl_linkarbl(merge_flag, from_date, to_date, user_init, refno, curr_anz))

    if acct_error == 1:
        msg_str = translateExtended ("Reference number already exists.", lvcarea, "")

        return generate_output()

    elif acct_error == 2:
        msg_str = translateExtended ("Chart of Account not defined ", lvcarea, "") + chr_unicode(13) + chr_unicode(10) +\
                translateExtended ("ArticleNo", lvcarea, "") + " " + to_string(art_artnr) + " - " + art_bezeich

        return generate_output()

    return generate_output()