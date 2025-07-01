#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_fo_usrjournalbl():
    from_date = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date

        return {"from_date": from_date}

    from_date = get_output(htpdate(110))

    return generate_output()