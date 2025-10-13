#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Messages, Bediener

def messages_get_messagebl(m_mess_recid:int):

    prepare_cache ([Bediener])

    username = ""
    t_messages_data = []
    messages = bediener = None

    t_messages = None

    t_messages_data, T_messages = create_model_like(Messages, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal username, t_messages_data, messages, bediener
        nonlocal m_mess_recid


        nonlocal t_messages
        nonlocal t_messages_data
        
        return {"username": username, "t-messages": t_messages_data}

    # messages = get_cache (Messages, {"_recid": [(eq, m_mess_recid)]})
    messages = db_session.query(Messages).filter(
             (Messages._recid == m_mess_recid)).first()

    # bediener = get_cache (Bediener, {"usercode": [(eq, messages.usre)]})
    bediener = db_session.query(Bediener).filter(
             (Bediener.usercode == messages.usre)).first()

    if bediener:
        username = bediener.username
    else:

        # bediener = get_cache (Bediener, {"userinit": [(eq, messages.usre)]})
        bediener = db_session.query(Bediener).filter(
                 (Bediener.userinit == messages.usre)).first()

        if bediener:
            username = bediener.username
        else:
            username = ""
    t_messages = T_messages()
    t_messages_data.append(t_messages)

    buffer_copy(messages, t_messages)
    t_messages.rec_id = messages._recid

    return generate_output()