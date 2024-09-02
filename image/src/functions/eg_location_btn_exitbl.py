from functions.additional_functions import *
import decimal
from models import Eg_location

def eg_location_btn_exitbl(case_type:int, rec_id:int, location:[Location]):
    eg_location = None

    location = None

    location_list, Location = create_model_like(Eg_location)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_location


        nonlocal location
        nonlocal location_list
        return {}

    location = query(location_list, first=True)

    if case_type == 1:
        eg_location = Eg_location()
        db_session.add(eg_location)

        buffer_copy(location, eg_location)

    elif case_type == 2:

        eg_location = db_session.query(Eg_location).filter(
                (Eg_location._recid == rec_id)).first()

        eg_location = db_session.query(Eg_location).first()
        buffer_copy(location, eg_location)

        eg_location = db_session.query(Eg_location).first()

    return generate_output()