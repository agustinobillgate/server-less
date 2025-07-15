#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line

def nsargt_admin_btn_cancartbl(rec_id:int):
    argt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_line
        nonlocal rec_id

        return {}


    argt_line = get_cache (Argt_line, {"_recid": [(eq, rec_id)]})
    pass
    db_session.delete(argt_line)

    return generate_output()