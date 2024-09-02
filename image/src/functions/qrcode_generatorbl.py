from functions.additional_functions import *
import decimal
from models import Queasy

def qrcode_generatorbl(case_type:int, code_list:[Code_list]):
    q248_count = 0
    msg_result = ""
    found_bill:bool = False
    bill_no:int = 0
    count_j:int = 0
    str_code:str = ""
    queasy = None

    code_list = queasy248 = qns_cashless = None

    code_list_list, Code_list = create_model("Code_list", {"code_num":int, "img_name":str, "code_str":str, "code_type":int})

    Queasy248 = Queasy
    Qns_cashless = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q248_count, msg_result, found_bill, bill_no, count_j, str_code, queasy
        nonlocal queasy248, qns_cashless


        nonlocal code_list, queasy248, qns_cashless
        nonlocal code_list_list
        return {"q248_count": q248_count, "msg_result": msg_result}

    if case_type == 1:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 248)).all():
            q248_count = queasy.number1 + 1
            break
    else:
        count_j = 0

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 248)).all():
            count_j = queasy.number1
            break

        for code_list in query(code_list_list):
            count_j = count_j + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 248
            queasy.number1 = count_j
            queasy.number2 = code_list.code_type
            queasy.char1 = code_list.img_name
            queasy.char2 = code_list.code_str

    return generate_output()