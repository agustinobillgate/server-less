from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def selforder_getparamsbl(session_parameter:str):
    department_number = 0
    table_no = 0
    guest_name = ""
    pax = 0
    room = ""
    checkin_date = ""
    checkout_date = ""
    package = ""
    mess_result = ""
    session_expired = False
    selforder_setup_list = []
    queasy = None

    selforder_setup = None

    selforder_setup_list, Selforder_setup = create_model("Selforder_setup", {"nr":int, "setup_keyword":str, "setup_value":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal department_number, table_no, guest_name, pax, room, checkin_date, checkout_date, package, mess_result, session_expired, selforder_setup_list, queasy


        nonlocal selforder_setup
        nonlocal selforder_setup_list
        return {"department_number": department_number, "table_no": table_no, "guest_name": guest_name, "pax": pax, "room": room, "checkin_date": checkin_date, "checkout_date": checkout_date, "package": package, "mess_result": mess_result, "session_expired": session_expired, "selforder-setup": selforder_setup_list}

    if session_parameter == "" or session_parameter == None:
        session_parameter = "1_session_parameter cannot be empty!"

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 230) &  (func.lower(Queasy.char1) == (session_parameter).lower())).first()

    if queasy:
        department_number = queasy.number1
        table_no = queasy.number2
        guest_name = queasy.char2
        pax = queasy.number3
        checkin_date = entry(1, queasy.char3, "|")
        checkout_date = entry(2, queasy.char3, "|")
        package = entry(3, queasy.char3, "|")
        room = entry(0, queasy.char3, "|")
        session_expired = queasy.logi1


    else:
        session_parameter = "2_data not found, please check your session!"

        return generate_output()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1)).all():
        selforder_setup = Selforder_setup()
        selforder_setup_list.append(selforder_setup)

        selforder_setup.nr = queasy.number2


        selforder_setup.setup_keyword = queasy.char1

        if queasy.number3 == 1:
            selforder_setup.setup_value = to_string(queasy.char2)

        elif queasy.number3 == 2:
            selforder_setup.setup_value = to_string(queasy.deci1)

        elif queasy.number3 == 3:
            selforder_setup.setup_value = to_string(queasy.date1)

        elif queasy.number3 == 4:
            selforder_setup.setup_value = to_string(queasy.logi1)

        elif queasy.number3 == 5:
            selforder_setup.setup_value = to_string(queasy.char2)

        elif queasy.number3 == 6:
            selforder_setup.setup_value = to_string(queasy.char2)
    mess_result = "0_get param success"

    return generate_output()