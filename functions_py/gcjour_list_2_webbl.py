#using conversion tools version: 1.0.0.117
#---------------------------------------------
# Rd, 17-July-25
# replace jtype -> gl_jouhdr.jtype
#---------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Gl_journal, Gl_acct

def gcjour_list_2_webbl(case_type:int, from_refno:string, sorttype:int, journaltype:int, jtype1:int, from_date:date, to_date:date, jnr:int):

    prepare_cache ([Gl_jouhdr, Gl_journal, Gl_acct])

    gl_jouhdr_list_data = []
    b2_list_data = []
    yy:int = 0
    jtype:List[string] = create_empty_list(6,"")
    gl_jouhdr = gl_journal = gl_acct = None

    note_list = gl_jouhdr_list = b2_list = None

    note_list_data, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string})
    gl_jouhdr_list_data, Gl_jouhdr_list = create_model("Gl_jouhdr_list", {"datum":date, "refno":string, "bezeich":string, "debit":Decimal, "credit":Decimal, "remain":Decimal, "jnr":int, "activeflag":int, "jtype":string})
    b2_list_data, B2_list = create_model("B2_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "bemerk":string, "userinit":string, "sysdate":date, "zeit":int, "chginit":string, "chgdate":date, "bezeich":string, "map_acct":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr_list_data, b2_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data

        return {"gl-jouhdr-list": gl_jouhdr_list_data, "b2-list": b2_list_data}

    def get_bemerk(bemerk:string):

        nonlocal gl_jouhdr_list_data, b2_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data

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

        nonlocal gl_jouhdr_list_data, b2_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data

        if from_refno == "":

            if sorttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            elif sorttype == 1:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            if jnr == 0:

                gl_jouhdr_list = query(gl_jouhdr_list_data, first=True)

                if gl_jouhdr_list:
                    disp_it2()
            else:

                gl_jouhdr_list = query(gl_jouhdr_list_data, filters=(lambda gl_jouhdr_list: gl_jouhdr_list.jnr == jnr), first=True)

                if gl_jouhdr_list:
                    disp_it2()

        elif substring(from_refno, 0, 1) == ("*").lower() :

            if sorttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch) & (matches(Gl_jouhdr.refno,(from_refno))) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            elif sorttype == 1:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch == False) & (matches(Gl_jouhdr.refno,(from_refno))) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            if jnr == 0:

                gl_jouhdr_list = query(gl_jouhdr_list_data, first=True)

                if gl_jouhdr_list:
                    disp_it2()
            else:

                gl_jouhdr_list = query(gl_jouhdr_list_data, filters=(lambda gl_jouhdr_list: gl_jouhdr_list.jnr == jnr), first=True)

                if gl_jouhdr_list:
                    disp_it2()
        else:

            if sorttype == 0:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch) & (Gl_jouhdr.refno == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            elif sorttype == 1:

                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                         (Gl_jouhdr.activeflag == sorttype) & ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) & (Gl_jouhdr.batch == False) & (Gl_jouhdr.refno == (from_refno).lower()) & (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_jouhdr.bezeich).all():
                    assign_it()


            if jnr == 0:

                gl_jouhdr_list = query(gl_jouhdr_list_data, first=True)

                if gl_jouhdr_list:
                    disp_it2()
            else:

                gl_jouhdr_list = query(gl_jouhdr_list_data, filters=(lambda gl_jouhdr_list: gl_jouhdr_list.jnr == jnr), first=True)

                if gl_jouhdr_list:
                    disp_it2()


    def disp_it2():

        nonlocal gl_jouhdr_list_data, b2_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data


        note_list_data.clear()

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr_list.jnr)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

        gl_journal_obj_list = {}
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == gl_jouhdr_list.jnr)).order_by(Gl_acct.fibukonto, Gl_journal.sysdate, Gl_journal.zeit).all():
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
            b2_list.bezeich = gl_acct.bezeich

            if num_entries(gl_acct.userinit, ";") > 1:
                b2_list.map_acct = entry(1, gl_acct.userinit, ";")
            else:
                b2_list.map_acct = " "


    def disp_it_2_1():

        nonlocal gl_jouhdr_list_data, b2_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data


        note_list_data.clear()

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == sorttype)).order_by(Gl_journal._recid).all():
            note_list = Note_list()
            note_list_data.append(note_list)

            note_list.s_recid = gl_journal._recid
            note_list.bemerk = get_bemerk (gl_journal.bemerk)

        gl_journal_obj_list = {}
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                 (Gl_journal.jnr == sorttype)).order_by(Gl_acct.fibukonto, Gl_journal.sysdate, Gl_journal.zeit).all():
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
            b2_list.bezeich = gl_acct.bezeich

            if num_entries(gl_acct.userinit, ";") > 1:
                b2_list.map_acct = entry(1, gl_acct.userinit, ";")
            else:
                b2_list.map_acct = " "


    def assign_it():

        nonlocal gl_jouhdr_list_data, b2_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr


        nonlocal note_list, gl_jouhdr_list, b2_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data


        gl_jouhdr_list = Gl_jouhdr_list()
        gl_jouhdr_list_data.append(gl_jouhdr_list)

        gl_jouhdr_list.datum = gl_jouhdr.datum
        gl_jouhdr_list.refno = gl_jouhdr.refno
        gl_jouhdr_list.bezeich = gl_jouhdr.bezeich
        gl_jouhdr_list.debit =  to_decimal(gl_jouhdr.debit)
        gl_jouhdr_list.credit =  to_decimal(gl_jouhdr.credit)
        gl_jouhdr_list.remain =  to_decimal(gl_jouhdr.remain)
        gl_jouhdr_list.jnr = gl_jouhdr.jnr
        gl_jouhdr_list.activeflag = gl_jouhdr.activeflag

        # if gl_jouhdr.jtype == 0:
        #     gl_jouhdr_list.jtype = jtype[5]
        # else:
        #     gl_jouhdr_list.jtype = jtype[gl_jouhdr.jtype - 1]
        # Rd, 17-July-26, jtype -> gl_jouhdr.jtype
        if gl_jouhdr.jtype == 0:
            gl_jouhdr_list.jtype = gl_jouhdr.jtype[5]
        else:
            # gl_jouhdr_list.jtype = gl_jouhdr.jtype[gl_jouhdr.jtype - 1]
            jtype_index = gl_jouhdr.jtype - 1  # convert 1-based to 0-based
            print("Jtype:", jtype_index, gl_jouhdr.jtype)
            if 0 <= jtype_index < len(jtype):
                gl_jouhdr_list.jtype = jtype[jtype_index]
            else:
                raise IndexError(f"Invalid jtype index: {jtype_index}")

    jtype[0] = "From F/O"
    jtype[1] = "From A/R"
    jtype[2] = "From inventory"
    jtype[3] = "From A/P"
    jtype[4] = "From General Cashier"
    jtype[5] = "No Transfer"

    if case_type == 1:
        display_it()
    else:
        disp_it_2_1()

    return generate_output()