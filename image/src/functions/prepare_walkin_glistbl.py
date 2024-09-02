from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Segment

def prepare_walkin_glistbl():
    ci_date = None
    walk_in = 0
    wi_grp = 0
    htparam = segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, walk_in, wi_grp, htparam, segment


        return {"ci_date": ci_date, "walk_in": walk_in, "wi_grp": wi_grp}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 48)).first()

    segment = db_session.query(Segment).filter(
            (Segment.segmentcode == htparam.finteger)).first()

    if not segment:

        return generate_output()
    walk_in = htparam.finteger
    wi_grp = segmentgrup

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    return generate_output()