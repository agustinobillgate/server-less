#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
from models import Gl_journal, Gl_jouhdr, Gl_acct, Gl_main

def glacct_export2bl(fdate:date, tdate:date):

    prepare_cache ([Gl_journal, Gl_acct])

    fromdate:date = None
    todate:date = None
    mm:int = 0
    loc_curr = ""
    t_gl_jouhdr_data = []
    g_list_data = []
    gl_journal = gl_jouhdr = gl_acct = gl_main = None

    note_list = g_list = t_gl_journal = t_gl_jouhdr = None

    note_list_data, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string})
    g_list_data, G_list = create_model("G_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "jnr":int, "bezeich":string, "doc_date":date, "curr":string, "post_date":date, "ref":string, "doc_header":string, "comp":string, "code1":string, "amount":Decimal, "costc":string, "profc":string, "acc_type":string, "deptnr":int, "revtype":string, "datum":date, "refno":string})
    t_gl_journal_data, T_gl_journal = create_model_like(Gl_journal)
    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr, {"b_recid":int, "code1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_data, g_list_data, gl_journal, gl_jouhdr, gl_acct, gl_main
        nonlocal fdate, tdate


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_data, g_list_data, t_gl_journal_data, t_gl_jouhdr_data

        return {"loc_curr": loc_curr, "t-gl-jouhdr": t_gl_jouhdr_data, "g-list": g_list_data}

    def get_bemerk(bemerk:string):

        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_data, g_list_data, gl_journal, gl_jouhdr, gl_acct, gl_main
        nonlocal fdate, tdate


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_data, g_list_data, t_gl_journal_data, t_gl_jouhdr_data

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

        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_data, g_list_data, gl_journal, gl_jouhdr, gl_acct, gl_main
        nonlocal fdate, tdate


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_data, g_list_data, t_gl_journal_data, t_gl_jouhdr_data

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.datum >= fromdate) & (Gl_jouhdr.datum <= todate)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)


    def disp_it2():

        nonlocal fromdate, todate, mm, loc_curr, t_gl_jouhdr_data, g_list_data, gl_journal, gl_jouhdr, gl_acct, gl_main
        nonlocal fdate, tdate


        nonlocal note_list, g_list, t_gl_journal, t_gl_jouhdr
        nonlocal note_list_data, g_list_data, t_gl_journal_data, t_gl_jouhdr_data


        note_list_data.clear()
        g_list_data.clear()

        for t_gl_jouhdr in query(t_gl_jouhdr_data):

            for gl_journal in db_session.query(Gl_journal).filter(
                     (Gl_journal.jnr == t_gl_jouhdr.jnr)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)]})

                gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})

                gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})
                g_list = G_list()
                g_list_data.append(g_list)

                g_list.fibukonto = gl_acct.fibukonto
                g_list.bemerk = get_bemerk (gl_journal.bemerk)
                g_list.userinit = gl_journal.userinit
                g_list.sysdate = gl_journal.sysdate
                g_list.zeit = gl_journal.zeit
                g_list.chginit = gl_journal.chginit
                g_list.chgdate = gl_journal.chgdate
                g_list.jnr = gl_journal.jnr
                g_list.bezeich = gl_acct.bemerk
                g_list.post_date = t_gl_jouhdr.datum
                g_list.acc_type = to_string(gl_acct.acc_type)
                g_list.deptnr = gl_acct.deptnr

                if gl_jouhdr:
                    g_list.datum = gl_jouhdr.datum


                g_list.refno = gl_jouhdr.refno

                if gl_journal.debit != 0 and gl_journal.credit != 0:
                    g_list.debit =  to_decimal(gl_journal.debit)


                    g_list = G_list()
                    g_list_data.append(g_list)

                    g_list.fibukonto = gl_acct.fibukonto
                    g_list.bemerk = get_bemerk (gl_journal.bemerk)
                    g_list.userinit = gl_journal.userinit
                    g_list.sysdate = gl_journal.sysdate
                    g_list.zeit = gl_journal.zeit
                    g_list.chginit = gl_journal.chginit
                    g_list.chgdate = gl_journal.chgdate
                    g_list.jnr = gl_journal.jnr
                    g_list.bezeich = gl_acct.bemerk
                    g_list.post_date = t_gl_jouhdr.datum
                    g_list.acc_type = to_string(gl_acct.acc_type)
                    g_list.deptnr = gl_acct.deptnr
                    g_list.credit =  to_decimal(gl_journal.credit)

                    if gl_jouhdr:
                        g_list.datum = gl_jouhdr.datum


                    g_list.refno = gl_jouhdr.refno
                else:
                    g_list.debit =  to_decimal(gl_journal.debit)
                    g_list.credit =  to_decimal(gl_journal.credit)


    loc_curr = get_output(htpchar(152))
    fromdate = fdate
    todate = tdate


    display_it()

    t_gl_jouhdr = query(t_gl_jouhdr_data, first=True)

    if t_gl_jouhdr:
        disp_it2()

    return generate_output()