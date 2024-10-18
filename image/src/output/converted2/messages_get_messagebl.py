from functions.additional_functions import *
import decimal
from models import Messages, Bediener

def messages_get_messagebl(m_mess_recid:int):
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

    messages = db_session.query(Messages).filter(
             (Messages._recid == m_mess_recid)).first()

    bediener = db_session.query(Bediener).filter(
             (Bediener.usercode == messages.usre)).first()

    if bediener:
        username = bediener.username
    else:

        bediener = db_session.query(Bediener).filter(
                 (Bediener.userinit == messages.usre)).first()

        if bediener:
            username = bediener.username
        else:
            username = ""
    t_messages = T_messages()
    t_messages_list.append(t_messages)

    buffer_copy(messages, t_messages)
    t_messages.rec_id = messages._recid

    return generate_output()