from functions.additional_functions import *
import decimal
from models import Eg_property

def eg_property_btn_delartbl(case_type:int, nr:int):
    eg_property = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_property


        return {}


    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == nr)).first()

    if case_type == 1:

        eg_property = db_session.query(Eg_property).first()
        eg_property.activeflag = False


    elif case_type == 2:

        eg_property = db_session.query(Eg_property).first()
        db_session.delete(eg_property)

    return generate_output()