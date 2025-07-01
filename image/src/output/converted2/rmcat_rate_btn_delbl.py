#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Katpreis

def rmcat_rate_btn_delbl(rec_id:int):
    katpreis = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal katpreis
        nonlocal rec_id

        return {}


    katpreis = get_cache (Katpreis, {"_recid": [(eq, rec_id)]})
    pass
    db_session.delete(katpreis)
    pass

    return generate_output()