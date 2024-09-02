from functions.additional_functions import *
import decimal
from datetime import date
from functions.sorder_list_btn_gobl import sorder_list_btn_gobl
import re

def sorder_list_btn_go2bl(user_init:str, sorttype:int, s_artnr:int, from_date:date, to_date:date, from_sup:str, to_sup:str, closepo:bool):
    po_list_list = []
    delidate:date = None

    str_list = po_list = None

    str_list_list, Str_list = create_model("Str_list", {"docu_nr":str, "s":str, "dunit":str, "content":int, "lief_nr":int, "warenwert":decimal})
    po_list_list, Po_list = create_model("Po_list", {"datum":date, "document_no":str, "artno":int, "artdesc":str, "orderqty":int, "unit_price":decimal, "amount1":decimal, "delivered":int, "s_unit":int, "amount2":decimal, "delivdate":date, "supplier":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal po_list_list, delidate


        nonlocal str_list, po_list
        nonlocal str_list_list, po_list_list
        return {"po-list": po_list_list}

    str_list_list = get_output(sorder_list_btn_gobl(user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo))
    po_list_list.clear()

    for str_list in query(str_list_list):

        if re.match(".*T O T A L.*",str_list.s):
            po_list = Po_list()
            po_list_list.append(po_list)

            artdesc = "T O T A L"
            amount1 = decimal.Decimal(trim(substring(str_list.s, 80, 15)))


        else:
            delidate = date_mdy(trim(substring(str_list.s, 122, 8)))
            po_list = Po_list()
            po_list_list.append(po_list)

            datum = date_mdy(trim(substring(str_list.s, 0, 8)))
            document_no = trim(substring(str_list.s, 8, 12))
            artno = to_int(trim(substring(str_list.s, 20, 7)))
            artdesc = trim(substring(str_list.s, 27, 30))
            orderqty = to_int(trim(substring(str_list.s, 57, 10)))
            unit_price = decimal.Decimal(trim(substring(str_list.s, 67, 13)))
            amount1 = decimal.Decimal(trim(substring(str_list.s, 80, 15)))
            delivered = to_int(trim(substring(str_list.s, 95, 11)))
            s_unit = to_int(trim(substring(str_list.s, 105, 4)))
            amount2 = decimal.Decimal(trim(substring(str_list.s, 108, 15)))
            delivdate = delidate
            supplier = trim(substring(str_list.s, 130, 16))

    return generate_output()