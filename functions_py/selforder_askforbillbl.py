#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def selforder_askforbillbl(session_parameter:string, outlet_number:int):

    prepare_cache ([Queasy])

    mess_result = ""
    queasy = None

    db_session = local_storage.db_session
    session_parameter = session_parameter.strip()

    def generate_output():
        nonlocal mess_result, queasy
        nonlocal session_parameter, outlet_number

        return {"mess_result": mess_result}


    if session_parameter == "" or session_parameter == None:
        mess_result = "1-Session Param can't be null"

        return generate_output()

    if outlet_number == 0 or outlet_number == None:
        mess_result = "1-Outlet can't be null"

        return generate_output()

    # queasy = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"number1": [(eq, outlet_number)],"char3": [(eq, session_parameter)],"logi1": [(eq, True)]})
    queasy = db_session.query(Queasy).filter(
        (Queasy.key == 225) & (Queasy.char1 == "orderbill") &
        (Queasy.number1 == outlet_number) & (Queasy.char3 == session_parameter) &
        (Queasy.logi1 == True)).with_for_update().first()
    if queasy:
        pass
        queasy.logi2 = True
        mess_result = "0-Ask For Bill Success"
        pass
    else:
        mess_result = "1-No Record Found!Ask for Bill Failed"
    pass

    return generate_output()