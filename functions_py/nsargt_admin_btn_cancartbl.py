#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
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


    # argt_line = get_cache (Argt_line, {"_recid": [(eq, rec_id)]})
    argt_line = db_session.query(Argt_line).filter(
             (Argt_line._recid == rec_id)).with_for_update().first()
    db_session.delete(argt_line)

    return generate_output()