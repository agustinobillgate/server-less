#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill_line, Bill

def fo_invoice_disp_bill_linebl(bil_recid:int, double_currency:bool):

    prepare_cache ([Bill])

    t_bill_line_data = []
    t_spbill_list_data = []
    bill_line = bill = None

    t_spbill_list = t_bill_line = None

    t_spbill_list_data, T_spbill_list = create_model("T_spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bill_line_data, t_spbill_list_data, bill_line, bill
        nonlocal bil_recid, double_currency


        nonlocal t_spbill_list, t_bill_line
        nonlocal t_spbill_list_data, t_bill_line_data

        return {"t-bill-line": t_bill_line_data, "t-spbill-list": t_spbill_list_data}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if bill:

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():

            t_spbill_list = query(t_spbill_list_data, filters=(lambda t_spbill_list: t_spbill_list.bl_recid == to_int(bill_line._recid)), first=True)

            if not t_spbill_list:
                t_spbill_list = T_spbill_list()
                t_spbill_list_data.append(t_spbill_list)

                t_spbill_list.selected = False
                t_spbill_list.bl_recid = bill_line._recid

        if double_currency:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
                t_bill_line.rec_id = bill_line._recid

        else:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line._recid).all():
                t_bill_line = T_bill_line()
                t_bill_line_data.append(t_bill_line)

                buffer_copy(bill_line, t_bill_line)
                t_bill_line.rec_id = bill_line._recid


    return generate_output()