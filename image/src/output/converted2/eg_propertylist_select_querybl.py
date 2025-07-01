#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Eg_location

def eg_propertylist_select_querybl(nonr:int):

    prepare_cache ([Eg_property, Eg_location])

    sloc = ""
    eg_property = eg_location = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sloc, eg_property, eg_location
        nonlocal nonr

        return {"sloc": sloc}


    eg_property = get_cache (Eg_property, {"nr": [(eq, nonr)]})

    if eg_property:

        eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

        if eg_location:
            sloc = eg_location.bezeich


        else:
            sloc = ""

    return generate_output()