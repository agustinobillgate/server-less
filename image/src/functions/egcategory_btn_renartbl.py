from functions.additional_functions import *
import decimal
from models import Eg_request

def egcategory_btn_renartbl(category_number1:int):
    fl_code = False
    eg_request = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_request


        return {"fl_code": fl_code}


    eg_request = db_session.query(Eg_request).filter(
            (eg_Request.category == category_number1)).first()

    if eg_Request:
        fl_code = True

    return generate_output()