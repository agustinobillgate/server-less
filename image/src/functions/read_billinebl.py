from functions.additional_functions import *
from sqlalchemy import func
from models import Bill_line, Artikel

t_bill_line_list = []
bill_line = artikel = None

t_bill_line = None

t_bill_line_list, T_bill_line = create_model_like(Bill_line)


def read_billinebl(case_type:int, rechno:int, artno:int):

    global t_bill_line_list, bill_line

    db_session = local_storage.db_session


    def generate_output():
        db_session.save()
        return {"t-bill-line": t_bill_line_list}

    if case_type == 1:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.rechnr == rechno)).first()

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            t_bill_line = buffer_copy(bill_line, T_bill_line)
    elif case_type == 2:

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == rechno)).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            t_bill_line = buffer_copy(bill_line, T_bill_line)
    elif case_type == 3:

        bill_line_recid_list = []
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                (Bill_line.rechnr == rechno)).all():
            if bill_line._recid in bill_line_recid_list:
                continue
            else:
                bill_line_recid_list.append(bill_line._recid)

            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                t_bill_line = T_bill_line()
                t_bill_line_list.append(t_bill_line)

                t_bill_line = buffer_copy(bill_line, T_bill_line)
    elif case_type == 4:

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == rechno) & (func.lower(Bill_line.zinr) != "")).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            t_bill_line = buffer_copy(bill_line, T_bill_line)
    elif case_type == 5:

        bill_line_recid_list = []
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                (Bill_line.rechnr == rechno)).all():
            if bill_line._recid in bill_line_recid_list:
                continue
            else:
                bill_line_recid_list.append(bill_line._recid)

            if artikel.artart == 2 or artikel.artart == 5 or artikel.artart == 6 or artikel.artart == 7:
                t_bill_line = T_bill_line()
                t_bill_line_list.append(t_bill_line)

                t_bill_line = buffer_copy(bill_line, T_bill_line)
    elif case_type == 6:

        bill_line_recid_list = []
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                (Bill_line.rechnr == rechno)).all():
            if bill_line._recid in bill_line_recid_list:
                continue
            else:
                bill_line_recid_list.append(bill_line._recid)


            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            t_bill_line = buffer_copy(bill_line, T_bill_line)
    elif case_type == 7:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line._recid == rechno)).first()

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            t_bill_line = buffer_copy(bill_line, T_bill_line)

    return generate_output()