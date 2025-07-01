#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Messages, Bediener

def messages_get_messagebl(m_mess_recid:int):

    prepare_cache ([Bediener])

    username = ""
    t_messages_list = []
    messages = bediener = None

    t_messages = None

    t_messages_list, T_messages = create_model_like(Messages, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal username, t_messages_list, messages, bediener
        nonlocal m_mess_recid


        nonlocal t_messages
        nonlocal t_messages_list

        return {"username": username, "t-messages": t_messages_list}

    messages = get_cache (Messages, {"_recid": [(eq, m_mess_recid)]})

    bediener = get_cache (Bediener, {"usercode": [(eq, messages.usre)]})

    if bediener:
        username = bediener.username
    else:

        bediener = get_cache (Bediener, {"userinit": [(eq, messages.usre)]})

        if bediener:
            username = bediener.username
        else:
            username = ""
    t_messages = T_messages()
    t_messages_list.append(t_messages)

    buffer_copy(messages, t_messages)
    t_messages.rec_id = messages._recid

    return generate_output()