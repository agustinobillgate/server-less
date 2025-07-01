#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Segment

def prepare_rm_drecap2bl():

    prepare_cache ([Htparam])

    segmtype_exist = False
    long_digit = False
    to_date = None
    tdate = None
    fdate = None
    opening_date = None
    htparam = segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segmtype_exist, long_digit, to_date, tdate, fdate, opening_date, htparam, segment

        return {"segmtype_exist": segmtype_exist, "long_digit": long_digit, "to_date": to_date, "tdate": tdate, "fdate": fdate, "opening_date": opening_date}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    segment = get_cache (Segment, {"betriebsnr": [(gt, 0)]})

    if segment:
        segmtype_exist = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate - timedelta(days=1)
    tdate = htparam.fdate - timedelta(days=1)
    fdate = date_mdy(get_month(tdate) , 1, get_year(tdate))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 186)]})
    opening_date = htparam.fdate

    return generate_output()