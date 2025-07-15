#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_mk_apbl import prepare_mk_apbl
from functions.mk_ap_btn_ok_1bl import mk_ap_btn_ok_1bl
from models import Bediener, L_kredit, L_lieferant

s_list_data, S_list = create_model("S_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "flag":bool, "bezeich":string, "remark":string}, {"fibukonto": "000000000000"})

def create_manual_apbl(language_code:int, docu_nr:string, lief_nr:int, firma:string, invoice:string, rgdatum:date, saldo:Decimal, disc:Decimal, d_amount:Decimal, netto:Decimal, ziel:int, ap_other:string, comments:string, balance:Decimal, s_list_fibukonto:string, s_list_debit:Decimal, journ_flag:bool, nr:int, user_init:string, tax_code:string, tax_amt:string, s_list_data:[S_list]):

    prepare_cache ([Bediener, L_kredit, L_lieferant])

    msg_str = ""
    fl_code = 0
    avail_gl = False
    err_code = ""
    avail_sbuff:bool = False
    closed_date:date = None
    defaultrgdatum:date = None
    p_2000:bool = False
    av_gl_acct:bool = False
    ap_acct:string = ""
    gst_flag:bool = False
    bediener_nr:int = 0
    debit:Decimal = to_decimal("0.0")
    credit:Decimal = to_decimal("0.0")
    supplier_name:string = ""
    bediener = l_kredit = l_lieferant = None

    s_list = sbuff = tp_bediener = None

    Sbuff = S_list
    sbuff_data = s_list_data

    Tp_bediener = create_buffer("Tp_bediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, fl_code, avail_gl, err_code, avail_sbuff, closed_date, defaultrgdatum, p_2000, av_gl_acct, ap_acct, gst_flag, bediener_nr, debit, credit, supplier_name, bediener, l_kredit, l_lieferant
        nonlocal language_code, docu_nr, lief_nr, firma, invoice, rgdatum, saldo, disc, d_amount, netto, ziel, ap_other, comments, balance, s_list_fibukonto, s_list_debit, journ_flag, nr, user_init, tax_code, tax_amt
        nonlocal sbuff, tp_bediener


        nonlocal s_list, sbuff, tp_bediener

        return {"s-list": s_list_data, "msg_str": msg_str, "fl_code": fl_code, "avail_gl": avail_gl, "err_code": err_code}


    closed_date, defaultrgdatum, p_2000, av_gl_acct, ap_acct, ap_other, gst_flag = get_output(prepare_mk_apbl())

    sbuff = query(sbuff_data, filters=(lambda sbuff:(sbuff.debit != 0 or sbuff.credit != 0)), first=True)

    if not sbuff:
        avail_sbuff = False
    else:
        avail_sbuff = True

    if firma == "":
        fl_code = 7
        msg_str = "Supplier not yet defined."
        err_code = "7 - " + msg_str

        return generate_output()

    elif docu_nr == "":
        fl_code = 8
        msg_str = "document number not yet defined."
        err_code = "8 - " + msg_str

        return generate_output()

    elif invoice == "":
        fl_code = 9
        msg_str = "invoice number not yet defined."
        err_code = "9 - " + msg_str

        return generate_output()

    elif saldo == 0:
        fl_code = 10
        msg_str = "A/P amount not yet defined."
        err_code = "10 - " + msg_str

        return generate_output()

    elif rgdatum == None:
        fl_code = 11
        msg_str = "A/P DATE not yet defined."
        err_code = "11 - " + msg_str

        return generate_output()

    elif rgdatum <= closed_date:
        fl_code = 12
        msg_str = "Date should be later than " + to_string(closed_date)
        err_code = "12 - " + msg_str

        return generate_output()

    tp_bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if tp_bediener:
        bediener_nr = tp_bediener.nr
    else:
        bediener_nr = nr

    l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, invoice)],"zahlkonto": [(eq, 0)]})

    if l_kredit:

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_kredit.lief_nr)]})

        if l_lieferant:
            supplier_name = l_lieferant.firma
        fl_code = 14
        msg_str = "A/P with same Delivery Number exists:" + " " + to_string(l_kredit.rgdatum) + " " + supplier_name
        err_code = "14 - " + msg_str

        return generate_output()
    s_list_data, msg_str, fl_code, avail_gl = get_output(mk_ap_btn_ok_1bl(s_list_data, language_code, invoice, journ_flag, balance, avail_sbuff, docu_nr, rgdatum, lief_nr, disc, saldo, d_amount, ziel, bediener_nr, comments, netto, user_init, ap_other, user_init, firma, s_list_fibukonto, s_list_debit, tax_code, tax_amt))

    if not avail_gl:
        fl_code = 13
        msg_str = "G/L account number not defined."
        err_code = "13 - " + msg_str

        for s_list in query(s_list_data):

            if s_list.flag:
                s_list.debit =  to_decimal(s_list.debit)
                s_list.fibukonto = "000000000000"

        return generate_output()

    if msg_str != "":
        err_code = to_string(fl_code) + " - " + msg_str

        return generate_output()

    return generate_output()