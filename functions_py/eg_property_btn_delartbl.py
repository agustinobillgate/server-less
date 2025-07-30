#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 30/7/2025
# gitlab: 
# if available
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property

def eg_property_btn_delartbl(case_type:int, nr:int):
    eg_property = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_property
        nonlocal case_type, nr

        return {}


    eg_property = get_cache (Eg_property, {"nr": [(eq, nr)]})

    if case_type == 1:
        # Rd 30/7/2025
        # if available
        if eg_property:
            eg_property.activeflag = False


        pass

    elif case_type == 2:
        # Rd 30/7/2025
        # if available
        if eg_property:
            db_session.delete(eg_property)

    return generate_output()