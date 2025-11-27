#using conversion tools version: 1.0.0.117

# =========================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_request, Queasy

def egsource_btn_delartbl(source_number1:int, rec_id:int):

    prepare_cache ([Eg_request])

    err_code = 0
    eg_request = queasy = None

    egreq = None

    Egreq = create_buffer("Egreq",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, eg_request, queasy
        nonlocal source_number1, rec_id
        nonlocal egreq


        nonlocal egreq

        return {"err_code": err_code}


    # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).with_for_update().first()

    egreq = get_cache (Eg_request, {"source": [(eq, source_number1)]})

    if egreq:
        err_code = 1

        return generate_output()
    # pass
    db_session.delete(queasy)
    db_session.refresh(queasy,with_for_update=True)

    return generate_output()
