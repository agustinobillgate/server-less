from functions.additional_functions import *
import decimal
from models import Eg_request, Queasy

def egsource_btn_delartbl(source_number1:int, rec_id:int):
    err_code = 0
    eg_request = queasy = None

    egreq = None

    Egreq = Eg_request

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, eg_request, queasy
        nonlocal egreq


        nonlocal egreq
        return {"err_code": err_code}


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    egreq = db_session.query(Egreq).filter(
            (egReq.SOURCE == source_number1)).first()

    if egReq:
        err_code = 1

        return generate_output()

    queasy = db_session.query(Queasy).first()
    db_session.delete(queasy)

    return generate_output()