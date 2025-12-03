#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def close_inventory_endbl(user_init:string):

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam
        nonlocal user_init

        return {}

    htparam = db_session.query(Htparam).filter(Htparam.paramnr == 232).with_for_update().first()
    htparam.flogical = False
    htparam.lupdate = get_current_date()
    htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
    pass

    return generate_output()