from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_acct, Gc_pibline

def mk_gcpi_btn_gobl(pvilanguage:int, inv_acctno:str, invoice_amt:decimal, pbuff_docu_nr:str, pi_liefnr:int, invoice_nr:str, inv_bezeich:str, inv_bemerk:str, supplier:str):
    msg_str = ""
    inv_list_list = []
    lvcarea:str = "mk_gcPI"
    gl_acct = gc_pibline = None

    inv_list = None

    inv_list_list, Inv_list = create_model("Inv_list", {"s_recid":int, "reihenfolge":int, "amount":decimal, "remark":str, "inv_acctno":str, "inv_bezeich":str, "supplier":str, "invno":str, "created":date, "zeit":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, inv_list_list, lvcarea, gl_acct, gc_pibline


        nonlocal inv_list
        nonlocal inv_list_list
        return {"msg_str": msg_str, "inv-list": inv_list_list}

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == inv_acctno)).first()

    if not gl_acct:
        msg_str = msg_str + chr(2) + translateExtended ("GL Account Number not found.", lvcarea, "")

    elif invoice_amt == 0:
        msg_str = msg_str + chr(2) + translateExtended ("Enter the amount.", lvcarea, "")
    else:
        gc_pibline = Gc_pibline()
        db_session.add(gc_pibline)

        gc_PIbline.docu_nr = pbuff_docu_nr
        gc_PIbline.supplier = supplier
        gc_PIbline.lief_nr = pi_liefnr
        gc_PIbline.invoice_nr = invoice_nr
        gc_PIbline.inv_acctno = inv_acctno
        gc_PIbline.inv_bezeich = inv_bezeich
        gc_PIbline.inv_amount = invoice_amt
        gc_PIbline.inv_bemerk = inv_bemerk
        gc_PIbline.created = get_current_date()
        gc_PIbline.zeit = get_current_time_in_seconds()


        inv_list = Inv_list()
        inv_list_list.append(inv_list)

        inv_list.supplier = gc_PIbline.supplier
        inv_list.inv_acctno = gc_PIbline.inv_acctno
        inv_list.inv_bezeich = gc_PIbline.inv_bezeich
        inv_list.amount = gc_PIbline.inv_amount
        inv_list.remark = gc_PIbline.inv_bemerk
        inv_list.invNo = gc_PIbline.invoice_nr
        inv_list.created = gc_PIbline.created
        inv_list.zeit = gc_PIbline.zeit
        inv_list.s_recid = gc_PIbline._recid

    return generate_output()