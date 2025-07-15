#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_jouhdr, Gl_jhdrhis

payload_list_data, Payload_list = create_model("Payload_list", {"refno":string})

def manual_ar_add_validation_webbl(payload_list_data:[Payload_list]):
    response_list_data = []
    refno:string = ""
    gl_jouhdr = gl_jhdrhis = None

    payload_list = response_list = None

    response_list_data, Response_list = create_model("Response_list", {"success_flag":bool, "err_msg":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_data, refno, gl_jouhdr, gl_jhdrhis


        nonlocal payload_list, response_list
        nonlocal response_list_data

        return {"response-list": response_list_data}

    response_list = Response_list()
    response_list_data.append(response_list)

    response_list.success_flag = True

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        refno = payload_list.refno

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, refno)]})

        if gl_jouhdr:
            response_list.success_flag = False
            response_list.err_msg = "Reference Number already used"

            return generate_output()

        gl_jhdrhis = get_cache (Gl_jhdrhis, {"refno": [(eq, refno)]})

        if gl_jhdrhis:
            response_list.success_flag = False
            response_list.err_msg = "Reference Number already used"

            return generate_output()
    else:
        response_list.success_flag = False

    return generate_output()