from functions.additional_functions import *
import decimal
from models import Billhis, Bill

def view_history2bl(resnr:int, reslinnr:int):
    bill_list_list = []
    billhis = bill = None

    bill_list = None

    bill_list_list, Bill_list = create_model_like(Billhis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_list_list, billhis, bill


        nonlocal bill_list
        nonlocal bill_list_list
        return {"bill-list": bill_list_list}

    for bill in db_session.query(Bill).filter(
            (Bill.resnr == resnr) &  (Bill.parent_nr == reslinnr)).all():
        bill_list = Bill_list()
        bill_list_list.append(bill_list)

        buffer_copy(bill, bill_list)

    if not bill_list:

        for billhis in db_session.query(Billhis).filter(
                (Billhis.resnr == resnr) &  (Billhis.parent_nr == reslinnr)).all():
            bill_list = Bill_list()
            bill_list_list.append(bill_list)

            buffer_copy(billhis, bill_list)

    return generate_output()