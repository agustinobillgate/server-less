from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Gl_jouhdr, Gl_acct, Exrate, Gl_journal

def closemonth2bl():
    profit:decimal = to_decimal("0.0")
    revlocal:decimal = to_decimal("0.0")
    revfremd:decimal = to_decimal("0.0")
    lost:decimal = to_decimal("0.0")
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


    db_session = local_storage.db_session

    def generate_output():
        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        return {}

    def closing_month():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        acct_date = 0

        def generate_inner_output():
            return (acct_date)


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

        gl_acc = None
        Gl_acc =  create_buffer("Gl_acc",Gl_acct)

        for gl_acc in db_session.query(Gl_acc).order_by(Gl_acc._recid).all():

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct._recid == gl_acc._recid)).first()
            gl_acct.actual[curr_month - 1] = 0

            if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:

                if curr_month != beg_month:
                    gl_acct.actual[curr_month - 1] = gl_acct.actual[prev_month - 1]
                else:
                    gl_acct.actual[curr_month - 1] = gl_acct.last_yr[end_month - 1]

                if gl_acct.fibukonto.lower()  == ("10001006").lower() :
                    pass


    def process_journal(jnr:int, datum:date):

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        bacct = None
        bjournal = None
        Bacct =  create_buffer("Bacct",Gl_acct)
        Bjournal =  create_buffer("Bjournal",Gl_journal)

        gl_journal_obj_list = []
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == jnr) & (Gl_journal.activeflag == 0)).order_by(Gl_journal.fibukonto).all():
            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)

            if gl_acct.fibukonto.lower()  == ("10001006").lower() :
                pass

            bacct = db_session.query(Bacct).filter(
                     (Bacct._recid == gl_acct._recid)).first()
            bacct.actual[curr_month - 1] = bacct.actual[curr_month - 1] +\
                    gl_journal.debit - gl_journal.credit

            if gl_acct.acc_type == 1:
                profit =  to_decimal(profit) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)

                if wahrno != 0:

                    exrate = db_session.query(Exrate).filter(
                             (Exrate.artnr == wahrno) & (Exrate.datum == datum)).first()

                    if exrate and exrate.betrag != 0:
                        revlocal =  to_decimal(revlocal) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)
                        revfremd =  to_decimal(revfremd) + to_decimal((gl_journal.credit) - to_decimal(gl_journal.debit)) / to_decimal(exrate.betrag)

            elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                lost =  to_decimal(lost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

            bjournal = db_session.query(Bjournal).filter(
                     (Bjournal._recid == gl_journal._recid)).first()
            bjournal.activeflag = 1
            pass
            pass


    def process_jouhdr():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).first()
        while None != gl_jouhdr:
            gl_jouhdr.activeflag = 1

            curr_recid = gl_jouhdr._recid
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).filter(Gl_jouhdr._recid > curr_recid).first()


    def set_acct_modflag():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        gl_acc = None
        Gl_acc =  create_buffer("Gl_acc",Gl_acct)

        for gl_acc in db_session.query(Gl_acc).order_by(Gl_acc._recid).all():

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct._recid == gl_acc._recid)).first()
            gl_acct.modifiable = False

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
    first_date = htparam.fdate + timedelta(days=1)

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
            wahrno = waehrung.waehrungsnr
    curr_month = closing_month()
    prev_month = curr_month - 1

    if prev_month == 0:
        prev_month = 12

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).first()
    htparam.flogical = True

    update_glacct()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).order_by(Gl_jouhdr._recid).all():
        process_journal(gl_jouhdr.jnr, gl_jouhdr.datum)
    process_jouhdr()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 979)).first()

    gl_acct = db_session.query(Gl_acct).filter(
             (Gl_acct.fibukonto == fchar)).first()
    gl_acct.actual[curr_month - 1] = gl_acct.actual[curr_month - 1] - profit + lost

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).first()
    htparam.flogical = False

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 558)).first()
    htparam.fdate = curr_date
    htparam.lupdate = get_current_date()

    set_acct_modflag()

    exrate = db_session.query(Exrate).filter(
                 (Exrate.artnr == 99999) & (Exrate.datum == curr_date)).first()

    if not exrate:
        exrate = Exrate()
        db_session.add(exrate)

        exrate.artnr = 99999
        exrate.datum = curr_date

    if revfremd != 0:
        exrate.betrag = to_decimal(round(revlocal / revfremd , 2))


    else:
        exrate.betrag =  to_decimal("1")


    return generate_output()