#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_staff

def eg_chgreq_assign_tobl(request1_deptnum:int, request1_assign_to:int):

    prepare_cache ([Eg_staff])

    avail_usr = False
    usr_name = ""
    eg_staff = None

    usr1 = None

    Usr1 = create_buffer("Usr1",Eg_staff)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_usr, usr_name, eg_staff
        nonlocal request1_deptnum, request1_assign_to
        nonlocal usr1


        nonlocal usr1

        return {"avail_usr": avail_usr, "usr_name": usr_name}


    usr1 = get_cache (Eg_staff, {"usergroup": [(eq, request1_deptnum)],"activeflag": [(eq, True)],"nr": [(eq, request1_assign_to)]})

    if usr1:
        avail_usr = True
        usr_name = usr1.name

    return generate_output()