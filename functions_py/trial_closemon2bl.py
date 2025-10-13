#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Gl_jouhdr, Exrate, Gl_acct, Gl_journal

def trial_closemon2bl():

    prepare_cache ([Htparam, Waehrung, Exrate, Gl_acct])

    lost:Decimal = to_decimal("0.0")
    profit:Decimal = to_decimal("0.0")
    revlocal:Decimal = to_decimal("0.0")
    revfremd:Decimal = to_decimal("0.0")
    curr_date:date = None
    beg_month:int = 0
    end_month:int = 0
    foreign_rate:bool = False
    curr_month:int = 0
    prev_month:int = 0
    first_date:date = None
    double_currency:bool = False
    wahrno:int = 0
    htparam = waehrung = gl_jouhdr = exrate = gl_acct = gl_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lost, profit, revlocal, revfremd, curr_date, beg_month, end_month, foreign_rate, curr_month, prev_month, first_date, double_currency, wahrno, htparam, waehrung, gl_jouhdr, exrate, gl_acct, gl_journal

        return {}

    def update_glacct():

        nonlocal lost, profit, revlocal, revfremd, curr_date, beg_month, end_month, foreign_rate, curr_month, prev_month, first_date, double_currency, wahrno, htparam, waehrung, gl_jouhdr, exrate, gl_acct, gl_journal

        for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
            gl_acct.actual[curr_month - 1] = 0

            if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:

                if curr_month != beg_month:
                    gl_acct.actual[curr_month - 1] = gl_acct.actual[prev_month - 1]
                else:
                    gl_acct.actual[curr_month - 1] = gl_acct.last_yr[end_month - 1]


    def process_journal(jnr:int, datum:date):

        nonlocal lost, profit, revlocal, revfremd, curr_date, beg_month, end_month, foreign_rate, curr_month, prev_month, first_date, double_currency, wahrno, htparam, waehrung, gl_jouhdr, exrate, gl_acct, gl_journal

        gl_journal = get_cache (Gl_journal, {"jnr": [(eq, jnr)],"activeflag": [(eq, 0)]})
        while None != gl_journal:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)]})

            if gl_acct:
                pass
                gl_acct.actual[curr_month - 1] = gl_acct.actual[curr_month - 1] + gl_journal.debit - gl_journal.credit
                pass

                if gl_acct.acc_type == 1:
                    profit =  to_decimal(profit) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)

                    if wahrno != 0:

                        exrate = get_cache (Exrate, {"artnr": [(eq, wahrno)],"datum": [(eq, datum)]})

                        if exrate and exrate.betrag != 0:
                            revlocal =  to_decimal(revlocal) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)
                            revfremd =  to_decimal(revfremd) + to_decimal((gl_journal.credit) - to_decimal(gl_journal.debit)) / to_decimal(exrate.betrag)

                elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                    lost =  to_decimal(lost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

            curr_recid = gl_journal._recid
            gl_journal = db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == jnr) & (Gl_journal.activeflag == 0) & (Gl_journal._recid > curr_recid)).first()


    def closing_month():

        nonlocal lost, profit, revlocal, revfremd, curr_date, beg_month, end_month, foreign_rate, curr_month, prev_month, first_date, double_currency, wahrno, htparam, waehrung, gl_jouhdr, exrate, gl_acct, gl_journal

        acct_date = 0

        def generate_inner_output():
            return (acct_date)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        acct_date = get_month(htparam.fdate)

        if get_day(htparam.fdate) < 15:
            acct_date = acct_date - 1

        if acct_date == 0:
            acct_date = 12

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 993)]})
    end_month = htparam.finteger
    beg_month = htparam.finteger + 1

    if beg_month > 12:
        beg_month = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    first_date = htparam.fdate + timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam:
        double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            wahrno = waehrung.waehrungsnr
    curr_month = closing_month()
    prev_month = curr_month - 1

    if prev_month == 0:
        prev_month = 12

    htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})
    htparam.flogical = True
    update_glacct()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).order_by(Gl_jouhdr._recid).all():
        process_journal(gl_jouhdr.jnr, gl_jouhdr.datum)

    exrate = get_cache (Exrate, {"artnr": [(eq, 99999)],"datum": [(eq, curr_date)]})

    if not exrate:
        exrate = Exrate()
        db_session.add(exrate)

        exrate.artnr = 99999
        exrate.datum = curr_date

    if revfremd != 0:
        exrate.betrag = to_decimal(round(revlocal / revfremd , 2))


    else:
        exrate.betrag =  to_decimal("1")
    pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 979)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})
    gl_acct.actual[curr_month - 1] = gl_acct.actual[curr_month - 1] - profit + lost
    pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})
    htparam.flogical = False
    pass

    return generate_output()