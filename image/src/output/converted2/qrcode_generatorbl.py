#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

code_list_list, Code_list = create_model("Code_list", {"code_num":int, "img_name":string, "code_str":string, "code_type":int})

def qrcode_generatorbl(case_type:int, code_list_list:[Code_list]):

    prepare_cache ([Queasy])

    q248_count = 1
    msg_result = ""
    found_bill:bool = False
    bill_no:int = 0
    count_j:int = 0
    str_code:string = ""
    queasy = None

    code_list = queasy248 = qns_cashless = None

    Queasy248 = create_buffer("Queasy248",Queasy)
    Qns_cashless = create_buffer("Qns_cashless",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q248_count, msg_result, found_bill, bill_no, count_j, str_code, queasy
        nonlocal case_type
        nonlocal queasy248, qns_cashless


        nonlocal code_list, queasy248, qns_cashless

        return {"q248_count": q248_count, "msg_result": msg_result}

    if case_type == 1:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 248)).order_by(Queasy.number1.desc()).yield_per(100):
            q248_count = queasy.number1 + 1
            break
    else:
        count_j = 0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 248)).order_by(Queasy.number1.desc()).yield_per(100):
            count_j = queasy.number1
            break

        for code_list in query(code_list_list, sort_by=[("code_num",False)]):
            count_j = count_j + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 248
            queasy.number1 = count_j
            queasy.number2 = code_list.code_type
            queasy.char1 = code_list.img_name
            queasy.char2 = code_list.code_str

    return generate_output()