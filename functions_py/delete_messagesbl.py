#using conversion tools version: 1.0.0.119
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Messages

messbuff_data, Messbuff = create_model_like(Messages)

def delete_messagesbl(messbuff_data:[Messbuff]):
    success_flag = False
    messages = None

    messbuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, messages


        nonlocal messbuff

        return {"success_flag": success_flag}

    messbuff = query(messbuff_data, first=True)

    # messages = get_cache (Messages, {"gastnr": [(eq, messbuff.gastnr)],"zeit": [(eq, messbuff.zeit)],"name": [(eq, messbuff.name)]})
    messages = db_session.query(Messages).filter(Messages.gastnr == messbuff.gastnr, 
                                                 Messages.zeit == messbuff.zeit, Messages.name == messbuff.name).with_for_update().first()

    if messages:
        db_session.delete(messages)
        pass
        success_flag = True

    return generate_output()