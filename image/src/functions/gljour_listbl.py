from functions.additional_functions import *
import decimal
from datetime import date
from models import Gl_jouhdr, Gl_journal, Gl_acct

def gljour_listbl(sorttype:int, from_date:date, to_date:date):
    t_gl_jouhdr_list = []
    b2_list_list = []
    gl_jouhdr = gl_journal = gl_acct = None

    note_list = t_gl_jouhdr = b2_list = None

    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":str})
    t_gl_jouhdr_list, T_gl_jouhdr = create_model_like(Gl_jouhdr)
    b2_list_list, B2_list = create_model("B2_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "jnr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_jouhdr_list, b2_list_list, gl_jouhdr, gl_journal, gl_acct


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_list, t_gl_jouhdr_list, b2_list_list
        return {"t-gl-jouhdr": t_gl_jouhdr_list, "b2-list": b2_list_list}

    def get_bemerk(bemerk:str):

        nonlocal t_gl_jouhdr_list, b2_list_list, gl_jouhdr, gl_journal, gl_acct


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_list, t_gl_jouhdr_list, b2_list_list

        n:int = 0
        s1:str = ""
        bemerk = replace_str(bemerk, chr(10) , " ")
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1

    def display_it():

        nonlocal t_gl_jouhdr_list, b2_list_list, gl_jouhdr, gl_journal, gl_acct


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_list, t_gl_jouhdr_list, b2_list_list

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.activeflag == sorttype) and  (Gl_jouhdr.batch == False) and  (Gl_jouhdr.datum >= from_date) and  (Gl_jouhdr.datum <= to_date)).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_list.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)

    def disp_it2():

        nonlocal t_gl_jouhdr_list, b2_list_list, gl_jouhdr, gl_journal, gl_acct
        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_list, t_gl_jouhdr_list, b2_list_list

        note_list_list.clear()

        query_results = db_session.query(Gl_journal, Gl_acct)\
                            .join(Gl_acct, (Gl_acct.fibukonto==Gl_journal.fibukonto))\
                            .order_by(Gl_journal.sysdate)\
                            .order_by(Gl_journal.zeit)\
                            .filter((Gl_journal.jnr == t_gl_jouhdr.jnr)).all()
        
        for gl_journal, gl_acct in query_results:
            print("GL:", gl_journal.fibukonto, gl_journal.bemerk)
            note_list = Note_list()
            note_list_list.append(note_list)
            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

            
        # note_list_list_indexed = indexed_list(note_list_list, ["s_recid", "bemerk", "add_note"] )
        
        # for gl_journal in db_session.query(Gl_journal).filter(
        #         (Gl_journal.jnr == t_gl_jouhdr.jnr)).all():
        #     note_list = Note_list()
        #     note_list_list.append(note_list)

        #     note_list.s_recid = gl_journal._recid
        #     note_list.bemerk = get_bemerk (gl_journal.bemerk)

        gl_journal_obj_list = []
        for gl_journal, gl_acct in query_results:
            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)
        
        # for gl_journal, gl_acct, note_list in db_session.query(Gl_journal, Gl_acct, Note_list)\
        #         .join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto))\
        #         .join(Note_list,(Note_list.s_recid == Gl_journal._recid))\
        #         .filter((Gl_journal.jnr == t_gl_jouhdr.jnr)).all():
            
            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)

            b2_list = B2_list()
            b2_list_list.append(b2_list)

            b2_list.fibukonto = gl_acct.fibukonto
            b2_list.debit = gl_journal.debit
            b2_list.credit = gl_journal.credit
            b2_list.bemerk = note_list.bemerk
            b2_list.userinit = gl_journal.userinit
            b2_list.sysdate = gl_journal.sysdate
            b2_list.zeit = gl_journal.zeit
            b2_list.chginit = gl_journal.chginit
            b2_list.chgdate = gl_journal.chgdate
            b2_list.jnr = gl_journal.jnr
            b2_list.bezeich = gl_acct.bezeich


    display_it()

    t_gl_jouhdr = query(t_gl_jouhdr_list, first=True)

    if t_gl_jouhdr:
        disp_it2()

    return generate_output()