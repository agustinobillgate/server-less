#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.clclosingbl import clclosingbl
from models import Htparam

def mn_club_softwarebl():

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1114)]})

    if htparam.flogical:
        get_output(clclosingbl())

    htparam = get_cache (Htparam, {"paramnr": [(eq, 592)]})

    if htparam.flogical:

        return generate_output()
    pass
    htparam.flogical = True
    pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 592)]})
    htparam.fchar = "Midnight Program"
    htparam.fdate = get_current_date()
    htparam.finteger = get_current_time_in_seconds()
    htparam.flogical = False
    pass

    return generate_output()