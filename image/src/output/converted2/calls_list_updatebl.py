#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Calls

def calls_list_updatebl(i_case:int, s_recid:int, destination:string):

    prepare_cache ([Calls])

    calls = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal calls
        nonlocal i_case, s_recid, destination

        return {}


    calls = get_cache (Calls, {"_recid": [(eq, s_recid)]})

    if calls:

        if i_case == 1:
            calls.satz_id = destination

        elif i_case == 2:
            calls.betriebsnr = 0
        pass

    return generate_output()