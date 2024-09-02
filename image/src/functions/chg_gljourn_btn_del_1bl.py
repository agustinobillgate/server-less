from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_journal, Gl_jouhdr, Bediener, Res_history

def chg_gljourn_btn_del_1bl(jnr:int, rec_id:int, user_init:str, fibukonto:str):
    debits = 0
    credits = 0
    remains = 0
    str:str = ""
    datum:date = None
    refno:str = ""
    debit:decimal = 0
    credit:decimal = 0
    gl_journal = gl_jouhdr = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal debits, credits, remains, str, datum, refno, debit, credit, gl_journal, gl_jouhdr, bediener, res_history


        return {"debits": debits, "credits": credits, "remains": remains}


    gl_journal = db_session.query(Gl_journal).filter(
            (Gl_journal._recid == rec_id)).first()

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jnr == jnr)).first()
    datum = gl_jouhdr.datum
    refno = gl_jouhdr.refno
    debit = gl_journal.debit
    credit = gl_journal.credit
    gl_jouhdr.debit = gl_jouhdr.debit - gl_journal.debit
    gl_jouhdr.credit = gl_jouhdr.credit - gl_journal.credit
    gl_jouhdr.remain = gl_jouhdr.debit - gl_jouhdr.credit

    gl_jouhdr = db_session.query(Gl_jouhdr).first()
    debits = gl_jouhdr.debit
    credits = gl_jouhdr.credit
    remains = gl_jouhdr.remain

    gl_journal = db_session.query(Gl_journal).first()
    db_session.delete(gl_journal)
    str = "Delete Journal, Date: " + to_string(datum) + ", AcctNo: " + fibukonto + ", refno: " + refno

    if debit != 0:
        str = str + ", debit: " + to_string(debit)
    else:
        str = str + ", credit: " + to_string(credit)

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = str
        res_history.action = "G/L"

        res_history = db_session.query(Res_history).first()


    return generate_output()