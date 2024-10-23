from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def additional_custom_programbl(prog_name:str, prog_title:str, prog_description:str, prog_type:int, prog_flag:bool, case_type:int, prog_number:int, prog_hotel_code:str, prog_password:str):
    mess_result = ""
    program_list_list = []
    record_number:int = 0
    queasy = None

    program_list = None

    program_list_list, Program_list = create_model("Program_list", {"prog_number":int, "prog_hotel_code":str, "prog_name":str, "prog_title":str, "prog_description":str, "prog_type":int, "prog_flag":bool, "prog_password":str, "prog_hashpassword":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, program_list_list, record_number, queasy
        nonlocal prog_name, prog_title, prog_description, prog_type, prog_flag, case_type, prog_number, prog_hotel_code, prog_password


        nonlocal program_list
        nonlocal program_list_list
        return {"mess_result": mess_result, "program-list": program_list_list}

    def load_data():

        nonlocal mess_result, program_list_list, record_number, queasy
        nonlocal prog_name, prog_title, prog_description, prog_type, prog_flag, case_type, prog_number, prog_hotel_code, prog_password


        nonlocal program_list
        nonlocal program_list_list

        rrawdatasha:bytes = None
        chmacsha:str = ""
        strdate:str = ""
        strpass:str = ""
        strhtlcode:str = ""
        strdate = to_string(get_year(get_current_date()) , "9999") + to_string(get_month(get_current_date()) , "99") + to_string(get_day(get_current_date()) , "99")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 268) & (func.lower(Queasy.char1) == (prog_hotel_code).lower())).order_by(Queasy._recid).all():

            if num_entries(queasy.char3, "|") >= 3:
                strhtlcode = queasy.char1
                strpass = entry(2, queasy.char3, "|")
                rrawdatasha = MESSAGE_DIGEST ('sha-256', strdate + strpass + strhtlcode, "")
                chmacsha = rrawdatasha.hexdigest()
            else:
                strpass = ""
                chmacsha = ""
            program_list = Program_list()
            program_list_list.append(program_list)

            program_list.prog_number = queasy.number1
            program_list.prog_hotel_code = queasy.char1
            program_list.prog_name = queasy.char2
            program_list.prog_title = entry(0, queasy.char3, "|")
            program_list.prog_description = entry(1, queasy.char3, "|")
            program_list.prog_type = queasy.number2
            program_list.prog_flag = queasy.logi1
            program_list.prog_password = strpass
            program_list.prog_hashpassword = chmacsha


    def load_data_list():

        nonlocal mess_result, program_list_list, record_number, queasy
        nonlocal prog_name, prog_title, prog_description, prog_type, prog_flag, case_type, prog_number, prog_hotel_code, prog_password


        nonlocal program_list
        nonlocal program_list_list

        rrawdatasha:bytes = None
        chmacsha:str = ""
        strdate:str = ""
        strpass:str = ""
        strhtlcode:str = ""
        strdate = to_string(get_year(get_current_date()) , "9999") + to_string(get_month(get_current_date()) , "99") + to_string(get_day(get_current_date()) , "99")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 268) & (func.lower(Queasy.char1) == (prog_hotel_code).lower())).order_by(Queasy._recid).all():

            if num_entries(queasy.char3, "|") >= 3:
                strhtlcode = queasy.char1
                strpass = entry(2, queasy.char3, "|")
                rrawdatasha = MESSAGE_DIGEST ('sha-256', strdate + strpass + strhtlcode, "")
                chmacsha = rrawdatasha.hexdigest()
            else:
                strpass = ""
                chmacsha = ""
            program_list = Program_list()
            program_list_list.append(program_list)

            program_list.prog_number = queasy.number1
            program_list.prog_hotel_code = queasy.char1
            program_list.prog_name = queasy.char2
            program_list.prog_title = entry(0, queasy.char3, "|")
            program_list.prog_description = entry(1, queasy.char3, "|")
            program_list.prog_type = queasy.number2
            program_list.prog_flag = queasy.logi1
            program_list.prog_password = ""
            program_list.prog_hashpassword = chmacsha


    if case_type == 1:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 268) & (func.lower(Queasy.char1) == (prog_hotel_code).lower()) & (func.lower(Queasy.char2) == (prog_name).lower())).first()

        if queasy:
            mess_result = "Program Already Exist"
        else:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 268) & (func.lower(Queasy.char1) == (prog_hotel_code).lower())).order_by(Queasy.number1.desc()).all():
                record_number = queasy.number1
                break

            if record_number == 0:
                record_number = 1
            else:
                record_number = record_number + 1
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 268
            queasy.char1 = prog_hotel_code
            queasy.char2 = prog_name
            queasy.char3 = prog_title + "|" + prog_description + "|" + prog_password
            queasy.number1 = record_number
            queasy.number2 = prog_type
            queasy.logi1 = prog_flag


            mess_result = "Add Program Success"
        load_data()

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 268) & (func.lower(Queasy.char1) == (prog_hotel_code).lower()) & (Queasy.number1 == prog_number)).first()

        if not queasy:
            mess_result = "Program Not Available"
        else:
            queasy.char1 = prog_hotel_code
            queasy.char2 = prog_name
            queasy.char3 = prog_title + "|" + prog_description + "|" + prog_password
            queasy.number2 = prog_type
            queasy.logi1 = prog_flag


            mess_result = "Modify Program Success"
        load_data()

    elif case_type == 3:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 268) & (func.lower(Queasy.char1) == (prog_hotel_code).lower()) & (Queasy.number1 == prog_number)).first()

        if not queasy:
            mess_result = "Program Not Available"
        else:
            db_session.delete(queasy)
            mess_result = "Delete Program Success"
        load_data()

    elif case_type == 4:
        load_data()
        mess_result = "Load Data Success"

    elif case_type == 5:
        load_data_list()
        mess_result = "Load Data Success"

    return generate_output()