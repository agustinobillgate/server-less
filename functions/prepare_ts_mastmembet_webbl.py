#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Bill, Res_line

def prepare_ts_mastmembet_webbl(billno:int):

    prepare_cache ([Htparam, Bill, Res_line])

    resno = 0
    price_decimal = 0
    q1_list_data = []
    htparam = bill = res_line = None

    q1_list = b_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"zinr":string, "name":string, "resstatus":int, "ankunft":date, "abreise":date, "gastnr":int, "resnr":int, "reslinnr":int, "parent_nr":int})
    b_list_data, B_list = create_model("B_list", {"resnr":int, "reslinnr":int, "rechnr":int, "saldo":Decimal, "parent_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resno, price_decimal, q1_list_data, htparam, bill, res_line
        nonlocal billno


        nonlocal q1_list, b_list
        nonlocal q1_list_data, b_list_data

        return {"resno": resno, "price_decimal": price_decimal, "q1-list": q1_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    bill = get_cache (Bill, {"rechnr": [(eq, billno)]})
    resno = bill.resnr

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
        b_list = B_list()
        b_list_data.append(b_list)

        b_list.resnr = res_line.resnr
        b_list.reslinnr = res_line.reslinnr

        if bill:
            b_list.rechnr = bill.rechnr
            b_list.saldo =  to_decimal(bill.saldo)
            b_list.parent_nr = bill.parent_nr

    res_line_obj_list = {}
    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line.zinr, b_list.parent_nr, Res_line.name).all():
        b_list = query(b_list_data, (lambda b_list: b_list.resnr == res_line.resnr and b_list.reslinnr == res_line.reslinnr), first=True)
        if not b_list:
            continue

        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.zinr = res_line.zinr
        q1_list.name = res_line.name
        q1_list.resstatus = res_line.resstatus
        q1_list.ankunft = res_line.ankunft
        q1_list.abreise = res_line.abreise
        q1_list.gastnr = res_line.gastnr
        q1_list.resnr = res_line.resnr
        q1_list.reslinnr = res_line.reslinnr
        q1_list.parent_nr = b_list.parent_nr

    return generate_output()