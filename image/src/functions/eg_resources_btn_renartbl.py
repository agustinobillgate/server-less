from functions.additional_functions import *
import decimal
from models import Eg_cost

def eg_resources_btn_renartbl(resources_nr:int):
    avail_req = False
    eg_cost = None

    req = None

    Req = Eg_cost

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_req, eg_cost
        nonlocal req


        nonlocal req
        return {"avail_req": avail_req}


    req = db_session.query(Req).filter(
            (Req.resource_nr == resources_nr)).first()

    if req:
        avail_req = True

    return generate_output()