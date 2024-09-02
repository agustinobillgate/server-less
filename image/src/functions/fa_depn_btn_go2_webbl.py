from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Htparam, Counters, Gl_journal, Fa_artikel

def fa_depn_btn_go2_webbl(g_list:[G_list], datum:date, refno:str, bezeich:str, debits:decimal, credits:decimal, remains:decimal):
    success_flag = False
    new_hdr:bool = True
    gl_acct = gl_jouhdr = htparam = counters = gl_journal = fa_artikel = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = None

    g_list_list, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool, "gl_acct1_fibukonto":str, "gl_acct1_bezeich":str}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

    Gl_acc1 = Gl_acct
    Gl_acct1 = Gl_acct
    Gl_jouhdr1 = Gl_jouhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list
        return {"success_flag": success_flag}

    def create_header():

        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = "G/L Transaction Journal"
        counters.counter = counters.counter + 1

        counters = db_session.query(Counters).first()
        gl_jouhdr.jnr = counters.counter
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 7
        new_hdr = True

    def create_journals():

        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list

        for g_list in query(g_list_list):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = counters.counter
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit = g_list.debit
            gl_journal.credit = g_list.credit
            gl_journal.bemerk = g_list.bemerk
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains = 0

        gl_jouhdr = db_session.query(Gl_jouhdr).first()
        gl_jouhdr.credit = credits
        gl_jouhdr.debit = debits
        gl_jouhdr.remain = remains

        gl_jouhdr = db_session.query(Gl_jouhdr).first()

    def update_fix_asset():

        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list
        nonlocal g_list_list

        next_date:date = None
        next_date = datum + 35
        next_date = date_mdy(get_month(next_date) , 1, get_year(next_date)) - 1

        for g_list in query(g_list_list):

            if g_list.credit != 0:

                fa_artikel = db_session.query(Fa_artikel).filter(
                        (Fa_artikel.nr == g_list.nr)).first()
                fa_artikel.posted = True

                if fa_artikel.first_depn == None:
                    fa_artikel.first_depn = datum
                fa_artikel.last_depn = datum
                fa_artikel.depn_wert = fa_artikel.depn_wert + g_list.credit
                fa_artikel.book_wert = fa_artikel.book_wert - g_list.credit
                fa_artikel.anz_depn = fa_artikel.anz_depn + 1

                if fa_artikel.book_wert > 0:
                    fa_artikel.next_depn = next_date

                fa_artikel = db_session.query(Fa_artikel).first()
            g_list_list.remove(g_list)


    create_header()
    create_journals()
    update_fix_asset()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 881)).first()
    htparam.fdate = datum

    htparam = db_session.query(Htparam).first()
    success_flag = True

    return generate_output()