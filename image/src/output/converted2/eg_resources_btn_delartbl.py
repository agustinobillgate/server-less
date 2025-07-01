#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_cost, Eg_resources

def eg_resources_btn_delartbl(rec_id:int, resources_nr:int):

    prepare_cache ([Eg_cost])

    fl_code = 0
    eg_cost = eg_resources = None

    egreq = None

    Egreq = create_buffer("Egreq",Eg_cost)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_cost, eg_resources
        nonlocal rec_id, resources_nr
        nonlocal egreq


        nonlocal egreq

        return {"fl_code": fl_code}


    egreq = get_cache (Eg_cost, {"resource_nr": [(eq, resources_nr)]})

    if egreq:
        fl_code = 1

        return generate_output()

    eg_resources = get_cache (Eg_resources, {"_recid": [(eq, rec_id)]})

    if eg_resources:
        pass
        db_session.delete(eg_resources)
        pass

    return generate_output()