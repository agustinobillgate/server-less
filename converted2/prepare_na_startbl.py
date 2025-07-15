#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Nation

def prepare_na_startbl():

    prepare_cache ([Htparam, Nation])

    def_natcode = ""
    na_date = None
    na_time = 0
    na_name = ""
    htparam = nation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal def_natcode, na_date, na_time, na_name, htparam, nation

        return {"def_natcode": def_natcode, "na_date": na_date, "na_time": na_time, "na_name": na_name}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 276)]})

    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

    if nation:
        def_natcode = nation.kurzbez

    htparam = get_cache (Htparam, {"paramnr": [(eq, 102)]})
    na_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 103)]})
    na_time = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
    na_name = htparam.fchar

    return generate_output()