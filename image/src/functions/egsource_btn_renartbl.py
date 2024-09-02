from functions.additional_functions import *
import decimal
from models import Eg_request

def egsource_btn_renartbl(source_number1:int):
    fl_code = 0
    eg_request = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_request


        return {"fl_code": fl_code}


    eg_request = db_session.query(Eg_request).filter(
            (eg_Request.SOURCE == source_number1)).first()

    if eg_Request:
        fl_code = 1

    return generate_output()