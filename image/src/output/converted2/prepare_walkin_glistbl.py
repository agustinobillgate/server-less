#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Segment

def prepare_walkin_glistbl():

    prepare_cache ([Htparam, Segment])

    ci_date = None
    walk_in = 0
    wi_grp = 0
    htparam = segment = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, walk_in, wi_grp, htparam, segment

        return {"ci_date": ci_date, "walk_in": walk_in, "wi_grp": wi_grp}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 48)]})

    segment = get_cache (Segment, {"segmentcode": [(eq, htparam.finteger)]})

    if not segment:

        return generate_output()
    walk_in = htparam.finteger
    wi_grp = segment.segmentgrup

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    return generate_output()