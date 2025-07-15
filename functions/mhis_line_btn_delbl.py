#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mhis_line

def mhis_line_btn_delbl(rec_id:int):
    mhis_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mhis_line
        nonlocal rec_id

        return {}


    mhis_line = get_cache (Mhis_line, {"_recid": [(eq, rec_id)]})
    db_session.delete(mhis_line)

    return generate_output()