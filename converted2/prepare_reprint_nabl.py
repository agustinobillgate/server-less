#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.reprint_nabl import reprint_nabl
from models import Htparam

def prepare_reprint_nabl():

    prepare_cache ([Htparam])

    store_flag = False
    na_date = None
    na_time = 0
    na_name = ""
    b1_list_data = []
    htparam = None

    b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"reihenfolge":int, "hogarest":int, "bezeichnun":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal store_flag, na_date, na_time, na_name, b1_list_data, htparam


        nonlocal b1_list
        nonlocal b1_list_data

        return {"store_flag": store_flag, "na_date": na_date, "na_time": na_time, "na_name": na_name, "b1-list": b1_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 230)]})

    if htparam.feldtyp == 4 and htparam.flogical:
        store_flag = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    na_date = htparam.fdate - timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 103)]})
    na_time = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
    na_name = htparam.fchar
    b1_list_data = get_output(reprint_nabl())

    return generate_output()