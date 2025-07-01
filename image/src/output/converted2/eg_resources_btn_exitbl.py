#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_resources

resources_list, Resources = create_model_like(Eg_resources)

def eg_resources_btn_exitbl(resources_list:[Resources], case_type:int, rec_id:int, fibukonto:string):

    prepare_cache ([Eg_resources])

    eg_resources = None

    resources = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_resources
        nonlocal case_type, rec_id, fibukonto


        nonlocal resources

        return {}

    resources = query(resources_list, first=True)

    if case_type == 1:
        eg_resources = Eg_resources()
        db_session.add(eg_resources)

        buffer_copy(resources, eg_resources)
        eg_resources.char1 = fibukonto

    elif case_type == 2:

        eg_resources = get_cache (Eg_resources, {"_recid": [(eq, rec_id)]})
        pass
        buffer_copy(resources, eg_resources)
        eg_resources.char1 = fibukonto


        pass

    return generate_output()