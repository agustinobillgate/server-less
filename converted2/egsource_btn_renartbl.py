#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_request

def egsource_btn_renartbl(source_number1:int):
    fl_code = 0
    eg_request = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_request
        nonlocal source_number1

        return {"fl_code": fl_code}


    eg_request = get_cache (Eg_request, {"source": [(eq, source_number1)]})

    if eg_Request:
        fl_code = 1

    return generate_output()