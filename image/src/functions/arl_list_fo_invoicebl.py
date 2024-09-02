from functions.additional_functions import *
import decimal
from models import Res_line, Bill

def arl_list_fo_invoicebl(recid_resline:int):
    inp_rechnr = 0
    res_line = bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal inp_rechnr, res_line, bill


        return {"inp_rechnr": inp_rechnr}


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == recid_resline)).first()

    bill = db_session.query(Bill).filter(
            (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.zinr == res_line.zinr)).first()

    if bill:
        inp_rechnr = bill.rechnr

    return generate_output()