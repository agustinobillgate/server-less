from functions.additional_functions import *
import decimal
from functions.upload_imagesetupbl import upload_imagesetupbl
from models import Akt_line, Counters

def mk_aktline_btn_exit_webbl(akt_line1:[Akt_line1], prior:str, case_type:int, base64file:str, user_init:str):
    result_message = ""
    curr_counter:int = 0
    akt_line = counters = None

    akt_line1 = None

    akt_line1_list, Akt_line1 = create_model_like(Akt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, curr_counter, akt_line, counters


        nonlocal akt_line1
        nonlocal akt_line1_list
        return {"result_message": result_message}

    def init_prior():

        nonlocal result_message, curr_counter, akt_line, counters


        nonlocal akt_line1
        nonlocal akt_line1_list

        if prior.lower()  == "Low":
            akt_line1.prioritaet = 1

        elif prior.lower()  == "Medium":
            akt_line1.prioritaet = 2

        elif prior.lower()  == "High":
            akt_line1.prioritaet = 3

    akt_line1 = query(akt_line1_list, first=True)

    counters = db_session.query(Counters).filter(
            (Counters.counter_no == 27)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 27
        counters.counter_bez = "Counter for sales activity_line"
    counters = counters + 1
    akt_line1.linenr = counters
    curr_counter = counters

    counters = db_session.query(Counters).first()
    init_prior()
    akt_line = Akt_line()
    db_session.add(akt_line)

    buffer_copy(akt_line1, akt_line)

    if (base64file != "" or base64file != None) and user_init != "":
        result_message = get_output(upload_imagesetupbl(case_type, base64file, user_init, curr_counter))

    return generate_output()