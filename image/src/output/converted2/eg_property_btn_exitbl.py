#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property

property_list, Property = create_model_like(Eg_property)

def eg_property_btn_exitbl(property_list:[Property]):
    eg_property = None

    property = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_property


        nonlocal property

        return {}

    property = query(property_list, first=True)
    eg_property = Eg_property()
    db_session.add(eg_property)

    buffer_copy(property, eg_property)

    return generate_output()