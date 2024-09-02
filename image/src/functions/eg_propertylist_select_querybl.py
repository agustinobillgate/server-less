from functions.additional_functions import *
import decimal
from models import Eg_property, Eg_location

def eg_propertylist_select_querybl(nonr:int):
    sloc = ""
    eg_property = eg_location = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sloc, eg_property, eg_location


        return {"sloc": sloc}


    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == nonr)).first()

    if eg_property:

        eg_location = db_session.query(Eg_location).filter(
                (Eg_location.nr == eg_property.location)).first()

        if eg_location:
            sloc = eg_location.bezeich


        else:
            sloc = ""

    return generate_output()