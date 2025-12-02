#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
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

    # eg_location = get_cache (Eg_location, {"_recid": [(eq, rec_id)]})
    eg_location = db_session.query(Eg_location).filter(
             (Eg_location._recid == rec_id)).with_for_update().first()

    if eg_location:
        pass
        db_session.delete(eg_location)
        pass

    return generate_output()