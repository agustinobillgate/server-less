from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy

def selforder_proc_sessionbl(case_type:int, sessionid:str, outlet_no:int, table_nr:int, guest_name:str, pax:int, room:str, checkin_date:date, checkout_date:date, package:str, email_adr:str):
    ci_str:str = ""
    co_str:str = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_str, co_str, queasy


        return {}


    if checkin_date == None:
        ci_str = ""
    else:
        ci_str = to_string(checkin_date)

    if checkout_date == None:
        co_str = ""
    else:
        co_str = to_string(checkout_date)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 230
        queasy.number1 = outlet_no
        queasy.number2 = table_nr
        queasy.number3 = pax
        queasy.char1 = sessionid
        queasy.char2 = guest_name + "|" + email_adr
        queasy.char3 = room + "|" +\
                to_string(ci_str) + "|" +\
                to_string(co_str) + "|" +\
                package
        queasy.date1 = get_current_date()
        queasy.deci1 = get_current_time_in_seconds()
        queasy.logi1 = False

    return generate_output()