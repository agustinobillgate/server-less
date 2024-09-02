from functions.additional_functions import *
import decimal
from models import Eg_cost, Eg_resources

def eg_resources_btn_delartbl(rec_id:int, resources_nr:int):
    fl_code = 0
    eg_cost = eg_resources = None

    egreq = None

    Egreq = Eg_cost

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_cost, eg_resources
        nonlocal egreq


        nonlocal egreq
        return {"fl_code": fl_code}


    egreq = db_session.query(Egreq).filter(
            (egReq.resource_nr == resources_nr)).first()

    if egReq:
        fl_code = 1

        return generate_output()

    eg_resources = db_session.query(Eg_resources).filter(
            (Eg_resources._recid == rec_id)).first()

    eg_resources = db_session.query(Eg_resources).first()
    db_session.delete(eg_resources)


    return generate_output()