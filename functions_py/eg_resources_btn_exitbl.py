#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 1/8/2025
# if available 
#----------------------------------------

# =========================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# =========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_resources

resources_data, Resources = create_model_like(Eg_resources)

def eg_resources_btn_exitbl(resources_data:[Resources], case_type:int, rec_id:int, fibukonto:string):

    prepare_cache ([Eg_resources])

    eg_resources = None

    resources = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_resources
        nonlocal case_type, rec_id, fibukonto


        nonlocal resources

        return {}

    resources = query(resources_data, first=True)

    if case_type == 1:
        eg_resources = Eg_resources()
        db_session.add(eg_resources)

        buffer_copy(resources, eg_resources)
        eg_resources.char1 = fibukonto

    elif case_type == 2:

        # eg_resources = get_cache (Eg_resources, {"_recid": [(eq, rec_id)]})
        eg_resources = db_session.query(Eg_resources).filter(
             (Eg_resources._recid == rec_id)).with_for_update().first()
        pass
        buffer_copy(resources, eg_resources)
        eg_resources.char1 = fibukonto

        db_session.refresh(eg_resources,with_for_update=True)

    return generate_output()