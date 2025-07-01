#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Bill_line, Billjournal, Res_line, Arrangement, Argt_line

def check_gledger_show_lodgingbl(currdate:date):

    prepare_cache ([Bill, Bill_line, Billjournal, Argt_line])

    lod_list_list = []
    bill = bill_line = billjournal = res_line = arrangement = argt_line = None

    lod_list = None

    lod_list_list, Lod_list = create_model("Lod_list", {"resnr":int, "reslinnr":int, "zinr":string, "rmrate":Decimal, "lodge":Decimal, "bfast":Decimal, "tot":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lod_list_list, bill, bill_line, billjournal, res_line, arrangement, argt_line
        nonlocal currdate


        nonlocal lod_list
        nonlocal lod_list_list

        return {"lod-list": lod_list_list}

    def show_lodging():

        nonlocal lod_list_list, bill, bill_line, billjournal, res_line, arrangement, argt_line
        nonlocal currdate


        nonlocal lod_list
        nonlocal lod_list_list

        do_it:bool = False
        lod_list_list.clear()

        bill_line_obj_list = {}
        bill_line = Bill_line()
        bill = Bill()
        for bill_line.zinr, bill_line.betrag, bill_line._recid, bill.resnr, bill._recid in db_session.query(Bill_line.zinr, Bill_line.betrag, Bill_line._recid, Bill.resnr, Bill._recid).join(Bill,(Bill.rechnr == Bill_line.rechnr)).filter(
                 (Bill_line.bill_datum == currdate) & (Bill_line.artnr == 99) & (Bill_line.departement == 0)).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True


            lod_list = Lod_list()
            lod_list_list.append(lod_list)

            lod_list.zinr = bill_line.zinr
            lod_list.rmrate =  to_decimal(bill_line.betrag)
            lod_list.resnr = bill.resnr

        for lod_list in query(lod_list_list):

            billjournal = get_cache (Billjournal, {"departement": [(eq, 0)],"zinr": [(eq, lod_list.zinr)],"bill_datum": [(eq, currdate)],"artnr": [(eq, 100)]})

            if billjournal:
                lod_list.lodge =  to_decimal(billjournal.betrag)
                lod_list.tot =  to_decimal(billjournal.betrag)

            res_line = get_cache (Res_line, {"zinr": [(eq, lod_list.zinr)],"resnr": [(eq, lod_list.resnr)]})
            do_it = None != res_line

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
            do_it = None != arrangement

            if do_it:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

                    billjournal = get_cache (Billjournal, {"departement": [(ne, 0)],"zinr": [(eq, lod_list.zinr)],"bill_datum": [(eq, currdate)],"artnr": [(eq, argt_line.argt_artnr)]})

                    if billjournal:
                        lod_list.bfast =  to_decimal(lod_list.bfast) + to_decimal(billjournal.betrag)
                        lod_list.tot =  to_decimal(lod_list.lodge) + to_decimal(lod_list.bfast)

    show_lodging()

    return generate_output()