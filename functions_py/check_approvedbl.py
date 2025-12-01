#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Messages

def check_approvedbl(docu_nr:string):

    prepare_cache ([Queasy])

    current_approval:int = 0
    last_approval:int = 0
    queasy = messages = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal current_approval, last_approval, queasy, messages
        nonlocal docu_nr

        return {}


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 245) & (Queasy.char1 == (docu_nr).lower())).order_by(Queasy.number1.desc()).all():
        current_approval = queasy.number1
        break

    # messages = get_cache (Messages, {"zinr": [(eq, docu_nr)]})
    messages = db_session.query(Messages).filter(
             (Messages.zinr == docu_nr)).with_for_update().first()

    if messages:
        last_approval = to_int(messages.messtext[8])

        if current_approval != last_approval:
            db_session.delete(messages)

    return generate_output()