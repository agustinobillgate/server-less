from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Gl_journal, Gl_acct

def gcjour_listbl(case_type:int, from_refno:str, sorttype:int, journaltype:int, jtype1:int, from_date:date, to_date:date):
    gl_jouhdr_list_list = []
    b2_list_list = []
    yy:int = 0
    gl_jouhdr = gl_journal = gl_acct = None

    note_list = gl_jouhdr_list = b2_list = None

    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":str})
    gl_jouhdr_list_list, Gl_jouhdr_list = create_model("Gl_jouhdr_list", {"datum":date, "refno":str, "bezeich":str, "debit":decimal, "credit":decimal, "remain":decimal, "jnr":int, "activeflag":int})
    b2_list_list, B2_list = create_model("B2_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "bemerk":str, "userinit":str, "sysdate":date, "zeit":int, "chginit":str, "chgdate":date, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr_list_list, b2_list_list, yy, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_list, gl_jouhdr_list_list, b2_list_list
        return {"gl-jouhdr-list": gl_jouhdr_list_list, "b2-list": b2_list_list}

    def get_bemerk(bemerk:str):

        nonlocal gl_jouhdr_list_list, b2_list_list, yy, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_list, gl_jouhdr_list_list, b2_list_list

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

        nonlocal gl_jouhdr_list_list, b2_list_list, yy, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_list, gl_jouhdr_list_list, b2_list_list

        if from_refno == "":

            if sorttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            elif sorttype == 1:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            gl_jouhdr_list = query(gl_jouhdr_list_list, first=True)

            if gl_jouhdr_list:
                disp_it2()

        elif substring(from_refno, 0, 1) == ("*").lower() :

            if sorttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch) & (func.lower(Gl_jouhdr.refno).op("~")(((from_refno).lower().replace("*",".*")))) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            elif sorttype == 1:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch == False) & (func.lower(Gl_jouhdr.refno).op("~")(((from_refno).lower().replace("*",".*")))) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            gl_jouhdr_list = query(gl_jouhdr_list_list, first=True)

            if gl_jouhdr_list:
                disp_it2()
        else:

            if sorttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch) & (func.lower(Gl_jouhdr.refno) == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            elif sorttype == 1:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch == False) & (func.lower(Gl_jouhdr.refno) == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            gl_jouhdr_list = query(gl_jouhdr_list_list, first=True)

            if gl_jouhdr_list:
                disp_it2()


    def disp_it2():

        nonlocal gl_jouhdr_list_list, b2_list_list, yy, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_list, gl_jouhdr_list_list, b2_list_list


        note_list_list.clear()

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr_list.jnr)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_list.append(note_list)

            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

        gl_journal_obj_list = []
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == gl_jouhdr_list.jnr)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():
            note_list = query(note_list_list, (lambda note_list: note_list.s_recid == to_int(gl_journal._recid)), first=True)
            if not note_list:
                continue

            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)


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


    def disp_it_2_1():

        nonlocal gl_jouhdr_list_list, b2_list_list, yy, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_list, gl_jouhdr_list_list, b2_list_list


        note_list_list.clear()

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == sorttype)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_list.append(note_list)

            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

        gl_journal_obj_list = []
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == sorttype)).order_by(Gl_journal.sysdate, Gl_journal.zeit).all():
            note_list = query(note_list_list, (lambda note_list: note_list.s_recid == to_int(gl_journal._recid)), first=True)
            if not note_list:
                continue

            if gl_journal._recid in gl_journal_obj_list:
                continue
            else:
                gl_journal_obj_list.append(gl_journal._recid)


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


    def assign_it():

        nonlocal gl_jouhdr_list_list, b2_list_list, yy, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_list, gl_jouhdr_list_list, b2_list_list


        gl_jouhdr_list = Gl_jouhdr_list()
        gl_jouhdr_list_list.append(gl_jouhdr_list)

        gl_jouhdr_list.datum = gl_jouhdr.datum
        gl_jouhdr_list.refno = gl_jouhdr.refno
        gl_jouhdr_list.bezeich = gl_jouhdr.bezeich
        gl_jouhdr_list.debit =  to_decimal(gl_jouhdr.debit)
        gl_jouhdr_list.credit =  to_decimal(gl_jouhdr.credit)
        gl_jouhdr_list.remain =  to_decimal(gl_jouhdr.remain)
        gl_jouhdr_list.jnr = gl_jouhdr.jnr
        gl_jouhdr_list.activeflag = gl_jouhdr.activeflag


    if case_type == 1:
        display_it()
    else:
        disp_it_2_1()

    return generate_output()