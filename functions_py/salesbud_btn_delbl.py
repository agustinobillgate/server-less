#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 04/08/2025
# gitlab: -
# remarks: -
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Salesbud

def salesbud_btn_delbl(rec_id:int):
    salesbud = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal salesbud
        nonlocal rec_id

        return {}


    salesbud = get_cache (Salesbud, {"_recid": [(eq, rec_id)]})
    # Rd 4/8/2025
    if salesbud:
        db_session.delete(salesbud)
    
    return generate_output()