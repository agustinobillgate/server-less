#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ns_inv_cashless_toolsbl(cashless_code:string, type_code:int):

    prepare_cache ([Queasy])

    ok_flag = False
    code_list_list = []
    count_j:int = 0
    queasy = None

    code_list = queasy248 = None

    code_list_list, Code_list = create_model("Code_list", {"code_num":int, "img_name":string, "code_str":string, "code_type":int, "type_name":string})

    Queasy248 = create_buffer("Queasy248",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, code_list_list, count_j, queasy
        nonlocal cashless_code, type_code
        nonlocal queasy248


        nonlocal code_list, queasy248
        nonlocal code_list_list

        return {"ok_flag": ok_flag, "code-list": code_list_list}


    count_j = 0

    for queasy248 in db_session.query(Queasy248).filter(
             (Queasy248.key == 248)).order_by(Queasy248.number1.desc()).yield_per(100):
        count_j = queasy248.number1 + 1
        break

    queasy = get_cache (Queasy, {"key": [(eq, 248)],"char2": [(eq, cashless_code)]})

    if queasy:
        ok_flag = False
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 248
        queasy.number1 = count_j
        queasy.number2 = type_code
        queasy.char1 = "C:\\e1-vhp\\Zint\\BarcodeData\\NSCashless" + to_string(count_j, "999") + ".png"


        queasy.char2 = trim(cashless_code)
        pass
        ok_flag = True

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 248)).order_by(Queasy.number1.desc()).all():
        code_list = Code_list()
        code_list_list.append(code_list)

        code_list.code_num = queasy.number1
        code_list.img_name = queasy.char1
        code_list.code_str = queasy.char2
        code_list.code_type = queasy.number2

        if queasy.number2 == 1:
            code_list.type_name = "Barcode"
        else:
            code_list.type_name = "QR Code"

    return generate_output()