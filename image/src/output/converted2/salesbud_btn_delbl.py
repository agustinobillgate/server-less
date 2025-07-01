#using conversion tools version: 1.0.0.111

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
    db_session.delete(salesbud)
    pass

    return generate_output()