from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_acct

def gljour_list2bl(jnr:int):
    b2_list_list = []
    gl_journal = gl_acct = None

    note_list = b2_list = None

    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":str})
    b2_list_list, B2_list = create_model("B2_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "jnr":int, "bezeich":str})
    gl_acct_list_list, GL_list = create_model("GL_list", {"s_recid":int, "fibukonto":str})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b2_list_list, gl_journal, gl_acct


        nonlocal note_list, b2_list
        nonlocal note_list_list, b2_list_list
        return {"b2-list": b2_list_list}

    def get_bemerk(bemerk:str):

        nonlocal b2_list_list, gl_journal, gl_acct


        nonlocal note_list, b2_list
        nonlocal note_list_list, b2_list_list

        n:int = 0
        s1:str = ""
        bemerk = replace_str(bemerk, chr(10) , " ")
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1

    def disp_it2():

        nonlocal b2_list_list, gl_journal, gl_acct


        nonlocal note_list, b2_list
        nonlocal note_list_list, b2_list_list, gl_acct_list_list


        note_list_list.clear()

        query_results = db_session.query(Gl_journal).filter((Gl_journal.jnr == jnr)).all()
        for gl_journal in query_results:
            note_list = Note_list()
            note_list_list.append(note_list)
            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

        for gl_journal in query_results:
            gl_acct = db_session.query(Gl_acct).filter(Gl_acct.fibukonto==gl_journal.fibukonto).first()
            
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


        # gl_journal_obj_list = []
        # for gl_journal, gl_acct, note_list in \
        #     db_session.query(Gl_journal, Gl_acct, Note_list)\
        #     .join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto))\
        #     .join(Note_list,(Note_list.s_recid == Gl_journal._recid)).filter(
        #         (Gl_journal.jnr == jnr)).all():
            
        #     if gl_journal._recid in gl_journal_obj_list:
        #         continue
        #     else:
        #         gl_journal_obj_list.append(gl_journal._recid)


        #     b2_list = B2_list()
        #     b2_list_list.append(b2_list)

        #     b2_list.fibukonto = gl_acct.fibukonto
        #     b2_list.debit = gl_journal.debit
        #     b2_list.credit = gl_journal.credit
        #     b2_list.bemerk = note_list.bemerk
        #     b2_list.userinit = gl_journal.userinit
        #     b2_list.sysdate = gl_journal.sysdate
        #     b2_list.zeit = gl_journal.zeit
        #     b2_list.chginit = gl_journal.chginit
        #     b2_list.chgdate = gl_journal.chgdate
        #     b2_list.jnr = gl_journal.jnr
        #     b2_list.bezeich = gl_acct.bezeich
            
    disp_it2()

    return generate_output()