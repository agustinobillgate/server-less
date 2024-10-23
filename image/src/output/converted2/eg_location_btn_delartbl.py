from functions.additional_functions import *
import decimal
from models import Eg_property, Eg_request, Eg_location

def eg_location_btn_delartbl(location_nr:int, rec_id:int):
    err_code = 0
    eg_property = eg_request = eg_location = None

    egreq = egpro = None

    Egreq = create_buffer("Egreq",Eg_property)
    Egpro = create_buffer("Egpro",Eg_request)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, eg_property, eg_request, eg_location
        nonlocal location_nr, rec_id
        nonlocal egreq, egpro


        nonlocal egreq, egpro
        return {"err_code": err_code}


    egreq = db_session.query(Egreq).filter(
             (egreq.location == location_nr)).first()

    egpro = db_session.query(Egpro).filter(
             (egPro.location == location_nr)).first()

    if egreq or egPro:
        err_code = 1

        return generate_output()

    eg_location = db_session.query(Eg_location).filter(
             (Eg_location._recid == rec_id)).first()
    db_session.delete(eg_location)
    pass

    return generate_output()