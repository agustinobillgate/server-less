from functions.additional_functions import *
import decimal
from datetime import date
from models import Gc_piacct, Gl_acct, Htparam, Gl_journal, Gl_jouhdr

def gc_fundreport_chk_acctnobl(curr_date:date):
    acctno = ""
    betrag = 0
    mm_close:date = None
    yy_close:date = None
    fibukonto:str = ""
    gc_piacct = gl_acct = htparam = gl_journal = gl_jouhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal acctno, betrag, mm_close, yy_close, fibukonto, gc_piacct, gl_acct, htparam, gl_journal, gl_jouhdr


        return {"acctno": acctno, "betrag": betrag}


    gc_piacct = db_session.query(Gc_piacct).filter(
            (Gc_piacct.nr == nr)).first()
    acctno = gc_piacct.fibukonto

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == acctno)).first()
    betrag = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    mm_close = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 795)).first()
    yy_close = htparam.fdate

    if get_year(mm_close) == get_year(curr_date):
        betrag = gl_acct.actual[get_month(mm_close) - 1]

    elif get_year(yy_close) == get_year(curr_date) - 2:
        betrag = gl_acct.actual[get_month(mm_close) - 1]

    elif get_year(yy_close) == get_year(curr_date) - 1:
        betrag = gl_acct.last_yr[get_month(mm_close) - 1]

    for gl_jouhdr, gl_journal in db_session.query(Gl_jouhdr, Gl_journal).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) &  (Gl_journal.fibukonto == acctno)).filter(
            (Gl_jouhdr.datum > mm_close)).all():
        betrag = betrag + gl_journal.debit - gl_journal.credit

    return generate_output()