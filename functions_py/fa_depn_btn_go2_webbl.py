#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, Gl_jouhdr, Htparam, Counters, Gl_journal, Fa_artikel, Queasy
from functions.next_counter_for_update import next_counter_for_update

g_list_data, G_list = create_model("G_list", {"nr":int, "jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool, "gl_acct1_fibukonto":string, "gl_acct1_bezeich":string}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})

def fa_depn_btn_go2_webbl(g_list_data:[G_list], datum:date, refno:string, bezeich:string, debits:Decimal, credits:Decimal, remains:Decimal):

    prepare_cache ([Gl_jouhdr, Htparam, Counters, Gl_journal, Fa_artikel, Queasy])

    success_flag = False
    new_hdr:bool = True
    gl_acct = gl_jouhdr = htparam = counters = gl_journal = fa_artikel = queasy = None

    gl_acc1 = gl_acct1 = gl_jouhdr1 = g_list = None

    Gl_acc1 = create_buffer("Gl_acc1",Gl_acct)
    Gl_acct1 = create_buffer("Gl_acct1",Gl_acct)
    Gl_jouhdr1 = create_buffer("Gl_jouhdr1",Gl_jouhdr)


    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""

    def generate_output():
        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel, queasy
        nonlocal datum, refno, bezeich, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        return {"g-list": g_list_data, "success_flag": success_flag}

    def create_header():

        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel, queasy
        nonlocal datum, refno, bezeich, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list


        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)


        # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})

        # if not counters:
        #     counters = Counters()
        #     db_session.add(counters)

        #     counters.counter_no = 25
        #     counters.counter_bez = "G/L Transaction Journal"
        # counters.counter = counters.counter + 1
        last_count, error_lock = get_output(next_counter_for_update(25))
        pass
        # gl_jouhdr.jnr = counters.counter
        gl_jouhdr.jnr = last_count
        gl_jouhdr.refno = refno
        gl_jouhdr.datum = datum
        gl_jouhdr.bezeich = bezeich
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 7
        new_hdr = True


    def create_journals():

        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel, queasy
        nonlocal datum, refno, bezeich, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        for g_list in query(g_list_data):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            # gl_journal.jnr = counters.counter
            gl_journal.jnr = last_count
            gl_journal.fibukonto = g_list.fibukonto
            gl_journal.debit =  to_decimal(g_list.debit)
            gl_journal.credit =  to_decimal(g_list.credit)
            gl_journal.bemerk = g_list.bemerk
            gl_journal.userinit = g_list.userinit
            gl_journal.zeit = g_list.zeit

        if remains == 0.01 or remains == - 0.01:
            remains =  to_decimal("0")
        pass
        gl_jouhdr.credit =  to_decimal(credits)
        gl_jouhdr.debit =  to_decimal(debits)
        gl_jouhdr.remain =  to_decimal(remains)
        pass
        pass


    def update_fix_asset():

        nonlocal success_flag, new_hdr, gl_acct, gl_jouhdr, htparam, counters, gl_journal, fa_artikel, queasy
        nonlocal datum, refno, bezeich, debits, credits, remains
        nonlocal gl_acc1, gl_acct1, gl_jouhdr1


        nonlocal gl_acc1, gl_acct1, gl_jouhdr1, g_list

        next_date:date = None
        depn_wert_hist:Decimal = to_decimal("0.0")
        anz_depn_hist:int = 0
        book_wert_hist:Decimal = to_decimal("0.0")
        fa_artikel_buff = None
        Fa_artikel_buff =  create_buffer("Fa_artikel_buff",Fa_artikel)
        next_date = datum + timedelta(days=35)
        next_date = date_mdy(get_month(next_date) , 1, get_year(next_date)) - timedelta(days=1)

        for g_list in query(g_list_data):

            if g_list.credit != 0:

                queasy = get_cache (Queasy, {"key": [(eq, 348)],"number1": [(eq, g_list.nr)],"date1": [(eq, datum)]})

                if not queasy:

                    fa_artikel_buff = get_cache (Fa_artikel, {"nr": [(eq, g_list.nr)]})

                    if fa_artikel_buff:
                        depn_wert_hist =  to_decimal(fa_artikel_buff.depn_wert) + to_decimal(g_list.credit)
                        anz_depn_hist = fa_artikel_buff.anz_depn + 1
                        book_wert_hist =  to_decimal(fa_artikel_buff.book_wert) - to_decimal(g_list.credit)
                        anzahl = fa_artikel_buff.anzahl
                    else:
                        depn_wert_hist = None
                        anz_depn_hist = None
                        book_wert_hist = None
                        anzahl = None
                    
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 348
                    queasy.number1 = g_list.nr
                    queasy.number2 = anzahl
                    queasy.date1 = datum
                    queasy.deci1 =  to_decimal(depn_wert_hist)
                    queasy.number3 = anz_depn_hist
                    queasy.deci2 =  to_decimal(book_wert_hist)

                fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, g_list.nr)]})

                if fa_artikel:
                    pass
                    fa_artikel.posted = True

                    if fa_artikel.first_depn == None:
                        fa_artikel.first_depn = datum
                    fa_artikel.last_depn = datum
                    fa_artikel.depn_wert =  to_decimal(fa_artikel.depn_wert) + to_decimal(g_list.credit)
                    fa_artikel.book_wert =  to_decimal(fa_artikel.book_wert) - to_decimal(g_list.credit)
                    fa_artikel.anz_depn = fa_artikel.anz_depn + 1

                    if fa_artikel.book_wert > 0:
                        fa_artikel.next_depn = next_date
                    pass
            g_list_data.remove(g_list)

    create_header()
    create_journals()
    update_fix_asset()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 881)]})
    htparam.fdate = datum
    pass
    success_flag = True

    return generate_output()