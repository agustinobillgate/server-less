#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def selforder_askforbillbl(session_parameter:string, outlet_number:int):

    prepare_cache ([Queasy])

    mess_result = ""
    queasy = None

    db_session = local_storage.db_session

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

    queasy = get_cache (Queasy, {"key": [(eq, 225)],"char1": [(eq, "orderbill")],"number1": [(eq, outlet_number)],"char3": [(eq, session_parameter)],"logi1": [(eq, True)]})

    if queasy:
        pass
        queasy.logi2 = True


        mess_result = "0-Ask For Bill Success"
        pass
    else:
        mess_result = "1-No Record Found!Ask for Bill Failed"
    pass

    return generate_output()