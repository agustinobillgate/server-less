#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.upload_imagesetupbl import upload_imagesetupbl
from models import Akt_line, Counters
from functions.next_counter_for_update import next_counter_for_update

akt_line1_data, Akt_line1 = create_model_like(Akt_line)

def mk_aktline_btn_exit_webbl(akt_line1_data:[Akt_line1], prior:string, case_type:int, base64file:string, user_init:string):

    prepare_cache ([Counters])

    result_message = ""
    curr_counter:int = 0
    akt_line = counters = None

    akt_line1 = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    prior = prior.strip()
    base64file = base64file.strip()
    user_init = user_init.strip()

    def generate_output():
        nonlocal result_message, curr_counter, akt_line, counters
        nonlocal akt_line1_data, prior, case_type, base64file, user_init


        nonlocal akt_line1

        return {"result_message": result_message}

    def init_prior():

        nonlocal result_message, curr_counter, akt_line, counters
        nonlocal akt_line1_data, prior, case_type, base64file, user_init


        nonlocal akt_line1

        if prior.lower()  == ("Low").lower() :
            akt_line1.prioritaet = 1

        elif prior.lower()  == ("Medium").lower() :
            akt_line1.prioritaet = 2

        elif prior.lower()  == ("High").lower() :
            akt_line1.prioritaet = 3


    akt_line1 = query(akt_line1_data, first=True)

    counters = get_cache (Counters, {"counter_no": [(eq, 27)]})

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 27
        counters.counter_bez = "Counter for sales activity-line"
    # counters.counter = counters.counter + 1
    
    last_count, error_lock = get_output(next_counter_for_update(27))

    # akt_line1.linenr = counters.counter
    # curr_counter = counters.counter
    # pass
    akt_line1.linenr = last_count
    curr_counter = last_count
    
    init_prior()
    akt_line = Akt_line()
    db_session.add(akt_line)

    buffer_copy(akt_line1, akt_line)

    if (base64file != "" or base64file != None) and user_init != "":
        result_message = get_output(upload_imagesetupbl(case_type, base64file, user_init, curr_counter))

    return generate_output()