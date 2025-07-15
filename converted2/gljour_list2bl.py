#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal, Gl_acct, Gl_jourhis

def gljour_list2bl(jnr:int):

    prepare_cache ([Gl_journal, Gl_acct, Gl_jourhis])

    b2_list_data = []
    gl_journal = gl_acct = gl_jourhis = None

    note_list = b2_list = None

    note_list_data, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string})
    b2_list_data, B2_list = create_model("B2_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "jnr":int, "bezeich":string, "map_acct":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b2_list_data, gl_journal, gl_acct, gl_jourhis
        nonlocal jnr


        nonlocal note_list, b2_list
        nonlocal note_list_data, b2_list_data

        return {"b2-list": b2_list_data}

    def get_bemerk(bemerk:string):

        nonlocal b2_list_data, gl_journal, gl_acct, gl_jourhis
        nonlocal jnr


        nonlocal note_list, b2_list
        nonlocal note_list_data, b2_list_data

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1


    def disp_it2():

        nonlocal b2_list_data, gl_journal, gl_acct, gl_jourhis
        nonlocal jnr


        nonlocal note_list, b2_list
        nonlocal note_list_data, b2_list_data


        note_list_data.clear()

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == jnr)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

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


            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.fibukonto = gl_acct.fibukonto
            b2_list.debit =  to_decimal(gl_journal.debit)
            b2_list.credit =  to_decimal(gl_journal.credit)
            b2_list.bemerk = note_list.bemerk
            b2_list.userinit = gl_journal.userinit
            b2_list.sysdate = gl_journal.sysdate
            b2_list.zeit = gl_journal.zeit
            b2_list.chginit = gl_journal.chginit
            b2_list.chgdate = gl_journal.chgdate
            b2_list.jnr = gl_journal.jnr
            b2_list.bezeich = gl_acct.bezeich


    def disp_it3():

        nonlocal b2_list_data, gl_journal, gl_acct, gl_jourhis
        nonlocal jnr


        nonlocal note_list, b2_list
        nonlocal note_list_data, b2_list_data


        note_list_data.clear()

        for gl_jourhis in db_session.query(Gl_jourhis).filter(
                 (Gl_jourhis.jnr == jnr)).order_by(Gl_jourhis._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_jourhis._recid
            note_list.bemerk = get_bemerk (gl_jourhis.bemerk)

        gl_jourhis_obj_list = {}
        for gl_jourhis, gl_acct in db_session.query(Gl_jourhis, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto)).filter(
                 (Gl_jourhis.jnr == jnr)).order_by(Gl_jourhis.sysdate, Gl_jourhis.zeit).all():
            note_list = query(note_list_data, (lambda note_list: note_list.s_recid == to_int(gl_jourhis._recid)), first=True)
            if not note_list:
                continue

            if gl_jourhis_obj_list.get(gl_jourhis._recid):
                continue
            else:
                gl_jourhis_obj_list[gl_jourhis._recid] = True


            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.fibukonto = gl_acct.fibukonto
            b2_list.debit =  to_decimal(gl_jourhis.debit)
            b2_list.credit =  to_decimal(gl_jourhis.credit)
            b2_list.bemerk = note_list.bemerk
            b2_list.userinit = gl_jourhis.userinit
            b2_list.sysdate = gl_jourhis.sysdate
            b2_list.zeit = gl_jourhis.zeit
            b2_list.chginit = gl_jourhis.chginit
            b2_list.chgdate = gl_jourhis.chgdate
            b2_list.jnr = gl_jourhis.jnr
            b2_list.bezeich = gl_acct.bezeich

            if num_entries(gl_acct.userinit, ";") > 1:
                b2_list.map_acct = entry(1, gl_acct.userinit, ";")
            else:
                b2_list.map_acct = " "


    disp_it2()

    b2_list = query(b2_list_data, first=True)

    if not b2_list:
        disp_it3()

    return generate_output()