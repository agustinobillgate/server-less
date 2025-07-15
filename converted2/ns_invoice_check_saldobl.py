#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill_line, Bill, Res_line, Artikel

def ns_invoice_check_saldobl(pvilanguage:int, t_rechnr:int):

    prepare_cache ([Bill, Artikel])

    t_bill_data = []
    t_bill_line_data = []
    lvcarea:string = "ns-invoice"
    bill_line = bill = res_line = artikel = None

    t_bill_line = t_bill = bibuff = rlbuff = None

    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    t_bill_data, T_bill = create_model_like(Bill, {"bl_recid":int})

    Bibuff = create_buffer("Bibuff",Bill)
    Rlbuff = create_buffer("Rlbuff",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_data, t_bill_line_data, lvcarea, bill_line, bill, res_line, artikel
        nonlocal pvilanguage, t_rechnr
        nonlocal bibuff, rlbuff


        nonlocal t_bill_line, t_bill, bibuff, rlbuff
        nonlocal t_bill_line_data, t_bill_data

        return {"t-bill": t_bill_data, "t-bill-line": t_bill_line_data}


    bill = get_cache (Bill, {"rechnr": [(eq, t_rechnr)]})

    if bill:
        t_bill = T_bill()
        t_bill_data.append(t_bill)

        buffer_copy(bill, t_bill)
        t_bill.bl_recid = bill._recid

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == t_rechnr)).order_by(Bill_line._recid).all():
            t_bill_line = T_bill_line()
            t_bill_line_data.append(t_bill_line)

            buffer_copy(bill_line, t_bill_line)
            t_bill_line.bl_recid = bill_line._recid

            artikel = get_cache (Artikel, {"artnr": [(eq, t_bill_line.artnr)],"departement": [(eq, t_bill_line.departement)]})

            if artikel:
                t_bill_line.artart = artikel.artart

            if bill_line.massnr != 0 and bill_line.billin_nr != 0 and (bill_line.massnr != bill.resnr or bill_line.billin_nr != bill.reslinnr):

                bibuff = get_cache (Bill, {"resnr": [(eq, bill_line.massnr)],"reslinnr": [(eq, bill_line.billin_nr)]})

                if bibuff:

                    rlbuff = db_session.query(Rlbuff).filter(
                             (Rlbuff.resnr == bibuff.resnr) & (Rlbuff.reslinnr == bibuff.parent_nr)).first()

                    if rlbuff:
                        t_bill_line.tool_tip = \
                            translateExtended ("RmNo", lvcarea, "") + " " +\
                            rlbuff.zinr + " " + rlbuff.name + " " + to_string(rlbuff.ankunft) +\
                            "-" + to_string(rlbuff.abreise) + " " +\
                            translateExtended ("BillNo", lvcarea, "") + " " +\
                            to_string(bibuff.rechnr)


                    else:
                        t_bill_line.tool_tip = translateExtended ("RmNo", lvcarea, "") + " " + bibuff.zinr + " " + bibuff.name + " " + translateExtended ("BillNo", lvcarea, "") + " " + to_string(bibuff.rechnr)
                else:
                    t_bill_line.tool_tip = ""

    return generate_output()