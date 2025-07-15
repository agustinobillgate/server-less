#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_cost

def eg_resources_btn_renartbl(resources_nr:int):
    avail_req = False
    eg_cost = None

    req = None

    Req = create_buffer("Req",Eg_cost)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_req, eg_cost
        nonlocal resources_nr
        nonlocal req


        nonlocal req

        return {"avail_req": avail_req}


    req = db_session.query(Req).filter(
             (Req.resource_nr == resources_nr)).first()

    if req:
        avail_req = True

    return generate_output()