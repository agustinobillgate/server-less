#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill_line, Artikel

def read_bill_linebl(case_type:int, rechno:int, artno:int):

    prepare_cache ([Artikel])

    t_bill_line_list = []
    bill_line = artikel = None

    t_bill_line = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_list, bill_line, artikel
        nonlocal case_type, rechno, artno


        nonlocal t_bill_line
        nonlocal t_bill_line_list

        return {"t-bill-line": t_bill_line_list}

    if case_type == 1:

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, rechno)]})

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
    elif case_type == 2:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == rechno)).order_by(Bill_line._recid).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
    elif case_type == 3:

        bill_line_obj_list = {}
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                 (Bill_line.rechnr == rechno)).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True

            if artikel.artart == 0 or artikel.artart == 1 or artikel.artart == 8 or artikel.artart == 9:
                t_bill_line = T_bill_line()
                t_bill_line_list.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
    elif case_type == 4:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == rechno) & (Bill_line.zinr != "")).order_by(Bill_line._recid).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
    elif case_type == 5:

        bill_line_obj_list = {}
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr)).filter(
                 (Bill_line.rechnr == rechno)).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True

            if artikel.artart == 2 or artikel.artart == 5 or artikel.artart == 6 or artikel.artart == 7:
                t_bill_line = T_bill_line()
                t_bill_line_list.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
    elif case_type == 6:

        bill_line_obj_list = {}
        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).filter(
                 (Bill_line.rechnr == rechno)).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True


            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
    elif case_type == 7:

        bill_line = get_cache (Bill_line, {"_recid": [(eq, rechno)]})

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)

    return generate_output()