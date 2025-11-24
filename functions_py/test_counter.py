#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guest_pr
from functions.next_counter_for_update import next_counter_for_update

def test_counter(bookengid:int):

    db_session = local_storage.db_session
    last_counter:int = 0
    error_str = ""

    def generate_output():

        return {"last_counter": last_counter, "error_lock": error_lock}

    last_counter, error_lock = get_output(next_counter_for_update(bookengid))

    return generate_output()

