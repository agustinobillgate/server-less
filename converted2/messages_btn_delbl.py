#using conversion tools version: 1.0.0.117

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


    messages = get_cache (Messages, {"_recid": [(eq, rec_id)]})
    pass
    db_session.delete(messages)
    pass

    return generate_output()