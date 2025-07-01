#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Eg_request, Eg_location

def eg_location_btn_delartbl(location_nr:int, rec_id:int):
    err_code = 0
    eg_property = eg_request = eg_location = None

    eg_pro = eg_req = None

    Eg_pro = create_buffer("Eg_pro",Eg_property)
    Eg_req = create_buffer("Eg_req",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, eg_property, eg_request, eg_location
        nonlocal location_nr, rec_id
        nonlocal eg_pro, eg_req


        nonlocal eg_pro, eg_req

        return {"err_code": err_code}


    eg_req = db_session.query(Eg_req).filter(
             (Eg_req.location == location_nr)).first()

    eg_pro = db_session.query(Eg_pro).filter(
             (Eg_pro.location == location_nr)).first()

    if eg_req or eg_pro:
        err_code = 1

        return generate_output()

    eg_location = get_cache (Eg_location, {"_recid": [(eq, rec_id)]})

    if eg_location:
        pass
        db_session.delete(eg_location)
        pass

    return generate_output()