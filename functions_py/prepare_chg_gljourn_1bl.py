#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Htparam, L_lieferant, Gl_journal, Gl_acct

def prepare_chg_gljourn_1bl(jnr:int):

    prepare_cache ([Htparam, Gl_journal, Gl_acct])

    closedate = None
    f_integer = 0
    gst_flag = False
    b1_list_data = []
    t_gl_jouhdr_data = []
    gl_jouhdr = htparam = l_lieferant = gl_journal = gl_acct = None

    t_gl_jouhdr = note_list = g_list = b1_list = None

    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr, {"rec_id":int})
    note_list_data, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string, "add_note":string, "orig_note":string})
    g_list_data, G_list = create_model("G_list", {"jnr":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    b1_list_data, B1_list = create_model("B1_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "bezeich":string, "chginit":string, "chgdate":date, "sysdate":date, "zeit":int, "activeflag":int, "rec_gl_journ":int, "tax_code":string, "tax_amount":string, "tot_amt":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal closedate, f_integer, gst_flag, b1_list_data, t_gl_jouhdr_data, gl_jouhdr, htparam, l_lieferant, gl_journal, gl_acct
        nonlocal jnr


        nonlocal t_gl_jouhdr, note_list, g_list, b1_list
        nonlocal t_gl_jouhdr_data, note_list_data, g_list_data, b1_list_data

        return {"closedate": closedate, "f_integer": f_integer, "gst_flag": gst_flag, "b1-list": b1_list_data, "t-gl-jouhdr": t_gl_jouhdr_data}

    def create_notelist():

        nonlocal closedate, f_integer, gst_flag, b1_list_data, t_gl_jouhdr_data, gl_jouhdr, htparam, l_lieferant, gl_journal, gl_acct
        nonlocal jnr


        nonlocal t_gl_jouhdr, note_list, g_list, b1_list
        nonlocal t_gl_jouhdr_data, note_list_data, g_list_data, b1_list_data

        s1:string = ""
        s2:string = ""
        n:int = 0

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == jnr)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_journal._recid
            n = get_index(gl_journal.bemerk, ";&&")

            if n > 0:
                s1 = substring(gl_journal.bemerk, 0, n - 1)
                note_list.s_recid = gl_journal._recid
                note_list.bemerk = substring(gl_journal.bemerk, 0, n - 1)
                note_list.add_note = substring(gl_journal.bemerk, n - 1, length(gl_journal.bemerk))


            else:
                note_list.s_recid = gl_journal._recid
                note_list.bemerk = gl_journal.bemerk


            note_list.orig_note = note_list.bemerk


    def disp_it1():

        nonlocal closedate, f_integer, gst_flag, b1_list_data, t_gl_jouhdr_data, gl_jouhdr, htparam, l_lieferant, gl_journal, gl_acct
        nonlocal jnr


        nonlocal t_gl_jouhdr, note_list, g_list, b1_list
        nonlocal t_gl_jouhdr_data, note_list_data, g_list_data, b1_list_data

        gl_journal_obj_list = {}
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == jnr)).order_by(Gl_acct.fibukonto, Gl_journal.sysdate, Gl_journal.zeit).all():
            note_list = query(note_list_data, (lambda note_list: note_list.s_recid == to_int(gl_journal._recid)), first=True)
            if not note_list:
                continue

            if gl_journal_obj_list.get(gl_journal._recid):
                continue
            else:
                gl_journal_obj_list[gl_journal._recid] = True


            b1_list = B1_list()
            b1_list_data.append(b1_list)

            b1_list.fibukonto = gl_acct.fibukonto
            b1_list.debit =  to_decimal(gl_journal.debit)
            b1_list.credit =  to_decimal(gl_journal.credit)
            b1_list.bemerk = note_list.bemerk
            b1_list.bezeich = gl_acct.bezeich
            b1_list.chginit = gl_journal.chginit
            b1_list.chgdate = gl_journal.chgdate
            b1_list.activeflag = gl_journal.activeflag
            b1_list.rec_gl_journ = gl_journal._recid
            b1_list.sysdate = gl_journal.sysdate
            b1_list.zeit = gl_journal.zeit

            if num_entries(gl_acct.bemerk, ";") > 1:
                b1_list.tax_code = entry(1, gl_acct.bemerk, ";")

    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, jnr)]})

    if not gl_jouhdr:

        return generate_output()
    t_gl_jouhdr = T_gl_jouhdr()
    t_gl_jouhdr_data.append(t_gl_jouhdr)

    buffer_copy(gl_jouhdr, t_gl_jouhdr)
    t_gl_jouhdr.rec_id = gl_jouhdr._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if get_month(htparam.fdate) > get_month(closedate):
        closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1:
        f_integer = htparam.finteger
    g_list = G_list()
    g_list_data.append(g_list)

    create_notelist()
    disp_it1()

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()