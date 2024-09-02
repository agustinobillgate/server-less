from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def ns_inv_cashless_toolsbl(cashless_code:str, type_code:int):
    ok_flag = False
    code_list_list = []
    count_j:int = 0
    queasy = None

    code_list = queasy248 = None

    code_list_list, Code_list = create_model("Code_list", {"code_num":int, "img_name":str, "code_str":str, "code_type":int, "type_name":str})

    Queasy248 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, code_list_list, count_j, queasy
        nonlocal queasy248


        nonlocal code_list, queasy248
        nonlocal code_list_list
        return {"ok_flag": ok_flag, "code-list": code_list_list}


    count_j = 0

    for queasy248 in db_session.query(Queasy248).filter(
            (Queasy248.key == 248)).all():
        count_j = queasy248.number1 + 1
        break

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 248) &  (func.lower(Queasy.char2) == (cashless_code).lower())).first()

    if queasy:
        ok_flag = False
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 248
        queasy.number1 = count_j
        queasy.number2 = type_code
        queasy.char1 = "C:\\e1_vhp\\Zint\\BarcodeData\\NSCashless" + to_string(count_j, "999") + ".png"


        queasy.char2 = trim(cashless_code)

        queasy = db_session.query(Queasy).first()
        ok_flag = True

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 248)).all():
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