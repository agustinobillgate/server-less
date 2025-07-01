#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gc_piacct, Gl_acct, Htparam, Gl_journal, Gl_jouhdr

def gc_fundreport_chk_acctnobl(curr_date:date):

    prepare_cache ([Gc_piacct, Gl_acct, Htparam, Gl_journal])

    acctno = ""
    betrag = to_decimal("0.0")
    mm_close:date = None
    yy_close:date = None
    fibukonto:string = ""
    gc_piacct = gl_acct = htparam = gl_journal = gl_jouhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal acctno, betrag, mm_close, yy_close, fibukonto, gc_piacct, gl_acct, htparam, gl_journal, gl_jouhdr
        nonlocal curr_date

        return {"acctno": acctno, "betrag": betrag}


    gc_piacct = get_cache (Gc_piacct, {"nr": [(eq, nr)]})
    acctno = gc_piacct.fibukonto

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, acctno)]})
    betrag =  to_decimal("0")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    mm_close = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    yy_close = htparam.fdate

    if get_year(mm_close) == get_year(curr_date):
        betrag =  to_decimal(gl_acct.actual[get_month(mm_close) - 1])

    elif get_year(yy_close) == get_year(curr_date) - 2:
        betrag =  to_decimal(gl_acct.actual[get_month(mm_close) - 1])

    elif get_year(yy_close) == get_year(curr_date) - 1:
        betrag =  to_decimal(gl_acct.last_yr[get_month(mm_close) - 1])

    for gl_jouhdr, gl_journal in db_session.query(Gl_jouhdr, Gl_journal).join(Gl_journal,(Gl_journal.jnr == Gl_jouhdr.jnr) & (Gl_journal.fibukonto == acctno)).filter(
             (Gl_jouhdr.datum > mm_close)).order_by(Gl_jouhdr._recid).all():
        betrag =  to_decimal(betrag) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

    return generate_output()