from functions.additional_functions import *
import decimal
from functions.read_billbl import read_billbl
from functions.write_bill2bl import write_bill2bl
from models import Bill

def mast_article_openbl(resnr:int, gastnrpay:int, bill_receiver:str):
    success = False
    bill = None

    bill1 = None

    bill1_list, Bill1 = create_model_like(Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success, bill


        nonlocal bill1
        nonlocal bill1_list
        return {"success": success}


    bill1_list = get_output(read_billbl(2, None, resnr, 0, None))

    bill1 = query(bill1_list, first=True)

    if bill1 and bill1.gastnr != gastnrpay:
        bill1.gastnr = gastnrpay
        bill1.name = bill_receiver


        success = get_output(write_bill2bl(bill1))

    return generate_output()