#------------------------------------------
# Rd, 22/11/2025
# get last counter dengan next_counter_for_update
#------------------------------------------
from functions.additional_functions import *
from models import Counters
from sqlalchemy.exc import NoResultFound

db_session = local_storage.db_session


def next_counter_for_update(counter_no: int) -> int:
    error_lock:str = ""
    new_value:int = 0

    def generate_output():
        nonlocal new_value, error_lock

        return {"counter": new_value, "error": error_lock}

    try:
        # try locking existing row
        row = (
            db_session.query(Counters)
            .filter(Counters.counter_no == counter_no)
            .with_for_update(nowait=False)
            .first()
        )
        row.counter += 1
        new_value = row.counter

    except NoResultFound:
        # if row missing → create new one starting from 1
        row = Counters(counter_no=counter_no, counter=1, counter_bez=to_string(counter_no))
        db_session.add(row)
        row.counter = 1
        new_value = 1

    except Exception as e:
        # IMPORTANT: rollback failed transactions
        db_session.rollback()
        error_lock = str(e)
        # raise e

    # commit if needed
    db_session.commit()

    return generate_output()