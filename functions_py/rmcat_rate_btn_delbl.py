#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# if available
#-----------------------------------------

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
    # Rd, 4/8 2025
    if katpreis:
        db_session.delete(katpreis)
    
    return generate_output()