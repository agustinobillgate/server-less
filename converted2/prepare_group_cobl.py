#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htpdate import htpdate

def prepare_group_cobl():
    htp__int = 0
    ci_datum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htp__int, ci_datum

        return {"htp__int": htp__int, "ci_datum": ci_datum}

    htp__int = get_output(htpint(297))
    ci_datum = get_output(htpdate(87))

    return generate_output()