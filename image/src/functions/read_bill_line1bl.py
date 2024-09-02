from functions.additional_functions import *
import decimal
from models import Bill_line, Res_line, Bill, Artikel

def read_bill_line1bl(case_type:int, pvilanguage:int, rechno:int, artno:int, deptno:int, anzahl:int, epreis:decimal, betrag:decimal):
    t_bill_line_list = []
    lvcarea:str = "fo_invoice"
    bill_line = res_line = bill = artikel = None

    t_bill_line = rlbuff = bibuff = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})

    Rlbuff = Res_line
    Bibuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_list, lvcarea, bill_line, res_line, bill, artikel
        nonlocal rlbuff, bibuff


        nonlocal t_bill_line, rlbuff, bibuff
        nonlocal t_bill_line_list
        return {"t-bill-line": t_bill_line_list}

    if case_type == 1:

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.artnr == artno) &  (Bill_line.departement == deptno) &  (Bill_line.rechnr == rechno)).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 2:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.artnr == artno) &  (Bill_line.departement == deptno) &  (Bill_line.rechnr == rechno) &  (Bill_line.anzahl == - anzahl) &  (Bill_line.epreis == epreis) &  (Bill_line.betrag == - betrag)).first()

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 3:

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == rechno)).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 4:

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == rechno) &  (Bill_line.artnr == artno)).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid
    elif case_type == 5:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line._recid == anzahl) &  (Bill_line.rechnr == rechno)).first()

        if bill_line:
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid

    if not t_bill_line:

        return generate_output()

    bill = db_session.query(Bill).filter(
            (Bill.rechnr == rechno)).first()

    for t_bill_line in query(t_bill_line_list):

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == t_bill_line.artnr) &  (Artikel.departement == t_bill_line.departement)).first()

        if artikel:
            t_bill_line.artart = artikel.artart

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line._recid == t_Bill_line.bl_recid)).first()

        if bill_line.massnr != 0 and bill_line.billin_nr != 0 and (bill_line.massnr != bill.resnr or bill_line.billin_nr != bill.reslinnr):

            bibuff = db_session.query(Bibuff).filter(
                    (Bibuff.resnr == bill_line.massnr) &  (Bibuff.reslinnr == bill_line.billin_nr)).first()

            if bibuff:

                rlbuff = db_session.query(Rlbuff).filter(
                        (Rlbuff.resnr == bibuff.resnr) &  (Rlbuff.reslinnr == bibuff.parent_nr)).first()

                if rlbuff:
                    t_bill_line.tool_tip = \
                        translateExtended ("RmNo", lvcarea, "") + " " +\
                        rlbuff.zinr + " " + rlbuff.name + "  " + to_string(rlbuff.ankunft) +\
                        "-" + to_string(rlbuff.abreise) + " " +\
                        translateExtended ("BillNo", lvcarea, "") + " " +\
                        to_string(bibuff.rechnr)


                else:
                    t_bill_line.tool_tip = translateExtended ("RmNo", lvcarea, "") + " " + bibuff.zinr + " " + bibuff.name + " " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(bibuff.rechnr)
            else:
                t_bill_line.tool_tip = ""

    return generate_output()