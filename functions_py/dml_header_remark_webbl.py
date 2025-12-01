#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 01-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

payload_list_data, Payload_list = create_model("Payload_list", {"dml_no":string, "dept_no":int, "datum":string, "remark":string})

def dml_header_remark_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Queasy])

    response_list_data = []
    dml_no:string = ""
    dept_no:int = 0
    datum:string = ""
    datum_date:date = None
    remark:string = ""
    queasy = None

    payload_list = response_list = None

    response_list_data, Response_list = create_model("Response_list", {"success_flag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_data, dml_no, dept_no, datum, datum_date, remark, queasy


        nonlocal payload_list, response_list
        nonlocal response_list_data

        return {"response-list": response_list_data}

    response_list = Response_list()
    response_list_data.append(response_list)

    response_list.success_flag = False

    payload_list = query(payload_list_data, first=True)

    if payload_list:
        dml_no = payload_list.dml_no
        dept_no = payload_list.dept_no
        datum = payload_list.datum
        remark = payload_list.remark


        datum_date = date_mdy(to_int(substring(datum, 0, 2)) , to_int(substring(datum, 3, 2)) , to_int(substring(datum, 6, 2)))

        if dml_no == "":
            dml_no = "D" + to_string(dept_no, "99") + substring(datum, 6, 2) + substring(datum, 0, 2) + substring(datum, 3, 2) + to_string(1, "999")

        # queasy = get_cache (Queasy, {"key": [(eq, 342)],"char1": [(eq, dml_no)],"number1": [(eq, dept_no)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 342) & (Queasy.char1 == dml_no) & (Queasy.number1 == dept_no)).with_for_update().first()

        if queasy:
            # pass
            queasy.char1 = dml_no
            queasy.number1 = dept_no
            queasy.date1 = datum_date
            queasy.char2 = remark
            # pass
            # pass
            db_session.refresh(queasy, with_for_update=True)
            response_list.success_flag = True
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 342
            queasy.char1 = dml_no
            queasy.number1 = dept_no
            queasy.date1 = datum_date
            queasy.char2 = remark


            response_list.success_flag = True

    return generate_output()