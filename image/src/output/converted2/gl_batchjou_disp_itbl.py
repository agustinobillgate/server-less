from functions.additional_functions import *
import decimal
from models import Gl_journal, Gl_acct

def gl_batchjou_disp_itbl(jnr:int):
    b2_list_list = []
    gl_journal = gl_acct = None

    b2_list = note_list = None

    b2_list_list, B2_list = create_model("B2_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bezeich":str})
    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b2_list_list, gl_journal, gl_acct
        nonlocal jnr


        nonlocal b2_list, note_list
        nonlocal b2_list_list, note_list_list

        return {"b2-list": b2_list_list}

    def get_bemerk(bemerk:str):

        nonlocal b2_list_list, gl_journal, gl_acct
        nonlocal jnr


        nonlocal b2_list, note_list
        nonlocal b2_list_list, note_list_list

        n:int = 0
        s1:str = ""
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk


    def assign_b2():

        nonlocal b2_list_list, gl_journal, gl_acct
        nonlocal jnr


        nonlocal b2_list, note_list
        nonlocal b2_list_list, note_list_list


        b2_list = B2_list()
        b2_list_list.append(b2_list)

        b2_list.fibukonto = gl_acct.fibukonto
        b2_list.debit =  to_decimal(gl_journal.debit)
        b2_list.credit =  to_decimal(gl_journal.credit)
        b2_list.bemerk = note_list.bemerk
        b2_list.userinit = gl_journal.userinit
        b2_list.sysdate = gl_journal.sysdate
        b2_list.zeit = gl_journal.zeit
        b2_list.chginit = gl_journal.chginit
        b2_list.chgdate = gl_journal.chgdate
        b2_list.bezeich = gl_acct.bezeich


    note_list_list.clear()

    for gl_journal in db_session.query(Gl_journal).filter(
             (Gl_journal.jnr == jnr)).order_by(Gl_journal._recid).all():
        note_list = Note_list()
        note_list_list.append(note_list)

        note_list.s_recid = gl_journal._recid
        note_list.bemerk = get_bemerk (gl_journal.bemerk)

    gl_journal_obj_list = []
    for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
             (Gl_journal.jnr == jnr)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():
        note_list = query(note_list_list, (lambda note_list: note_list.s_recid == to_int(gl_journal._recid)), first=True)
        if not note_list:
            continue

        if gl_journal._recid in gl_journal_obj_list:
            continue
        else:
            gl_journal_obj_list.append(gl_journal._recid)


        assign_b2()

    return generate_output()