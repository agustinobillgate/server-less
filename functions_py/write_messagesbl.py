#using conversion tools version: 1.0.0.119
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Messages

messbuff_data, Messbuff = create_model_like(Messages)
t_messages_data, T_messages = create_model_like(Messages)

def write_messagesbl(case_type:int, messbuff_data:[Messbuff], t_messages_data:[T_messages]):
    success_flag = False
    messages = None

    t_messages = messbuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, messages
        nonlocal case_type


        nonlocal t_messages, messbuff

        return {"success_flag": success_flag}


    messbuff = query(messbuff_data, first=True)

    t_messages = query(t_messages_data, first=True)

    if case_type != 0:

        # messages = get_cache (Messages, {"gastnr": [(eq, messbuff.gastnr)],"zeit": [(eq, messbuff.zeit)],"name": [(eq, messbuff.name)]})
        messages = db_session.query(Messages).filter(Messages.gastnr == messbuff.gastnr, 
                                                 Messages.zeit == messbuff.zeit, Messages.name == messbuff.name).with_for_update().first()

        if messages:

            if case_type == 1:
                buffer_copy(t_messages, messages)
                pass
                success_flag = True

            elif case_type == 2:
                db_session.delete(messages)
    else:
        messages = Messages()
        db_session.add(messages)

        buffer_copy(t_messages, messages)
        success_flag = True

    return generate_output()