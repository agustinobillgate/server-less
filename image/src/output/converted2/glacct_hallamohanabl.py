#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_journal, Gl_jouhdr, Htparam, Gl_acct

def glacct_hallamohanabl(months:int, years:int):

    prepare_cache ([Gl_journal, Htparam, Gl_acct])

    fromdate:date = None
    todate:date = None
    mm:int = 0
    loc_curr = ""
    t_gl_jouhdr_list = []
    g_list_list = []
    gl_journal = gl_jouhdr = htparam = gl_acct = None

    note_list = g_list = t_gl_journal = t_gl_jouhdr = None

    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string})
    g_list_list, G_list = create_model("G_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "jnr":int, "bezeich":string, "doc_date":date, "curr":string, "post_date":date, "ref":string, "doc_header":string, "comp":string, "code1":string, "amount":Decimal, "costc":string, "profc":string, "acc_type":string, "deptnr":int, "revtype":string})
    t_gl_journal_list, T_gl_journal = create_model_like(Gl_journal)
    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr, {"b_recid":int, "code1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_list, g_list_list, gl_journal, gl_jouhdr, htparam, gl_acct
        nonlocal months, years


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_list, g_list_list, t_gl_journal_list, t_gl_jouhdr_list

        return {"loc_curr": loc_curr, "t-gl-jouhdr": t_gl_jouhdr_list, "g-list": g_list_list}

    def get_bemerk(bemerk:string):

        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_list, g_list_list, gl_journal, gl_jouhdr, htparam, gl_acct
        nonlocal months, years


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_list, g_list_list, t_gl_journal_list, t_gl_jouhdr_list

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1


    def display_it():

        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_list, g_list_list, gl_journal, gl_jouhdr, htparam, gl_acct
        nonlocal months, years


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_list, g_list_list, t_gl_journal_list, t_gl_jouhdr_list

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fromdate) & (Gl_jouhdr.datum <= todate)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)


    def disp_it2():

        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_list, g_list_list, gl_journal, gl_jouhdr, htparam, gl_acct
        nonlocal months, years


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_list, g_list_list, t_gl_journal_list, t_gl_jouhdr_list


        note_list_list.clear()
        g_list_list.clear()

        for t_gl_jouhdr in query(t_gl_jouhdr_list):

            for gl_journal in db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == t_gl_jouhdr.jnr)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():
                note_list = Note_list()
                note_list_list.append(note_list)

                note_list.s_recid = gl_journal._recid
                note_list.bemerk = get_bemerk (gl_journal.bemerk)

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)],"fs_type": [(ne, 9)],"main_nr": [(ne, 37)]})

                if gl_acct:

                    note_list = query(note_list_list, filters=(lambda note_list: note_list.s_recid == to_int(gl_journal._recid)), first=True)

                    if note_list:
                        g_list = G_list()
                        g_list_list.append(g_list)

                        g_list.fibukonto = gl_acct.fibukonto
                        g_list.debit =  to_decimal(gl_journal.debit)
                        g_list.credit =  to_decimal(gl_journal.credit)
                        g_list.bemerk = note_list.bemerk
                        g_list.userinit = gl_journal.userinit
                        g_list.sysdate = gl_journal.sysdate
                        g_list.zeit = gl_journal.zeit
                        g_list.chginit = gl_journal.chginit
                        g_list.chgdate = gl_journal.chgdate
                        g_list.jnr = gl_journal.jnr
                        g_list.bezeich = gl_acct.bezeich
                        g_list.post_date = t_gl_jouhdr.datum
                        g_list.acc_type = to_string(gl_acct.acc_type)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    if htparam:

        if htparam.fchar.lower()  == ("RP").lower() :
            loc_curr = "IDR"

        elif htparam.fchar.lower()  == ("US$").lower() :
            loc_curr = "USD"


        else:
            loc_curr = htparam.fchar


    fromdate = date_mdy(months, 1, years)
    todate = add_interval(fromdate, 1, 'MONTH') - timedelta(days=1)
    display_it()

    t_gl_jouhdr = query(t_gl_jouhdr_list, first=True)

    if t_gl_jouhdr:
        disp_it2()

    return generate_output()