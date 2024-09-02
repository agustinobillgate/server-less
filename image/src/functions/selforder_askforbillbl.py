from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def selforder_askforbillbl(session_parameter:str, outlet_number:int):
    mess_result = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, queasy


        return {"mess_result": mess_result}


    if session_parameter == "" or session_parameter == None:
        mess_result = "1_Session Param can't be null"

        return generate_output()

    if outlet_number == 0 or outlet_number == None:
        mess_result = "1_Outlet can't be null"

        return generate_output()

    queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.number1 == outlet_number) &  (func.lower(Queasy.char3) == (session_parameter).lower()) &  (Queasy.logi1)).first()

    if queasy:
        queasy.logi2 = True


        mess_result = "0_Ask For Bill Success"
    else:
        mess_result = "1_No Record Found!Ask for Bill Failed"

    queasy = db_session.query(Queasy).first()

    return generate_output()