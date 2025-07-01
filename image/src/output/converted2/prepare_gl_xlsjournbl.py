#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
from functions.htpdate import htpdate

def prepare_gl_xlsjournbl():
    p_977 = ""
    p_558 = None
    p_597 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_977, p_558, p_597

        return {"p_977": p_977, "p_558": p_558, "p_597": p_597}

    p_977 = get_output(htpchar(977))
    p_558 = get_output(htpdate(558))
    p_597 = get_output(htpdate(597))

    return generate_output()