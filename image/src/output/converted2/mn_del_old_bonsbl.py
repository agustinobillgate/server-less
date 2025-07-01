#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy

def mn_del_old_bonsbl():

    prepare_cache ([Htparam])

    ci_date:date = None
    active_deposit:bool = False
    htparam = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, active_deposit, htparam, queasy

        return {}

    def del_old_bons():

        nonlocal ci_date, active_deposit, htparam, queasy

        bill_date:date = None
        anz:int = 0
        qsy = None
        q251 = None
        qkds_header = None
        qkds_line = None
        Qsy =  create_buffer("Qsy",Queasy)
        Q251 =  create_buffer("Q251",Queasy)
        Qkds_header =  create_buffer("Qkds_header",Queasy)
        Qkds_line =  create_buffer("Qkds_line",Queasy)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        htparam = get_cache (Htparam, {"paramnr": [(eq, 164)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 7

        queasy = get_cache (Queasy, {"key": [(eq, 3)],"date1": [(lt, bill_date)]})
        while None != queasy:
            pass
            db_session.delete(queasy)

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 3) & (Queasy.date1 < bill_date) & (Queasy._recid > curr_recid)).first()

        qkds_line = db_session.query(Qkds_line).filter(
                 (Qkds_line.key == 255) & (Qkds_line.char1 == ("kds-line").lower()) & (Qkds_line.date1 == bill_date)).first()
        while None != qkds_line:
            pass
            qkds_line.char3 = "4"
            pass
            pass

            curr_recid = qkds_line._recid
            qkds_line = db_session.query(Qkds_line).filter(
                     (Qkds_line.key == 255) & (Qkds_line.char1 == ("kds-line").lower()) & (Qkds_line.date1 == bill_date) & (Qkds_line._recid > curr_recid)).first()

        qkds_header = db_session.query(Qkds_header).filter(
                 (Qkds_header.key == 257) & (Qkds_header.char1 == ("kds-header").lower()) & (Qkds_header.date1 == bill_date)).first()
        while None != qkds_header:
            pass
            qkds_header.deci2 =  to_decimal("4")
            pass
            pass

            curr_recid = qkds_header._recid
            qkds_header = db_session.query(Qkds_header).filter(
                     (Qkds_header.key == 257) & (Qkds_header.char1 == ("kds-header").lower()) & (Qkds_header.date1 == bill_date) & (Qkds_header._recid > curr_recid)).first()

        if active_deposit:

            queasy = get_cache (Queasy, {"key": [(eq, 33)],"date1": [(le, (ci_date - anz))]})
            while None != queasy:

                q251 = db_session.query(Q251).filter(
                             (Q251.key == 251) & (Q251.number2 == to_int(queasy._recid))).first()

                if q251:
                    db_session.delete(q251)
                    pass

                qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == queasy._recid)).first()
                db_session.delete(qsy)
                pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 33) & (Queasy.date1 <= (ci_date - timedelta(days=anz))) & (Queasy._recid > curr_recid)).first()
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 33)],"date1": [(le, (ci_date - 730))]})
            while None != queasy:

                qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == queasy._recid)).first()
                db_session.delete(qsy)
                pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 33) & (Queasy.date1 <= (ci_date - timedelta(days=730))) & (Queasy._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 588)]})

    if htparam:
        active_deposit = htparam.flogical
    del_old_bons()

    return generate_output()