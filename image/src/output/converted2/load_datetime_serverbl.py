#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def load_datetime_serverbl():
    datetime_server = ""
    bill_date:date = None
    curr_zeit:int = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datetime_server, bill_date, curr_zeit

        return {"datetime_server": datetime_server}

    curr_zeit = get_current_time_in_seconds()
    datetime_server = to_string(get_current_date()) + " " + to_string(curr_zeit, "HH:MM:SS")

    return generate_output()