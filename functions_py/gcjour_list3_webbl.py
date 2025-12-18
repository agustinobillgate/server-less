# using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - fix python indentation
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jouhdr, Gl_journal, Gl_acct

t_payload_list_data, T_payload_list = create_model(
    "T_payload_list", {
        "v_mode": int,
        "fibukonto": str,
        "sysdate": date,
        "zeit": int,
        "rec_id": Decimal
    }
)


def gcjour_list3_webbl(t_payload_list_data: [T_payload_list], case_type: int, from_refno: string, sorttype: int, journaltype: int, jtype1: int, from_date: date, to_date: date, jnr: int):

    prepare_cache([Gl_jouhdr, Gl_acct])

    gl_jouhdr_list_data = []
    b2_list_data = []
    t_output_list_data = []
    yy: int = 0
    jtype = [
        "From F/O",
        "From A/R",
        "From inventory",
        "From A/P",
        "From General Cashier",
        "No Transfer",
        "From Fixed Asset",
        "From Purchasing"
    ]
    gl_jouhdr = gl_journal = gl_acct = None

    note_list = gl_jouhdr_list = b2_list = t_payload_list = t_output_list = None

    note_list_data, Note_list = create_model(
        "Note_list", {
            "s_recid": int,
            "bemerk": str
        }
    )
    gl_jouhdr_list_data, Gl_jouhdr_list = create_model(
        "Gl_jouhdr_list", {
            "datum": date,
            "refno": str,
            "bezeich": str,
            "debit": Decimal,
            "credit": Decimal,
            "remain": Decimal,
            "jnr": int,
            "activeflag": int,
            "jtype": str
        }
    )
    b2_list_data, B2_list = create_model(
        "B2_list", {
            "fibukonto": str,
            "debit": Decimal,
            "credit": Decimal,
            "bemerk": str,
            "userinit": str,
            "sysdate": date,
            "zeit": int,
            "chginit": str,
            "chgdate": date,
            "bezeich": str,
            "map_acct": str,
            "rec_id": Decimal
        }
    )
    t_output_list_data, T_output_list = create_model(
        "T_output_list", {
            "total_data": int
        }
    )

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_jouhdr_list_data, b2_list_data, t_output_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr
        nonlocal note_list, gl_jouhdr_list, b2_list, t_payload_list, t_output_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data, t_output_list_data

        return {
            "gl-jouhdr-list": gl_jouhdr_list_data,
            "b2-list": b2_list_data,
            "t-output-list": t_output_list_data
        }

    def get_bemerk(bemerk: string):
        nonlocal gl_jouhdr_list_data, b2_list_data, t_output_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr
        nonlocal note_list, gl_jouhdr_list, b2_list, t_payload_list, t_output_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data, t_output_list_data

        n: int = 0
        s1: string
        bemerk = replace_str(bemerk, chr_unicode(10), " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1

    def display_it():
        nonlocal gl_jouhdr_list_data, b2_list_data, t_output_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr
        nonlocal note_list, gl_jouhdr_list, b2_list, t_payload_list, t_output_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data, t_output_list_data

        if from_refno == "":
            if sorttype == 0:
                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.activeflag == sorttype) &
                    ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) &
                    (Gl_jouhdr.batch) &
                    (Gl_jouhdr.datum >= from_date) &
                    (Gl_jouhdr.datum <= to_date)
                ).order_by(Gl_jouhdr.datum,
                           Gl_jouhdr.refno,
                           Gl_jouhdr.bezeich
                           ).all():
                    assign_it()

            elif sorttype == 1:
                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.activeflag == sorttype) &
                        ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) &
                        (Gl_jouhdr.batch == False) &
                        (Gl_jouhdr.datum >= from_date) &
                        (Gl_jouhdr.datum <= to_date)
                ).order_by(Gl_jouhdr.datum,
                           Gl_jouhdr.refno,
                           Gl_jouhdr.bezeich
                           ).all():
                    assign_it()

            if jnr == 0:
                gl_jouhdr_list = query(gl_jouhdr_list_data, first=True)
                if gl_jouhdr_list:
                    disp_it2()
            else:
                gl_jouhdr_list = query(gl_jouhdr_list_data, filters=(
                    lambda gl_jouhdr_list: gl_jouhdr_list.jnr == jnr), first=True)

                if gl_jouhdr_list:
                    disp_it2()

        elif str(substring(from_refno, 0, 1)) == ("*"):
            if sorttype == 0:
                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.activeflag == sorttype) &
                        ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) &
                        (Gl_jouhdr.batch) &
                        (matches(Gl_jouhdr.refno, (from_refno))) &
                        (Gl_jouhdr.datum >= from_date) &
                        (Gl_jouhdr.datum <= to_date)
                ).order_by(Gl_jouhdr.datum,
                           Gl_jouhdr.refno,
                           Gl_jouhdr.bezeich
                           ).all():
                    assign_it()

            elif sorttype == 1:
                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.activeflag == sorttype) &
                        ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) &
                        (Gl_jouhdr.batch == False) &
                        (matches(Gl_jouhdr.refno, (from_refno))) &
                        (Gl_jouhdr.datum >= from_date) &
                        (Gl_jouhdr.datum <= to_date)
                ).order_by(Gl_jouhdr.datum,
                           Gl_jouhdr.refno,
                           Gl_jouhdr.bezeich
                           ).all():
                    assign_it()

            if jnr == 0:
                gl_jouhdr_list = query(gl_jouhdr_list_data, first=True)

                if gl_jouhdr_list:
                    disp_it2()

            else:
                gl_jouhdr_list = query(gl_jouhdr_list_data, filters=(
                    lambda gl_jouhdr_list: gl_jouhdr_list.jnr == jnr), first=True)

                if gl_jouhdr_list:
                    disp_it2()
        else:
            if sorttype == 0:
                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.activeflag == sorttype) &
                        ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) &
                        (Gl_jouhdr.batch) &
                        (Gl_jouhdr.refno == (from_refno).lower()) &
                        (Gl_jouhdr.datum >= from_date) &
                        (Gl_jouhdr.datum <= to_date)
                ).order_by(Gl_jouhdr.datum,
                           Gl_jouhdr.refno,
                           Gl_jouhdr.bezeich
                           ).all():
                    assign_it()

            elif sorttype == 1:
                for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                        (Gl_jouhdr.activeflag == sorttype) &
                        ((Gl_jouhdr.jtype == journaltype) | (Gl_jouhdr.jtype == jtype1)) &
                        (Gl_jouhdr.batch == False) &
                        (Gl_jouhdr.refno == (from_refno).lower()) &
                        (Gl_jouhdr.datum >= from_date) &
                        (Gl_jouhdr.datum <= to_date)
                ).order_by(Gl_jouhdr.datum,
                           Gl_jouhdr.refno,
                           Gl_jouhdr.bezeich
                           ).all():
                    assign_it()

            if jnr == 0:
                gl_jouhdr_list = query(gl_jouhdr_list_data, first=True)

                if gl_jouhdr_list:
                    disp_it2()
            else:
                gl_jouhdr_list = query(gl_jouhdr_list_data, filters=(
                    lambda gl_jouhdr_list: gl_jouhdr_list.jnr == jnr), first=True)

                if gl_jouhdr_list:
                    disp_it2()

    def disp_it2():
        nonlocal gl_jouhdr_list_data, b2_list_data, t_output_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr
        nonlocal note_list, gl_jouhdr_list, b2_list, t_payload_list, t_output_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data, t_output_list_data

        count_data: int = 0
        count_i: int = 0

        if t_payload_list.v_mode == 0:

            gl_journal = get_cache(Gl_journal, {
                "jnr": [(eq, gl_jouhdr_list.jnr)]})
            while gl_journal:
                count_data = count_data + 1

                curr_recid = gl_journal._recid
                gl_journal = db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == gl_jouhdr_list.jnr) &
                    (Gl_journal._recid > curr_recid)
                ).first()
            t_output_list = T_output_list()
            t_output_list_data.append(t_output_list)

            t_output_list.total_data = count_data

            if count_data >= 3000:

                # gl_journal_query = (
                #     db_session.query(Gl_journal, Gl_acct)
                #     .join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto))
                #     .filter(
                #         (Gl_journal.jnr == gl_jouhdr_list.jnr)
                #     ).order_by(Gl_acct.fibukonto,
                #                Gl_journal.sysdate,
                #                Gl_journal.zeit))

                gl_journal_obj_list = {}
                for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                        (Gl_journal.jnr == gl_jouhdr_list.jnr)
                    ).order_by(Gl_acct.fibukonto,
                               Gl_journal.sysdate,
                               Gl_journal.zeit).all():
                    if gl_journal_obj_list.get(gl_journal._recid):
                        continue
                    else:
                        gl_journal_obj_list[gl_journal._recid] = True

                    count_i = count_i + 1
                    b2_list = B2_list()
                    b2_list_data.append(b2_list)

                    b2_list.fibukonto = gl_acct.fibukonto
                    b2_list.debit = to_decimal(gl_journal.debit)
                    b2_list.credit = to_decimal(gl_journal.credit)
                    b2_list.bemerk = get_bemerk(gl_journal.bemerk)
                    b2_list.userinit = gl_journal.userinit
                    b2_list.sysdate = gl_journal.sysdate
                    b2_list.zeit = gl_journal.zeit
                    b2_list.chginit = gl_journal.chginit
                    b2_list.chgdate = gl_journal.chgdate
                    b2_list.bezeich = gl_acct.bezeich
                    b2_list.rec_id = gl_journal._recid

                    if num_entries(gl_acct.userinit, ";") > 1:
                        b2_list.map_acct = entry(1, gl_acct.userinit, ";")
                    else:
                        b2_list.map_acct = " "

                    if count_i == 3000:
                        break
            else:

                gl_journal_obj_list = {}
                for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                        (Gl_journal.jnr == gl_jouhdr_list.jnr)).order_by(Gl_acct.fibukonto, Gl_journal.sysdate, Gl_journal.zeit).all():

                    if gl_journal_obj_list.get(gl_journal._recid):
                        continue
                    else:
                        gl_journal_obj_list[gl_journal._recid] = True

                    b2_list = B2_list()
                    b2_list_data.append(b2_list)

                    b2_list.fibukonto = gl_acct.fibukonto
                    b2_list.debit = to_decimal(gl_journal.debit)
                    b2_list.credit = to_decimal(gl_journal.credit)
                    b2_list.bemerk = get_bemerk(gl_journal.bemerk)
                    b2_list.userinit = gl_journal.userinit
                    b2_list.sysdate = gl_journal.sysdate
                    b2_list.zeit = gl_journal.zeit
                    b2_list.chginit = gl_journal.chginit
                    b2_list.chgdate = gl_journal.chgdate
                    b2_list.bezeich = gl_acct.bezeich
                    b2_list.rec_id = gl_journal._recid

                    if num_entries(gl_acct.userinit, ";") > 1:
                        b2_list.map_acct = entry(1, gl_acct.userinit, ";")
                    else:
                        b2_list.map_acct = " "
        else:
            gl_journal_obj_list = {}

            # gl_journal_query_2 = (
            #     db_session.query(Gl_journal, Gl_acct)
            #     .join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto))
            #     .filter(
            #         (Gl_journal.jnr == gl_jouhdr_list.jnr) &
            #         (Gl_journal.fibukonto >= t_payload_list.fibukonto) &
            #         (Gl_journal.sysdate >= t_payload_list.sysdate) &
            #         (Gl_journal.zeit >= t_payload_list.zeit) &
            #         (Gl_journal._recid != to_int(b2_list.rec_id))
            #     )
            #     .order_by(Gl_acct.fibukonto,
            #               Gl_journal.sysdate,
            #               Gl_journal.zeit))

            for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                    (Gl_journal.jnr == gl_jouhdr_list.jnr) &
                    (Gl_journal.fibukonto >= t_payload_list.fibukonto) &
                    (Gl_journal.sysdate >= t_payload_list.sysdate) &
                    (Gl_journal.zeit >= t_payload_list.zeit) &
                    (Gl_journal._recid != to_int(b2_list.rec_id))
            ).order_by(Gl_acct.fibukonto,
                       Gl_journal.sysdate,
                       Gl_journal.zeit).all():
                if gl_journal_obj_list.get(gl_journal._recid):
                    continue
                else:
                    gl_journal_obj_list[gl_journal._recid] = True

                count_i = count_i + 1
                b2_list = B2_list()
                b2_list_data.append(b2_list)

                b2_list.fibukonto = gl_acct.fibukonto
                b2_list.debit = to_decimal(gl_journal.debit)
                b2_list.credit = to_decimal(gl_journal.credit)
                b2_list.bemerk = get_bemerk(gl_journal.bemerk)
                b2_list.userinit = gl_journal.userinit
                b2_list.sysdate = gl_journal.sysdate
                b2_list.zeit = gl_journal.zeit
                b2_list.chginit = gl_journal.chginit
                b2_list.chgdate = gl_journal.chgdate
                b2_list.bezeich = gl_acct.bezeich
                b2_list.rec_id = gl_journal._recid

                if num_entries(gl_acct.userinit, ";") > 1:
                    b2_list.map_acct = entry(1, gl_acct.userinit, ";")
                else:
                    b2_list.map_acct = " "

                if count_i == 3000:
                    break

    def disp_it_2_1():
        nonlocal gl_jouhdr_list_data, b2_list_data, t_output_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr
        nonlocal note_list, gl_jouhdr_list, b2_list, t_payload_list, t_output_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data, t_output_list_data

        gl_journal_obj_list = {}
        # gl_journal_query = (
        #     db_session.query(Gl_journal, Gl_acct)
        #     .join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto))
        #     .filter(
        #         (Gl_journal.jnr == sorttype)
        #     )
        #     .order_by(Gl_acct.fibukonto,
        #               Gl_journal.sysdate,
        #               Gl_journal.zeit))
        for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct, (Gl_acct.fibukonto == Gl_journal.fibukonto)).filter(
                (Gl_journal.jnr == sorttype)
            ).order_by(Gl_acct.fibukonto,
                       Gl_journal.sysdate,
                       Gl_journal.zeit).all():
            if gl_journal_obj_list.get(gl_journal._recid):
                continue
            else:
                gl_journal_obj_list[gl_journal._recid] = True

            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.fibukonto = gl_acct.fibukonto
            b2_list.debit = to_decimal(gl_journal.debit)
            b2_list.credit = to_decimal(gl_journal.credit)
            b2_list.bemerk = get_bemerk(gl_journal.bemerk)
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
        nonlocal gl_jouhdr_list_data, b2_list_data, t_output_list_data, yy, jtype, gl_jouhdr, gl_journal, gl_acct
        nonlocal case_type, from_refno, sorttype, journaltype, jtype1, from_date, to_date, jnr
        nonlocal note_list, gl_jouhdr_list, b2_list, t_payload_list, t_output_list
        nonlocal note_list_data, gl_jouhdr_list_data, b2_list_data, t_output_list_data

        gl_jouhdr_list = Gl_jouhdr_list()
        gl_jouhdr_list_data.append(gl_jouhdr_list)

        gl_jouhdr_list.datum = gl_jouhdr.datum
        gl_jouhdr_list.refno = gl_jouhdr.refno
        gl_jouhdr_list.bezeich = gl_jouhdr.bezeich
        gl_jouhdr_list.debit = to_decimal(gl_jouhdr.debit)
        gl_jouhdr_list.credit = to_decimal(gl_jouhdr.credit)
        gl_jouhdr_list.remain = to_decimal(gl_jouhdr.remain)
        gl_jouhdr_list.jnr = gl_jouhdr.jnr
        gl_jouhdr_list.activeflag = gl_jouhdr.activeflag

        if gl_jouhdr.jtype == 0:
            gl_jouhdr_list.jtype = jtype[5]

        else:
            gl_jouhdr_list.jtype = jtype[gl_jouhdr.jtype - 1]

    t_payload_list = query(t_payload_list_data, first=True)

    if not t_payload_list:
        return generate_output()

    if case_type == 1:
        display_it()
    else:
        disp_it_2_1()

    return generate_output()
