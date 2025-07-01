#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_bill1bl import read_bill1bl
from functions.read_billhisbl import read_billhisbl
from models import Bill, Billhis

def fo_invoice_inquirybillbl(inq_bill:int):
    pvilanguage:int = 1
    lvcarea:string = ""
    msg_str = ""
    str:string = ""
    done:bool = False
    bill_exist:bool = False
    bill = billhis = None

    t_bill = t_billhis = None

    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_billhis_list, T_billhis = create_model_like(Billhis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pvilanguage, lvcarea, msg_str, str, done, bill_exist, bill, billhis
        nonlocal inq_bill


        nonlocal t_bill, t_billhis
        nonlocal t_bill_list, t_billhis_list

        return {"msg_str": msg_str}

    t_bill_list = get_output(read_bill1bl(1, inq_bill, None, None, None, None, None, None, None, None))

    t_bill = query(t_bill_list, first=True)

    if not t_bill and inq_bill != 0:
        bill_exist, t_billhis_list = get_output(read_billhisbl(1, inq_bill, None, None))

        t_billhis = query(t_billhis_list, first=True)

        if t_billhis:

            if t_billhis.resnr > 0 and t_billhis.reslinnr == 0:
                str = translateExtended ("1Master Bill History found.", lvcarea, "")

            elif t_billhis.resnr > 0 and t_billhis.reslinnr > 0:
                str = translateExtended ("1Hotel Guest Bill History found.", lvcarea, "")
            else:
                str = translateExtended ("1Non Stay Guest Bill History found.", lvcarea, "")
            msg_str = str

            return generate_output()
        else:
            msg_str = translateExtended ("No such bill number.", lvcarea, "")

    elif t_bill and t_bill.flag == 0:

        if t_bill.resnr == 0:
            msg_str = translateExtended ("Non-stay Guest Bill - Status: active.", lvcarea, "")

            return generate_output()

        elif t_bill.resnr > 0 and t_bill.reslinnr == 0:
            msg_str = translateExtended ("Master Bill - Status: active.", lvcarea, "")

            return generate_output()

        elif t_bill.resnr > 0 and t_bill.reslinnr > 0:
            msg_str = translateExtended ("Hotel Guest Bill - Status: active.", lvcarea, "")

            return generate_output()

    elif t_bill and t_bill.flag == 1:

        if t_bill.resnr == 0:
            msg_str = translateExtended ("Non-stay Guest Bill - Status: closed.", lvcarea, "")

            return generate_output()

        elif t_bill.resnr > 0 and t_bill.reslinnr == 0:
            msg_str = translateExtended ("Master Bill - Status: closed.", lvcarea, "")

            return generate_output()

        elif t_bill.resnr > 0 and t_bill.reslinnr > 0:
            msg_str = translateExtended ("Hotel Guest Bill - Status: closed.", lvcarea, "")

            return generate_output()

    return generate_output()