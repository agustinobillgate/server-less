#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bill

def read_oth_billbl(resnr:int):

    prepare_cache ([Bill])

    split_bill = False
    bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal split_bill, bill
        nonlocal resnr

        return {"split_bill": split_bill}


    for bill in db_session.query(Bill).filter(
             (Bill.resnr == resnr)).order_by(Bill._recid).all():

        if bill.reslinnr > 1:
            split_bill = True
        else:
            split_bill = False

    return generate_output()