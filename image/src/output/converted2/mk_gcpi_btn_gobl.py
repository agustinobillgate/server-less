#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gc_pibline

def mk_gcpi_btn_gobl(pvilanguage:int, inv_acctno:string, invoice_amt:Decimal, pbuff_docu_nr:string, pi_liefnr:int, invoice_nr:string, inv_bezeich:string, inv_bemerk:string, supplier:string):

    prepare_cache ([Gc_pibline])

    msg_str = ""
    inv_list_list = []
    lvcarea:string = "mk-gcPI"
    gl_acct = gc_pibline = None

    inv_list = None

    inv_list_list, Inv_list = create_model("Inv_list", {"s_recid":int, "reihenfolge":int, "amount":Decimal, "remark":string, "inv_acctno":string, "inv_bezeich":string, "supplier":string, "invno":string, "created":date, "zeit":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, inv_list_list, lvcarea, gl_acct, gc_pibline
        nonlocal pvilanguage, inv_acctno, invoice_amt, pbuff_docu_nr, pi_liefnr, invoice_nr, inv_bezeich, inv_bemerk, supplier


        nonlocal inv_list
        nonlocal inv_list_list

        return {"msg_str": msg_str, "inv-list": inv_list_list}

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, inv_acctno)]})

    if not gl_acct:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("GL Account Number not found.", lvcarea, "")

    elif invoice_amt == 0:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Enter the amount.", lvcarea, "")
    else:
        gc_pibline = Gc_pibline()
        db_session.add(gc_pibline)

        gc_pibline.docu_nr = pbuff_docu_nr
        gc_pibline.supplier = supplier
        gc_pibline.lief_nr = pi_liefnr
        gc_pibline.invoice_nr = invoice_nr
        gc_pibline.inv_acctno = inv_acctno
        gc_pibline.inv_bezeich = inv_bezeich
        gc_pibline.inv_amount =  to_decimal(invoice_amt)
        gc_pibline.inv_bemerk = inv_bemerk
        gc_pibline.created = get_current_date()
        gc_pibline.zeit = get_current_time_in_seconds()


        inv_list = Inv_list()
        inv_list_list.append(inv_list)

        inv_list.supplier = gc_pibline.supplier
        inv_list.inv_acctno = gc_pibline.inv_acctno
        inv_list.inv_bezeich = gc_pibline.inv_bezeich
        inv_list.amount =  to_decimal(gc_pibline.inv_amount)
        inv_list.remark = gc_pibline.inv_bemerk
        inv_list.invno = gc_pibline.invoice_nr
        inv_list.created = gc_pibline.created
        inv_list.zeit = gc_pibline.zeit
        inv_list.s_recid = gc_pibline._recid

    return generate_output()