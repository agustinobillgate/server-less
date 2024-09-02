from functions.additional_functions import *
import decimal
from models import Eg_resources

def eg_resources_btn_exitbl(resources:[Resources], case_type:int, rec_id:int, fibukonto:str):
    eg_resources = None

    resources = None

    resources_list, Resources = create_model_like(Eg_resources)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_resources


        nonlocal resources
        nonlocal resources_list
        return {}

    resources = query(resources_list, first=True)

    if case_type == 1:
        eg_resources = Eg_resources()
        db_session.add(eg_resources)

        buffer_copy(resources, eg_resources)
        eg_resources.char1 = fibukonto

    elif case_type == 2:

        eg_resources = db_session.query(Eg_resources).filter(
                (Eg_resources._recid == rec_id)).first()

        eg_resources = db_session.query(Eg_resources).first()
        buffer_copy(resources, eg_resources)
        eg_resources.char1 = fibukonto

        eg_resources = db_session.query(Eg_resources).first()

    return generate_output()