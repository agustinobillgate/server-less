from functions.additional_functions import *
import decimal
from models import Bill

def read_oth_billbl(resnr:int):
    split_bill = False
    bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal split_bill, bill


        return {"split_bill": split_bill}


    for bill in db_session.query(Bill).filter(
            (Bill.resnr == resnr)).all():

        if bill.reslinnr > 1:
            split_bill = True
        else:
            split_bill = False

    return generate_output()