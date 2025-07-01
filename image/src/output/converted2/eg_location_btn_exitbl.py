#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location

location_list, Location = create_model_like(Eg_location)

def eg_location_btn_exitbl(case_type:int, rec_id:int, location_list:[Location]):
    eg_location = None

    location = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_location
        nonlocal case_type, rec_id


        nonlocal location

        return {}

    location = query(location_list, first=True)

    if case_type == 1:
        eg_location = Eg_location()
        db_session.add(eg_location)

        buffer_copy(location, eg_location)

    elif case_type == 2:

        eg_location = get_cache (Eg_location, {"_recid": [(eq, rec_id)]})
        pass
        buffer_copy(location, eg_location)
        pass

    return generate_output()