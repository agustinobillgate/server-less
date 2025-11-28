#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Messages

def messages_btn_delbl(rec_id:int):
    messages = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal messages
        nonlocal rec_id

        return {}


    # messages = get_cache (Messages, {"_recid": [(eq, rec_id)]})
    messages = db_session.query(Messages).filter(Messages._recid == rec_id).with_for_update().first()
    pass
    db_session.delete(messages)
    pass

    return generate_output()