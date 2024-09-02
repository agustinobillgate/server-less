from functions.additional_functions import *
import decimal
from models import Bill_line, Bill, Res_line, Artikel

def ns_invoice_check_saldobl(pvilanguage:int, t_rechnr:int):
    t_bill_list = []
    t_bill_line_list = []
    lvcarea:str = "ns_invoice"
    bill_line = bill = res_line = artikel = None

    t_bill_line = t_bill = bibuff = rlbuff = None

    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})

    Bibuff = Bill
    Rlbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_list, t_bill_line_list, lvcarea, bill_line, bill, res_line, artikel
        nonlocal bibuff, rlbuff


        nonlocal t_bill_line, t_bill, bibuff, rlbuff
        nonlocal t_bill_line_list, t_bill_list
        return {"t-bill": t_bill_list, "t-bill-line": t_bill_line_list}


    bill = db_session.query(Bill).filter(
            (Bill.rechnr == t_rechnr)).first()

    if bill:
        t_bill = T_bill()
        t_bill_list.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = bill._recid

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == t_rechnr)).all():
            t_bill_line = T_bill_line()
            t_bill_line_list.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == t_bill_line.artnr) &  (Artikel.departement == t_bill_line.departement)).first()

            if artikel:
                t_bill_line.artart = artikel.artart

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