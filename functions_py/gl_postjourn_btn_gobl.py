#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Gl_jouhdr, Counters, Gl_journal, Queasy
from functions.next_counter_for_update import next_counter_for_update

g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "acct_fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "bemerk":string, "bezeich":string, "duplicate":bool, "tax_code":string, "tax_amount":string, "tot_amt":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_postjourn_btn_gobl(g_list_data:[G_list], pvilanguage:int, curr_step:int, bezeich:string, credits:[Decimal], debits:[Decimal], remains:[Decimal], 
                          refno:string, datum:date, adjust_flag:bool, journaltype:int):

    prepare_cache ([Htparam, Gl_jouhdr, Counters, Gl_journal, Queasy])

    curr_jnr = 0
    msg_str = ""
    error_flag = False
    f_date:date = None
    lvcarea:string = "gl-postjourn"
    htparam = gl_jouhdr = counters = gl_journal = queasy = None

    g_list = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    bezeich = bezeich.strip()
    refno = refno.strip()


    def generate_output():
        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal, queasy
        nonlocal pvilanguage, curr_step, bezeich, refno, datum, adjust_flag, journaltype


        nonlocal g_list

        return {"curr_jnr": curr_jnr, "msg_str": msg_str, "error_flag": error_flag}

    def check_date():

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal, queasy
        nonlocal pvilanguage, curr_step, bezeich, refno, datum, adjust_flag, journaltype
        nonlocal last_count, error_lock


        nonlocal g_list

        acct_date:date = None
        last_acctdate:date = None
        jou_date:date = None
        close_year:date = None

        if not adjust_flag:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 372)]})
        else:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
        jou_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
        last_acctdate = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
        acct_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
        close_year = htparam.fdate

        if acct_date == None or last_acctdate == None or jou_date == None or close_year == None:
            msg_str = translateExtended ("Accounting Date is not defined.", lvcarea, "") +\
                    chr_unicode(10) +\
                    translateExtended ("(ParamNo 372, 558, 597, 975)", lvcarea, "")


            error_flag = True

            return
        else:

            if (datum <= last_acctdate) and not adjust_flag:
                msg_str = translateExtended ("Wrong Posting Date", lvcarea, "") + chr_unicode(10) + translateExtended ("Last Closing Date :", lvcarea, "") + " " + to_string(last_acctdate) + chr_unicode(10) + translateExtended ("Current Closing Date :", lvcarea, "") + " " + to_string(acct_date)
                error_flag = True

                return

            if datum > get_current_date():
                msg_str = translateExtended ("Posting Date can not be later THEN TODAY.", lvcarea, "")
                error_flag = True

                return
            f_date = get_output(htpdate(404))

            if f_date != None and journaltype == 5 and (datum <= f_date):
                msg_str = translateExtended ("Wrong Posting Date.", lvcarea, "") + " " + translateExtended ("Last G/C Closing Date :", lvcarea, "") + " " + to_string(f_date, "99/99/9999")
                error_flag = True

                return

            if not adjust_flag:

                gl_jouhdr = get_cache (Gl_jouhdr, {"jtype": [(eq, journaltype)],"datum": [(gt, datum)],"activeflag": [(eq, 0)]})

                if gl_jouhdr:
                    msg_str = "&W" +\
                        translateExtended ("Transaction journal found with LATER posting date :", lvcarea, "") +\
                        chr_unicode(10) +\
                        to_string(gl_jouhdr.datum) + " - " + gl_jouhdr.refno +\
                        chr_unicode(10) +\
                        translateExtended ("Please re-check the entered posting date.", lvcarea, "")


    def create_header():

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal, queasy
        nonlocal pvilanguage, curr_step, bezeich, refno, datum, adjust_flag, journaltype
        nonlocal last_count, error_lock


        nonlocal g_list

        # Rd, 24/11/2025, get counters dengan for update
        # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
        counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 25)).with_for_update().first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "") + ""
            counters.counter_no = 25


        counters.counter = counters.counter + 1

        pass
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = counters.counter

        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.jtype = journaltype
        gl_jouhdr.batch = (journaltype > 0)
        gl_jouhdr.credit =  to_decimal(credits)
        gl_jouhdr.debit =  to_decimal(debits)
        curr_jnr = counters.counter


        pass
        update_queasy_345(curr_jnr, datum, bezeich)


    def create_journals():

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal, queasy
        nonlocal pvilanguage, curr_step, bezeich, refno, datum, adjust_flag, journaltype
        nonlocal last_count, error_lock


        nonlocal g_list

        for g_list in query(g_list_data, filters=(lambda g_list: g_list.duplicate == False)):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            buffer_copy(g_list, gl_journal)
            gl_journal.jnr = curr_jnr


            pass


    def update_queasy_345(jnr:int, datum:date, bezeich:string):

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal, queasy
        nonlocal pvilanguage, curr_step, refno, adjust_flag, journaltype


        nonlocal g_list

        queasy = get_cache (Queasy, {"key": [(eq, 345)],"number1": [(eq, jnr)],"date1": [(eq, datum)]})

        if queasy:
            pass
            queasy.logi1 = True
            queasy.logi2 = False
            queasy.logi3 = False


            pass
            pass
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 345
            queasy.number1 = jnr
            queasy.number2 = get_current_time_in_seconds()
            queasy.char1 = bezeich
            queasy.date1 = datum
            queasy.logi1 = True
            queasy.logi2 = False
            queasy.logi3 = False


            pass


    if curr_step == 1:
        check_date()

        return generate_output()

    elif curr_step == 2:
        create_header()
        create_journals()

    return generate_output()