#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_jouhdr, Gl_jhdrhis, Gl_jourhis, Gl_acct, Gl_journal

def gljour_listbl(sorttype:int, from_date:date, to_date:date):

    prepare_cache ([Gl_jourhis, Gl_acct, Gl_journal])

    t_gl_jouhdr_data = []
    b2_list_data = []
    gl_jouhdr = gl_jhdrhis = gl_jourhis = gl_acct = gl_journal = None

    note_list = t_gl_jouhdr = b2_list = None

    note_list_data, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string})
    t_gl_jouhdr_data, T_gl_jouhdr = create_model_like(Gl_jouhdr)
    b2_list_data, B2_list = create_model("B2_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "jnr":int, "bezeich":string, "map_acct":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_jouhdr_data, b2_list_data, gl_jouhdr, gl_jhdrhis, gl_jourhis, gl_acct, gl_journal
        nonlocal sorttype, from_date, to_date


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_data, t_gl_jouhdr_data, b2_list_data

        return {"t-gl-jouhdr": t_gl_jouhdr_data, "b2-list": b2_list_data}

    def get_bemerk(bemerk:string):

        nonlocal t_gl_jouhdr_data, b2_list_data, gl_jouhdr, gl_jhdrhis, gl_jourhis, gl_acct, gl_journal
        nonlocal sorttype, from_date, to_date


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_data, t_gl_jouhdr_data, b2_list_data

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

        nonlocal t_gl_jouhdr_data, b2_list_data, gl_jouhdr, gl_jhdrhis, gl_jourhis, gl_acct, gl_journal
        nonlocal sorttype, from_date, to_date


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_data, t_gl_jouhdr_data, b2_list_data

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                 (Gl_jouhdr.activeflag == sorttype) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jouhdr, t_gl_jouhdr)


    def display_it1():

        nonlocal t_gl_jouhdr_data, b2_list_data, gl_jouhdr, gl_jhdrhis, gl_jourhis, gl_acct, gl_journal
        nonlocal sorttype, from_date, to_date


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_data, t_gl_jouhdr_data, b2_list_data

        for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter(
                 (Gl_jhdrhis.activeflag == sorttype) & (Gl_jhdrhis.datum >= from_date) & (Gl_jhdrhis.datum <= to_date)).order_by(Gl_jhdrhis.datum, Gl_jhdrhis.refno, Gl_jhdrhis.bezeich).all():
            t_gl_jouhdr = T_gl_jouhdr()
            t_gl_jouhdr_data.append(t_gl_jouhdr)

            buffer_copy(gl_jhdrhis, t_gl_jouhdr)


    def disp_it3():

        nonlocal t_gl_jouhdr_data, b2_list_data, gl_jouhdr, gl_jhdrhis, gl_jourhis, gl_acct, gl_journal
        nonlocal sorttype, from_date, to_date


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_data, t_gl_jouhdr_data, b2_list_data


        note_list_data.clear()

        for gl_jourhis in db_session.query(Gl_jourhis).filter(
                 (Gl_jourhis.jnr == t_gl_jouhdr.jnr)).order_by(Gl_jourhis._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_jourhis._recid
            note_list.bemerk = get_bemerk (gl_jourhis.bemerk)

        gl_jourhis_obj_list = {}
        for gl_jourhis, gl_acct in db_session.query(Gl_jourhis, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto)).filter(
                 (Gl_jourhis.jnr == t_gl_jouhdr.jnr)).order_by(Gl_jourhis.sysdate, Gl_jourhis.zeit).all():
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


    def disp_it2():

        nonlocal t_gl_jouhdr_data, b2_list_data, gl_jouhdr, gl_jhdrhis, gl_jourhis, gl_acct, gl_journal
        nonlocal sorttype, from_date, to_date


        nonlocal note_list, t_gl_jouhdr, b2_list
        nonlocal note_list_data, t_gl_jouhdr_data, b2_list_data


        note_list_data.clear()

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == t_gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

        gl_journal_obj_list = {}
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == t_gl_jouhdr.jnr)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():
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
            b2_list.map_acct = entry(1, gl_acct.userinit, ";")

    display_it()

    t_gl_jouhdr = query(t_gl_jouhdr_data, first=True)

    if t_gl_jouhdr:
        disp_it2()
    else:

        if sorttype == 1:
            display_it1()

            t_gl_jouhdr = query(t_gl_jouhdr_data, first=True)

            if t_gl_jouhdr:
                disp_it3()

    return generate_output()