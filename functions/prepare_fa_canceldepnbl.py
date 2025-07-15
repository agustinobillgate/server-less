#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_fa_canceldepnbl():
    datum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum

        return {"datum": datum}

    datum = get_output(htpdate(881))

    return generate_output()