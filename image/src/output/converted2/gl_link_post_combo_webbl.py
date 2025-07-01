#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_hotelnamebl import read_hotelnamebl
from functions.gl_linkfobl import gl_linkfobl
from functions.gl_linkfo_updatebl import gl_linkfo_updatebl
from functions.write_htparambl import write_htparambl
from functions.gl_linkarbl import gl_linkarbl
from functions.gl_linkar_updatebl import gl_linkar_updatebl
from models import Htparam, Gl_acct

g_list_list, G_list = create_model("G_list", {"flag":int, "datum":date, "artnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
ar_glist_list, Ar_glist = create_model("Ar_glist", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "add_info":string, "counter":int, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
trans_dept_list, Trans_dept = create_model("Trans_dept", {"nr":int})
g2_list_list, G2_list = create_model("G2_list", {"flag":int, "datum":date, "artnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
ar_g2list_list, Ar_g2list = create_model("Ar_g2list", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "add_info":string, "counter":int, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_link_post_combo_webbl(g_list_list:[G_list], ar_glist_list:[Ar_glist], trans_dept_list:[Trans_dept], language_code:int, vkey:string, vmodule:string, combo_gastnr:int, user_init:string, pf_file1:string, pf_file2:string, from_date:date, to_date:date, refno:string, bezeich:string, curr_anz1:int, debit1:Decimal, credit1:Decimal, merge_flag:bool, g2_list_list:[G2_list], ar_g2list_list:[Ar_g2list], debits:Decimal, credits:Decimal, remains:Decimal):
    frame_title2 = ""
    last_acctdate = None
    curr_anz = 0
    created = False
    message_result = ""
    s2_list_list = []
    connect_param:string = ""
    connect_paramssl:string = ""
    lreturn:bool = False
    htl_name:string = ""
    debit2:Decimal = to_decimal("0.0")
    credit2:Decimal = to_decimal("0.0")
    curr_anz2:int = 0
    remain2:Decimal = to_decimal("0.0")
    acct_error:int = 0
    art_dpt:int = 0
    art_artnr:int = 0
    art_bezeich:string = ""
    success_flag:bool = False
    err_flag:bool = False
    htparam = gl_acct = None

    g_list = g2_list = combo_glist = ar_glist = ar_g2list = combo_ar_glist = trans_dept = t_htparam = s2_list = None

    combo_glist_list, Combo_glist = create_model("Combo_glist", {"flag":int, "datum":date, "artnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    combo_ar_glist_list, Combo_ar_glist = create_model("Combo_ar_glist", {"rechnr":int, "dept":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "add_info":string, "counter":int, "acct_fibukonto":string, "bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    t_htparam_list, T_htparam = create_model_like(Htparam)
    s2_list_list, S2_list = create_model("S2_list", {"fibukonto":string, "bezeich":string, "credit":Decimal, "debit":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal frame_title2, last_acctdate, curr_anz, created, message_result, s2_list_list, connect_param, connect_paramssl, lreturn, htl_name, debit2, credit2, curr_anz2, remain2, acct_error, art_dpt, art_artnr, art_bezeich, success_flag, err_flag, htparam, gl_acct
        nonlocal language_code, vkey, vmodule, combo_gastnr, user_init, pf_file1, pf_file2, from_date, to_date, refno, bezeich, curr_anz1, debit1, credit1, merge_flag, g2_list_list, ar_g2list_list, debits, credits, remains


        nonlocal g_list, g2_list, combo_glist, ar_glist, ar_g2list, combo_ar_glist, trans_dept, t_htparam, s2_list
        nonlocal combo_glist_list, combo_ar_glist_list, t_htparam_list, s2_list_list

        return {"g2-list": g2_list_list, "ar-g2list": ar_g2list_list, "debits": debits, "credits": credits, "remains": remains, "frame_title2": frame_title2, "last_acctdate": last_acctdate, "curr_anz": curr_anz, "created": created, "message_result": message_result, "s2-list": s2_list_list}

    if pf_file1 == "" or pf_file1 == None:
        message_result = "01 - Param 339 is unfilled."

    elif pf_file2 == "" or pf_file2 == None:
        message_result = "02 - Param 340 is unfilled."

    elif combo_gastnr == 0 or combo_gastnr == None:
        message_result = "03 - Param 155 is unfilled."

    if refno == None:
        refno = ""

    if bezeich == None:
        bezeich = ""

    if vmodule.lower()  == ("vhpIA").lower() :

        if vkey.lower()  == ("createJournalListIA").lower() :
            connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session-free"
            connect_paramssl = connect_param + " -ssl -nohostverify"
            lreturn = set_combo_session(connect_paramssl, None, None, None)

            if not lreturn:
                lreturn = set_combo_session(connect_param, None, None, None)

            if lreturn:
                local_storage.combo_flag = True
                htl_name = get_output(read_hotelnamebl("A120"))
                local_storage.combo_flag = False

            frame_title2 = htl_name + " - " + "F/O Journal Transfer to GL"
            local_storage.combo_flag = True
            curr_anz2, debit2, credit2, acct_error, remain2, art_dpt, art_artnr, art_bezeich, g2_list_list = get_output(gl_linkfobl(trans_dept_list, from_date, to_date, user_init, refno, curr_anz2))
            local_storage.combo_flag = False

            reset_combo_session()

            if acct_error == 1:
                message_result = "04 - COMBO DB: Reference number already exists."

                return generate_output()

            elif acct_error == 2:
                message_result = "05 - COMBO DB: G/L AcctNo not found for the following article:" + chr_unicode(10) + to_string(art_dpt, "99 ") + to_string(art_artnr) + " - " + art_bezeich

                return generate_output()
            debits =  to_decimal(debit1) + to_decimal(debit2)
            credits =  to_decimal(credit1) + to_decimal(credit2)
            curr_anz = curr_anz1 + curr_anz2

            if curr_anz == 0:
                message_result = "06 - No GL journals have been created."

                return generate_output()

            if from_date == (last_acctdate + timedelta(days=1)):
                created = True
            else:
                created = False

        elif vkey.lower()  == ("postJournalListIA").lower() :
            combo_glist_list.clear()

            for g_list in query(g_list_list):
                combo_glist = Combo_glist()
                combo_glist_list.append(combo_glist)

                buffer_copy(g_list, combo_glist)

            for g2_list in query(g2_list_list):
                combo_glist = Combo_glist()
                combo_glist_list.append(combo_glist)

                buffer_copy(g2_list, combo_glist)

            for combo_glist in query(combo_glist_list):

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, combo_glist.fibukonto)]})

                if not gl_acct:
                    message_result = "COA " + combo_glist.fibukonto + " not found."
                    err_flag = True
                    break

            if err_flag:

                return generate_output()
            get_output(gl_linkfo_updatebl(language_code, remains, credits, debits, to_date, refno, bezeich, combo_glist_list))
            connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session-free"
            connect_paramssl = connect_param + " -ssl -nohostverify"
            lreturn = set_combo_session(connect_paramssl, None, None, None)

            if not lreturn:
                lreturn = set_combo_session(connect_param, None, None, None)

            if lreturn:
                local_storage.combo_flag = True
                htl_name = get_output(read_hotelnamebl("A120"))
                local_storage.combo_flag = False


            t_htparam = query(t_htparam_list, first=True)

            if not t_htparam:
                t_htparam = T_htparam()
                t_htparam_list.append(t_htparam)

            t_htparam.paramnr = 1003
            t_htparam.fdate = to_date


            local_storage.combo_flag = True
            success_flag = get_output(write_htparambl(2, t_htparam_list))
            local_storage.combo_flag = False

            reset_combo_session()
            message_result = "Transfer to GL Success."

    elif vmodule.lower()  == ("vhpAR").lower() :

        if vkey.lower()  == ("createJournalListAR").lower() :
            connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session-free"
            connect_paramssl = connect_param + " -ssl -nohostverify"
            lreturn = set_combo_session(connect_paramssl, None, None, None)

            if not lreturn:
                lreturn = set_combo_session(connect_param, None, None, None)

            if lreturn:
                local_storage.combo_flag = True
                htl_name = get_output(read_hotelnamebl("A120"))
                local_storage.combo_flag = False

            frame_title2 = htl_name + " - " + "A/R Journal Transfer to GL"
            local_storage.combo_flag = True
            curr_anz2, acct_error, debit2, credit2, remain2, ar_g2list_list, s2_list_list, art_artnr, art_bezeich = get_output(gl_linkarbl(merge_flag, from_date, to_date, user_init, refno, curr_anz2))
            local_storage.combo_flag = False

            reset_combo_session()

            if acct_error == 1:
                message_result = "04 - COMBO DB: Reference number already exists."

                return generate_output()

            elif acct_error == 2:
                message_result = "05 - COMBO DB: Chart of Account not defined." + chr_unicode(10) + "Article No " + to_string(art_artnr) + " - " + art_bezeich

                return generate_output()
            curr_anz = curr_anz1 + curr_anz2

            if (curr_anz1 + curr_anz2) == 0:
                message_result = "06 - A/R payment records missing." + chr_unicode(10) + "No GL journals have been created."

                return generate_output()
            created = True

            for ar_glist in query(ar_glist_list):
                debits =  to_decimal(debits) + to_decimal(ar_glist.debit)
                credits =  to_decimal(credits) + to_decimal(ar_glist.credit)

            for ar_g2list in query(ar_g2list_list):
                debits =  to_decimal(debits) + to_decimal(ar_g2list.debit)
                credits =  to_decimal(credits) + to_decimal(ar_g2list.credit)

        elif vkey.lower()  == ("postJournalListAR").lower() :
            combo_ar_glist_list.clear()

            for ar_glist in query(ar_glist_list):
                combo_ar_glist = Combo_ar_glist()
                combo_ar_glist_list.append(combo_ar_glist)

                buffer_copy(ar_glist, combo_ar_glist)

            for ar_g2list in query(ar_g2list_list):
                combo_ar_glist = Combo_ar_glist()
                combo_ar_glist_list.append(combo_ar_glist)

                buffer_copy(ar_g2list, combo_ar_glist)

            for ar_g2list in query(ar_g2list_list):

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ar_g2list.fibukonto)]})

                if not gl_acct:
                    message_result = "COA " + ar_g2list.fibukonto + " not found."
                    err_flag = True
                    break

            if err_flag:

                return generate_output()
            get_output(gl_linkar_updatebl(language_code, remains, credits, debits, to_date, refno, bezeich, to_date, combo_ar_glist_list))
            connect_param = "-H " + entry(0, pf_file2, ":") + " -S " + entry(1, pf_file2, ":") + " -DirectConnect -sessionModel Session-free"
            connect_paramssl = connect_param + " -ssl -nohostverify"
            lreturn = set_combo_session(connect_paramssl, None, None, None)

            if not lreturn:
                lreturn = set_combo_session(connect_param, None, None, None)

            if lreturn:
                local_storage.combo_flag = True
                htl_name = get_output(read_hotelnamebl("A120"))
                local_storage.combo_flag = False


            t_htparam = query(t_htparam_list, first=True)

            if not t_htparam:
                t_htparam = T_htparam()
                t_htparam_list.append(t_htparam)

            t_htparam.paramnr = 1014
            t_htparam.fdate = to_date


            local_storage.combo_flag = True
            success_flag = get_output(write_htparambl(2, t_htparam_list))
            local_storage.combo_flag = False

            reset_combo_session()
            message_result = "Transfer to GL Success."

    return generate_output()