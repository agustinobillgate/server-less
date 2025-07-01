#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_request

def egcategory_btn_renartbl(category_number1:int):
    fl_code = False
    eg_request = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_request
        nonlocal category_number1

        return {"fl_code": fl_code}


    eg_request = get_cache (Eg_request, {"category": [(eq, category_number1)]})

    if eg_Request:
        fl_code = True

    return generate_output()