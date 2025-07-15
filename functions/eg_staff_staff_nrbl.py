#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_staff

def eg_staff_staff_nrbl(rec_id:int, staff_nr:int, curr_select:string):

    prepare_cache ([Eg_staff])

    avail_sub = False
    eg_staff = None

    sub = None

    Sub = create_buffer("Sub",Eg_staff)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_staff
        nonlocal rec_id, staff_nr, curr_select
        nonlocal sub


        nonlocal sub

        return {"avail_sub": avail_sub}


    eg_staff = get_cache (Eg_staff, {"_recid": [(eq, rec_id)]})

    if curr_select.lower()  == ("chg").lower() :

        sub = get_cache (Eg_staff, {"nr": [(eq, staff_nr)],"_recid": [(ne, eg_staff._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        sub = get_cache (Eg_staff, {"nr": [(eq, staff_nr)]})

    if sub:
        avail_sub = True

    return generate_output()