from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Gl_jouhdr, Gl_acct, Exrate, Gl_journal

def closemonth2bl():
    profit:decimal = 0
    revlocal:decimal = 0
    revfremd:decimal = 0
    lost:decimal = 0
    prev_month:int = 0
    curr_month:int = 0
    curr_date:date = None
    beg_month:int = 0
    end_month:int = 0
    first_date:date = None
    wahrno:int = 0
    foreign_rate:bool = False
    double_currency:bool = False
    htparam = waehrung = gl_jouhdr = gl_acct = exrate = gl_journal = None

    gl_acc = None

    Gl_acc = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal
        nonlocal gl_acc


        nonlocal gl_acc
        return {}

    def closing_month():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal
        nonlocal gl_acc


        nonlocal gl_acc

        acct_date = 0

        def generate_inner_output():
            return acct_date

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 597)).first()
        acct_date = get_month(htparam.fdate)

        if get_day(htparam.fdate) < 15:
            acct_date = acct_date - 1

        if acct_date == 0:
            acct_date = 12


        return generate_inner_output()

    def update_glacct():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal
        nonlocal gl_acc


        nonlocal gl_acc


        Gl_acc = Gl_acct

        for gl_acc in db_session.query(Gl_acc).all():

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct._recid == gl_acc._recid)).first()
            gl_acct.actual[curr_month - 1] = 0

            if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:

                if curr_month != beg_month:
                    gl_acct.actual[curr_month - 1] = gl_acct.actual[prev_month - 1]
                else:
                    gl_acct.actual[curr_month - 1] = gl_acct.last_yr[end_month - 1]

    def process_journal(jnr:int, datum:date):

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal
        nonlocal gl_acc


        nonlocal gl_acc

        gl_journal = db_session.query(Gl_journal).filter(
                (Gl_journal.jnr == jnr) &  (Gl_journal.activeflag == 0)).first()
        while None != gl_journal:

            gl_journal = db_session.query(Gl_journal).first()

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == gl_journal.fibukonto)).first()
            gl_acct.actual[curr_month - 1] = gl_acct.actual[curr_month - 1] + gl_journal.debit - gl_journal.credit

            gl_acct = db_session.query(Gl_acct).first()

            if gl_acct.acc_type == 1:
                profit = profit - gl_journal.debit + gl_journal.credit

                if wahrno != 0:

                    exrate = db_session.query(Exrate).filter(
                            (Exrate.artnr == wahrno) &  (Exrate.datum == datum)).first()

                    if exrate and exrate.betrag != 0:
                        revlocal = revlocal + gl_journal.credit - gl_journal.debit
                        revfremd = revfremd + (gl_journal.credit - gl_journal.debit) / exrate.betrag

            elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                lost = lost + gl_journal.debit - gl_journal.credit
            gl_journal.activeflag = 1

            gl_journal = db_session.query(Gl_journal).first()

            gl_journal = db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == jnr) &  (Gl_journal.activeflag == 0)).first()

    def process_jouhdr():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal
        nonlocal gl_acc


        nonlocal gl_acc

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.datum >= first_date) &  (Gl_jouhdr.datum <= curr_date)).first()
        while None != gl_jouhdr:

            gl_jouhdr = db_session.query(Gl_jouhdr).first()
            gl_jouhdr.activeflag = 1

            gl_jouhdr = db_session.query(Gl_jouhdr).first()

            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.datum >= first_date) &  (Gl_jouhdr.datum <= curr_date)).first()

    def set_acct_modflag():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal
        nonlocal gl_acc


        nonlocal gl_acc


        Gl_acc = Gl_acct

        for gl_acc in db_session.query(Gl_acc).all():

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct._recid == gl_acc._recid)).first()
            gl_acct.modifiable = False

            gl_acct = db_session.query(Gl_acct).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 993)).first()
    end_month = htparam.finteger
    beg_month = htparam.finteger + 1

    if beg_month > 12:
        beg_month = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    first_date = fdate + timedelta(days=1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam:
        double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            wahrno = waehrungsnr
    curr_month = closing_month()
    prev_month = curr_month - 1

    if prev_month == 0:
        prev_month = 12

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 983)).first()
    htparam.flogical = True

    update_glacct()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.activeflag == 0) &  (Gl_jouhdr.datum >= first_date) &  (Gl_jouhdr.datum <= curr_date)).all():
        process_journal(gl_jouhdr.jnr, gl_jouhdr.datum)
    process_jouhdr()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 979)).first()

    gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fchar)).first()
    gl_acct.actual[curr_month - 1] = gl_acct.actual[curr_month - 1] - profit + lost

    gl_acct = db_session.query(Gl_acct).first()


    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 983)).first()
    flogical = False

    htparam = db_session.query(Htparam).first()

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 558)).first()
    htparam.fdate = curr_date
    htparam.lupdate = get_current_date()

    htparam = db_session.query(Htparam).first()

    set_acct_modflag()

    exrate = db_session.query(Exrate).filter(
                (Exrate.artnr == 99999) &  (Exrate.datum == curr_date)).first()

    if not exrate:
        exrate = Exrate()
        db_session.add(exrate)

        exrate.artnr = 99999
        exrate.datum = curr_date

    if revfremd != 0:
        exrate.betrag = round(revlocal / revfremd, 2)


    else:
        exrate.betrag = 1

    exrate = db_session.query(Exrate).first()


    return generate_output()