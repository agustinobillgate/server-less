from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Htparam, L_lieferant, Gl_journal, Gl_acct

def prepare_chg_gljourn_1bl(jnr:int):
    closedate = None
    f_integer = 0
    gst_flag = False
    b1_list_list = []
    t_gl_jouhdr_list = []
    gl_jouhdr = htparam = l_lieferant = gl_journal = gl_acct = None

    t_gl_jouhdr = note_list = g_list = b1_list = None

    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr, {"rec_id":int})
    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":str, "add_note":str, "orig_note":str})
    g_list_list, G_list = create_model("G_list", {"jnr":int, "fibukonto":str, "debit":decimal, "credit":decimal, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "duplicate":bool}, {"sysdate": get_current_date(), "chgdate": None, "duplicate": True})
    b1_list_list, B1_list = create_model("B1_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "bezeich":str, "chginit":str, "chgdate":date, "sysdate":date, "zeit":int, "activeflag":int, "rec_gl_journ":int, "tax_code":str, "tax_amount":str, "tot_amt":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal closedate, f_integer, gst_flag, b1_list_list, t_gl_jouhdr_list, gl_jouhdr, htparam, l_lieferant, gl_journal, gl_acct


        nonlocal t_gl_jouhdr, note_list, g_list, b1_list
        nonlocal t_gl_jouhdr_list, note_list_list, g_list_list, b1_list_list
        return {"closedate": closedate, "f_integer": f_integer, "gst_flag": gst_flag, "b1-list": b1_list_list, "t-gl-jouhdr": t_gl_jouhdr_list}

    def create_notelist():

        nonlocal closedate, f_integer, gst_flag, b1_list_list, t_gl_jouhdr_list, gl_jouhdr, htparam, l_lieferant, gl_journal, gl_acct
        nonlocal t_gl_jouhdr, note_list, g_list, b1_list
        nonlocal t_gl_jouhdr_list, note_list_list, g_list_list, b1_list_list

        s1:str = ""
        s2:str = ""
        n:int = 0

        for gl_journal in db_session.query(Gl_journal).filter(
                (Gl_journal.jnr == jnr)).all():
            note_list = Note_list()
            note_list_list.append(note_list)

            note_list.s_recid = gl_journal._recid
            n = 1 + get_index(gl_journal.bemerk, ";&&")

            if n > 0:
                s1 = substring(gl_journal.bemerk, 0, n - 1)
                note_list.s_recid = gl_journal._recid
                note_list.bemerk = substring(gl_journal.bemerk, 0, n - 1)
                note_list.add_note = substring(gl_journal.bemerk, n - 1, len(gl_journal.bemerk))

            else:
                note_list.s_recid = gl_journal._recid
                note_list.bemerk = gl_journal.bemerk


            note_list.orig_note = note_list.bemerk

    def disp_it1():
        nonlocal closedate, f_integer, gst_flag, b1_list_list, t_gl_jouhdr_list, gl_jouhdr, htparam, l_lieferant, gl_journal, gl_acct
        nonlocal t_gl_jouhdr, note_list, g_list, b1_list
        nonlocal t_gl_jouhdr_list, note_list_list, g_list_list, b1_list_list
        # print(Note_list)

        gl_journal_obj_list = []

        query_results = db_session.query(Gl_journal, Gl_acct)\
            .join(Gl_acct, (Gl_acct.fibukonto==Gl_journal.fibukonto)).filter((Gl_journal.jnr == jnr)).all()
        
        note_list_list_indexed = indexed_list(note_list_list, ["s_recid", "bemerk", "add_note"] )
    
        gl_journal_obj_list = []
        for gl_journal, gl_acct in query_results:
            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)
            # wbuff = get_indexed_record(wbuff_list_indexed,{'zknr':("==",h_artikel.zwkum),'departement':("==",h_artikel.departement)}, first=True)
            notes = get_indexed_record(note_list_list_indexed, {'s_recid': ("==", gl_journal._recid)} , first=True)

            b1_list = B1_list()
            b1_list_list.append(b1_list)
            b1_list.fibukonto = gl_journal.fibukonto
            b1_list.debit = gl_journal.debit 
            b1_list.credit = gl_journal.credit
            b1_list.bemerk = notes.bemerk
            b1_list.bezeich = gl_acct.bezeich
            b1_list.chginit      = gl_journal.chginit
            b1_list.chgdate      = gl_journal.chgdate
            b1_list.activeflag   = gl_journal.activeflag
            b1_list._recid = gl_journal._recid
            b1_list.sysdate      = gl_journal.sysdate
            b1_list.zeit         = gl_journal.zeit

            if num_entries(gl_acct.bemerk, ";") > 1:
                b1_list.tax_code = entry(1, gl_acct.bemerk, ";")

    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
            (Gl_jouhdr.jnr == jnr)).first()

    if not gl_jouhdr:

        return generate_output()
    t_gl_jouhdr = T_gl_jouhdr()
    t_gl_jouhdr_list.append(t_gl_jouhdr)

    buffer_copy(gl_jouhdr, t_gl_jouhdr)
    t_gl_jouhdr.rec_id = gl_jouhdr._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()

    if get_month(htparam.fdate) > get_month(closedate):
        closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1012)).first()

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1:
        f_integer = htparam.finteger
    g_list = G_list()
    g_list_list.append(g_list)

    create_notelist()
    disp_it1()

    l_lieferant = db_session.query(L_lieferant).filter(
            (func.lower(L_lieferant.firma) == "GST")).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()