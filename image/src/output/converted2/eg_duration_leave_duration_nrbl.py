#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_duration

def eg_duration_leave_duration_nrbl(curr_select:string, duration_duration_nr:int, rec_id:int):

    prepare_cache ([Eg_duration])

    fl_code = False
    eg_duration = None

    queasy1 = None

    Queasy1 = create_buffer("Queasy1",Eg_duration)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_duration
        nonlocal curr_select, duration_duration_nr, rec_id
        nonlocal queasy1


        nonlocal queasy1

        return {"fl_code": fl_code}


    eg_duration = get_cache (Eg_duration, {"_recid": [(eq, rec_id)]})

    if curr_select.lower()  == ("chg").lower() :

        queasy1 = get_cache (Eg_duration, {"duration_nr": [(eq, duration_duration_nr)],"_recid": [(ne, eg_duration._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        queasy1 = get_cache (Eg_duration, {"duration_nr": [(eq, duration_duration_nr)]})

    if queasy1:
        fl_code = True

    return generate_output()