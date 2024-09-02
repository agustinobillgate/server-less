from functions.additional_functions import *
import decimal
from models import Eg_property

def eg_property_btn_exitbl(property:[Property]):
    eg_property = None

    property = None

    property_list, Property = create_model_like(Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_property


        nonlocal property
        nonlocal property_list
        return {}

    property = query(property_list, first=True)
    eg_property = Eg_property()
    db_session.add(eg_property)

    buffer_copy(property, eg_property)

    return generate_output()