from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Bill_line, Billjournal, Res_line, Arrangement, Argt_line

def check_gledger_show_lodgingbl(currdate:date):
    lod_list_list = []
    bill = bill_line = billjournal = res_line = arrangement = argt_line = None

    lod_list = None

    lod_list_list, Lod_list = create_model("Lod_list", {"resnr":int, "reslinnr":int, "zinr":str, "rmrate":decimal, "lodge":decimal, "bfast":decimal, "tot":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lod_list_list, bill, bill_line, billjournal, res_line, arrangement, argt_line


        nonlocal lod_list
        nonlocal lod_list_list
        return {"lod-list": lod_list_list}

    def show_lodging():

        nonlocal lod_list_list, bill, bill_line, billjournal, res_line, arrangement, argt_line


        nonlocal lod_list
        nonlocal lod_list_list

        do_it:bool = False
        lod_list_list.clear()

        bill_line_obj_list = []
        for bill_line, bill in db_session.query(Bill_line, Bill).join(Bill,(Bill.rechnr == Bill_line.rechnr)).filter(
                (Bill_line.bill_datum == currdate) &  (Bill_line.artnr == 99) &  (Bill_line.departement == 0)).all():
            if bill_line._recid in bill_line_obj_list:
                continue
            else:
                bill_line_obj_list.append(bill_line._recid)


            lod_list = Lod_list()
            lod_list_list.append(lod_list)

            lod_list.zinr = bill_line.zinr
            lod_list.rmrate = bill_line.betrag
            lod_list.resnr = bill.resnr

        for lod_list in query(lod_list_list):

            billjournal = db_session.query(Billjournal).filter(
                    (Billjournal.departement == 0) &  (Billjournal.zinr == lod_list.zinr) &  (Billjournal.bill_datum == currdate) &  (Billjournal.artnr == 100)).first()

            if billjournal:
                lod_list.lodge = billjournal.betrag
                lod_list.tot = billjournal.betrag

            res_line = db_session.query(Res_line).filter(
                    (Res_line.zinr == lod_list.zinr) &  (Res_line.resnr == lod_list.resnr)).first()
            do_it = None != res_line

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()
            do_it = None != arrangement

            if do_it:

                for argt_line in db_session.query(Argt_line).filter(
                        (Argt_line.argtnr == arrangement.argtnr)).all():

                    billjournal = db_session.query(Billjournal).filter(
                            (Billjournal.departement != 0) &  (Billjournal.zinr == lod_list.zinr) &  (Billjournal.bill_datum == currdate) &  (Billjournal.artnr == argt_line.argt_artnr)).first()

                    if billjournal:
                        lod_list.bfast = lod_list.bfast + billjournal.betrag
                        lod_list.tot = lod_list.lodge + lod_list.bfast


    show_lodging()

    return generate_output()