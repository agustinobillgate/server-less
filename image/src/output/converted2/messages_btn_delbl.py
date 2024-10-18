from functions.additional_functions import *
import decimal
from models import Messages

def messages_btn_delbl(rec_id:int):
    messages = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal messages
        nonlocal rec_id


        return {}


    messages = db_session.query(Messages).filter(
             (Messages._recid == rec_id)).first()
    db_session.delete(messages)
    pass

    return generate_output()