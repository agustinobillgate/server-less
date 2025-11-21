from functions.additional_functions import *
from models import Bill, Counters
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from functions import log_program

import datetime
import time

# 49, 95, 112


def next_counter_for_update(db_session: Session, counter_no: int) -> int:
    try:
        row = (
            db_session.query(Counters)
            .filter(Counters.counter_no == counter_no)
            .with_for_update()      # <-- SELECT ... FOR UPDATE
            .one()
        )
    except NoResultFound:
        pass

    row.counter += 1
    return row.counter

def prepare_mk_hmenu_webbl(test:int):

    target = datetime.datetime(2025, 11, 21, 10, 8, 0)

    # log_program.write_log("debug-oscar", f"time: {datetime.datetime.now()}", "log_oscar.txt")

    while datetime.datetime.now() < target:
        log_program.write_log("debug-oscar","wait","log_oscar.txt")
        time.sleep(1)

    log_program.write_log("debug-oscar", f"start-recid: {test}","log_oscar.txt")
    
    bill = counters = None

    db_session = local_storage.db_session

    bill = db_session.query(Bill).filter(Bill._recid == test).first()


    if bill.rechnr == 0:
        # counters = db_session.query(Counters).filter((Counters.counter_no == 3)).first()
        # counters.counter = counters.counter + 1
        bill.rechnr = next_counter_for_update(db_session, 3)
        db_session.commit()