#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_earlyco_glistbl():
    ci_date = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date

        return {"ci_date": ci_date}

    ci_date = get_output(htpdate(87))

    return generate_output()