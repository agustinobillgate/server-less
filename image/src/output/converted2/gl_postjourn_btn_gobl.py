from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Htparam, Gl_jouhdr, Counters, Gl_journal

g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "acct_fibukonto":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bemerk":str, "bezeich":str, "duplicate":bool, "tax_code":str, "tax_amount":str, "tot_amt":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def gl_postjourn_btn_gobl(g_list_list:[G_list], pvilanguage:int, curr_step:int, bezeich:str, credits:[decimal], debits:[decimal], remains:[decimal], refno:str, datum:date, adjust_flag:bool, journaltype:int):
    curr_jnr = 0
    msg_str = ""
    error_flag = False
    f_date:date = None
    lvcarea:str = "gl-postjourn"
    htparam = gl_jouhdr = counters = gl_journal = None

    g_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal
        nonlocal pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype


        nonlocal g_list
        nonlocal g_list_list
        return {"curr_jnr": curr_jnr, "msg_str": msg_str, "error_flag": error_flag}

    def check_date():

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal
        nonlocal pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype


        nonlocal g_list
        nonlocal g_list_list

        acct_date:date = None
        last_acctdate:date = None
        jou_date:date = None
        close_year:date = None

        if not adjust_flag:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 372)).first()
        else:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 795)).first()
        jou_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 558)).first()
        last_acctdate = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 597)).first()
        acct_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 795)).first()
        close_year = htparam.fdate

        if acct_date == None or last_acctdate == None or jou_date == None or close_year == None:
            msg_str = translateExtended ("Accounting Date is not defined.", lvcarea, "") +\
                    chr(10) +\
                    translateExtended ("(ParamNo 372, 558, 597, 975)", lvcarea, "")


            error_flag = True

            return
        else:

            if (datum <= last_acctdate) and not adjust_flag:
                msg_str = translateExtended ("Wrong Posting Date", lvcarea, "") + chr(10) + translateExtended ("Last Closing Date :", lvcarea, "") + " " + to_string(last_acctdate) + chr(10) + translateExtended ("Current Closing Date :", lvcarea, "") + " " + to_string(acct_date)
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

                gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.jtype == journaltype) & (Gl_jouhdr.datum > datum) & (Gl_jouhdr.activeflag == 0)).first()

                if gl_jouhdr:
                    msg_str = "&W" +\
                        translateExtended ("Transaction journal found with LATER posting date :", lvcarea, "") +\
                        chr(10) +\
                        to_string(gl_jouhdr.datum) + " - " + gl_jouhdr.refno +\
                        chr(10) +\
                        translateExtended ("Please re-check the entered posting date.", lvcarea, "")


    def create_header():

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal
        nonlocal pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype


        nonlocal g_list
        nonlocal g_list_list

        counters = db_session.query(Counters).filter(
                 (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "") + ""
            counters.counter_no = 25


        counters.counter = counters.counter + 1
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


    def create_journals():

        nonlocal curr_jnr, msg_str, error_flag, f_date, lvcarea, htparam, gl_jouhdr, counters, gl_journal
        nonlocal pvilanguage, curr_step, bezeich, credits, debits, remains, refno, datum, adjust_flag, journaltype


        nonlocal g_list
        nonlocal g_list_list

        for g_list in query(g_list_list, filters=(lambda g_list: g_list.duplicate == False)):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            buffer_copy(g_list, gl_journal)
            gl_journal.jnr = curr_jnr


    if curr_step == 1:
        check_date()

        return generate_output()

    elif curr_step == 2:
        create_header()
        create_journals()

    return generate_output()