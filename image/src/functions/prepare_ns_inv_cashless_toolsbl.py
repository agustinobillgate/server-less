from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam, Queasy

def prepare_ns_inv_cashless_toolsbl():
    license_cashless = False
    code_list_list = []
    htparam = queasy = None

    code_list = None

    code_list_list, Code_list = create_model("Code_list", {"code_num":int, "img_name":str, "code_str":str, "code_type":int, "type_name":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal license_cashless, code_list_list, htparam, queasy


        nonlocal code_list
        nonlocal code_list_list
        return {"license_cashless": license_cashless, "code-list": code_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1022) &  (func.lower(Htparam.bezeich) != "not used") &  (Htparam.flogical)).first()

    if htparam:
        license_cashless = True

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