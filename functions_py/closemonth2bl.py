#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 10/10/2025
# fchar -> htparam.fchar
#------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Gl_jouhdr, Gl_acct, Exrate, Gl_journal
from sqlalchemy.orm import flag_modified

def closemonth2bl():

    prepare_cache ([Htparam, Waehrung, Gl_acct, Exrate, Gl_journal])

    profit:Decimal = to_decimal("0.0")
    revlocal:Decimal = to_decimal("0.0")
    revfremd:Decimal = to_decimal("0.0")
    lost:Decimal = to_decimal("0.0")
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


        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
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

            # gl_acct = get_cache (Gl_acct, {"_recid": [(eq, gl_acc._recid)]})
            gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct._recid == gl_acc._recid)).with_for_update().first()
            gl_acct.actual[curr_month - 1] = 0

            if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:

                if curr_month != beg_month:
                    gl_acct.actual[curr_month - 1] = gl_acct.actual[prev_month - 1]
                else:
                    gl_acct.actual[curr_month - 1] = gl_acct.last_yr[end_month - 1]

                if gl_acct.fibukonto  == ("10001006") :
                    pass
        flag_modified(gl_acct, "actual")


    def process_journal(jnr:int, datum:date):

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        bacct = None
        bjournal = None
        Bacct =  create_buffer("Bacct",Gl_acct)
        Bjournal =  create_buffer("Bjournal",Gl_journal)

        gl_journal_obj_list = {}
        gl_journal = Gl_journal()
        gl_acct = Gl_acct()
        
        # Rd, 25/11/2025, with_for_update added
        for gl_journal.debit, gl_journal.credit, gl_journal._recid, gl_acct.acc_type, gl_acct.actual, gl_acct.last_yr, gl_acct._recid, gl_acct.fibukonto, gl_acct.modifiable in db_session.query(Gl_journal.debit, Gl_journal.credit, Gl_journal._recid, Gl_acct.acc_type, Gl_acct.actual, Gl_acct.last_yr, Gl_acct._recid, Gl_acct.fibukonto, Gl_acct.modifiable).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == jnr) & (Gl_journal.activeflag == 0)).with_for_update().order_by(Gl_journal.fibukonto).all():
            if gl_journal_obj_list.get(gl_journal._recid):
                continue
            else:
                gl_journal_obj_list[gl_journal._recid] = True

            if gl_acct.fibukonto  == ("10001006") :
                pass

            # Rd, 25/11/2025, with_for_update added
            # bacct = get_cache (Gl_acct, {"_recid": [(eq, gl_acct._recid)]})
            bacct = db_session.query(Gl_acct).filter(
                         (Gl_acct._recid == gl_acct._recid)).with_for_update().first()
            bacct.actual[curr_month - 1] = bacct.actual[curr_month - 1] +\
                    gl_journal.debit - gl_journal.credit
            flag_modified(bacct, "actual")
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

            # Rd, 25/11/2025, with_for_update added
            # bjournal = get_cache (Gl_journal, {"_recid": [(eq, gl_journal._recid)]})
            bjournal = db_session.query(Gl_journal).filter(
                         (Gl_journal._recid == gl_journal._recid)).with_for_update
            bjournal.activeflag = 1
            pass
            pass
            pass


    def process_jouhdr():

        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        # gl_jouhdr = get_cache (Gl_jouhdr, {"activeflag": [(eq, 0)],"datum": [(ge, first_date),(le, curr_date)]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).order_by(Gl_jouhdr._recid).first()
        while None != gl_jouhdr:
            pass
            gl_jouhdr.activeflag = 1
            pass

            curr_recid = gl_jouhdr._recid
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date) & (Gl_jouhdr._recid > curr_recid)).with_for_update().first()


    def set_acct_modflag():
        # Rd, 25/11/2025, with_for_update added
        nonlocal profit, revlocal, revfremd, lost, prev_month, curr_month, curr_date, beg_month, end_month, first_date, wahrno, foreign_rate, double_currency, htparam, waehrung, gl_jouhdr, gl_acct, exrate, gl_journal

        gl_acc = None
        Gl_acc =  create_buffer("Gl_acc",Gl_acct)

        for gl_acc in db_session.query(Gl_acc).order_by(Gl_acc._recid).with_for_update().all():

            gl_acct = get_cache (Gl_acct, {"_recid": [(eq, gl_acc._recid)]})
            gl_acct.modifiable = False
            pass

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

    # htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})
    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).with_for_update().first()

    if htparam:
        pass
        htparam.flogical = True


        pass
        pass
    update_glacct()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.activeflag == 0) & (Gl_jouhdr.datum >= first_date) & (Gl_jouhdr.datum <= curr_date)).order_by(Gl_jouhdr._recid).all():
        process_journal(gl_jouhdr.jnr, gl_jouhdr.datum)
    process_jouhdr()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 979)]})

    # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})
    gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == htparam.fchar)).with_for_update().first()    
    gl_acct.actual[curr_month - 1] = gl_acct.actual[curr_month - 1] - profit + lost
    
    flag_modified(gl_acct, "actual")

    pass

    # htparam = get_cache (Htparam, {"paramnr": [(eq, 983)]})
    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 983)).with_for_update().first()

    if htparam:
        pass
        htparam.flogical = False


        pass
        pass

    # Rd, 24/11/2025, update htparam dengan next_counter_for_update
    # htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 558)).with_for_update().first()

    if htparam:
        pass
        htparam.fdate = curr_date
        htparam.lupdate = get_current_date()
        pass
        pass
    set_acct_modflag()

    # Rd 24/11/2025, update exrate dengan next_counter_for_update
    # exrate = get_cache (Exrate, {"artnr": [(eq, 99999)],"datum": [(eq, curr_date)]})
    exrate = db_session.query(Exrate).filter(
                 (Exrate.artnr == 99999) & (Exrate.datum == curr_date)).with_for_update().first()

    if not exrate:
        exrate = Exrate()
        db_session.add(exrate)

        exrate.artnr = 99999
        exrate.datum = curr_date

        if revfremd != 0:
            exrate.betrag = to_decimal(round(revlocal / revfremd , 2))


        else:
            exrate.betrag =  to_decimal("1")
    else:
        pass

        if revfremd != 0:
            exrate.betrag = to_decimal(round(revlocal / revfremd , 2))


        else:
            exrate.betrag =  to_decimal("1")
        pass


    return generate_output()