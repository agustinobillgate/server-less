from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_mk_apbl import prepare_mk_apbl
from sqlalchemy import func
from functions.mk_ap_btn_okbl import mk_ap_btn_okbl
from models import Bediener

def create_manual_apbl(language_code:int, docu_nr:str, lief_nr:int, firma:str, invoice:str, rgdatum:date, saldo:decimal, disc:decimal, d_amount:decimal, netto:decimal, ziel:int, ap_other:str, comments:str, balance:decimal, s_list_fibukonto:str, s_list_debit:decimal, journ_flag:bool, nr:int, user_init:str, tax_code:str, tax_amt:str, s_list:[S_list]):
    msg_str = ""
    fl_code = 0
    avail_gl = False
    err_code = ""
    avail_sbuff:bool = False
    closed_date:date = None
    defaultrgdatum:date = None
    p_2000:bool = False
    av_gl_acct:bool = False
    ap_acct:str = ""
    gst_flag:bool = False
    bediener_nr:int = 0
    debit:decimal = 0
    credit:decimal = 0
    bediener = None

    s_list = sbuff = tp_bediener = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "flag":bool, "bezeich":str}, {"fibukonto": "000000000000"})

    Sbuff = S_list
    sbuff_list = s_list_list

    Tp_bediener = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, fl_code, avail_gl, err_code, avail_sbuff, closed_date, defaultrgdatum, p_2000, av_gl_acct, ap_acct, gst_flag, bediener_nr, debit, credit, bediener
        nonlocal sbuff, tp_bediener


        nonlocal s_list, sbuff, tp_bediener
        nonlocal s_list_list
        return {"msg_str": msg_str, "fl_code": fl_code, "avail_gl": avail_gl, "err_code": err_code}


    closed_date, defaultrgdatum, p_2000, av_gl_acct, ap_acct, ap_other, gst_flag = get_output(prepare_mk_apbl())

    sbuff = query(sbuff_list, filters=(lambda sbuff :(sbuff.debit != 0 or sbuff.credit != 0)), first=True)

    if not sbuff:
        avail_sbuff = False
    else:
        avail_sbuff = True

    if firma == "":
        msg_str = "Supplier not yet defined."
        err_code = "7 - " + msg_str

        return generate_output()

    elif docu_nr == "":
        msg_str = "document number not yet defined."
        err_code = "8 - " + msg_str

        return generate_output()

    elif invoice == "":
        msg_str = "invoice number not yet defined."
        err_code = "9 - " + msg_str

        return generate_output()

    elif saldo == 0:
        msg_str = "A/P amount not yet defined."
        err_code = "10 - " + msg_str

        return generate_output()

    elif rgdatum == None:
        msg_str = "A/P DATE not yet defined."
        err_code = "11 - " + msg_str

        return generate_output()

    elif rgdatum <= closed_date:
        msg_str = "Date should be later than " + to_string(closed_date)
        err_code = "12 - " + msg_str

        return generate_output()

    tp_bediener = db_session.query(Tp_bediener).filter(
            (func.lower(Tp_bediener.userinit) == (user_init).lower())).first()

    if tp_bediener:
        bediener_nr = tp_bediener.nr
    else:
        bediener_nr = nr
    s_list_list, msg_str, fl_code, avail_gl = get_output(mk_ap_btn_okbl(s_list, language_code, invoice, journ_flag, balance, avail_sbuff, docu_nr, rgdatum, lief_nr, disc, saldo, d_amount, ziel, bediener_nr, comments, netto, user_init, ap_other, user_init, firma, s_list_fibukonto, s_list_debit, tax_code, tax_amt))

    if not avail_gl:
        msg_str = "G/L account number not defined."
        err_code = "13 - " + msg_str

        for s_list in query(s_list_list):

            if s_list.flag:
                s_list.debit = s_list.debit
                s_list.fibukonto = "000000000000"

        return generate_output()

    if msg_str != "":
        err_code = to_string(fl_code) + " - " + msg_str

        return generate_output()