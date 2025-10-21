#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------
from functions.additional_functions import *
from date import date, timedelta
from decimal import Decimal
from models import Queasy, H_artikel, Htparam, Bediener, Res_history

def nt_changedprice1():

    prepare_cache ([H_artikel, Htparam, Bediener, Res_history])

    queasy = h_artikel = htparam = bediener = res_history = None

    qbuff = hbuff = None

    Qbuff = create_buffer("Qbuff",Queasy)
    Hbuff = create_buffer("Hbuff",H_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy, h_artikel, htparam, bediener, res_history
        nonlocal qbuff, hbuff


        nonlocal qbuff, hbuff

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    queasy = get_cache (Queasy, {"key": [(eq, 142)],"date1": [(eq, htparam.fdate + timedelta(days=1))]})
    while None != queasy:

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, queasy.number1)],"departement": [(eq, queasy.number2)]})

        if h_artikel:

            hbuff = get_cache (H_artikel, {"_recid": [(eq, h_artikel._recid)]})
            hbuff.epreis1 =  to_decimal(queasy.deci1)
            hbuff.epreis2 =  to_decimal(queasy.deci2)


            pass
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, queasy.char2)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "N/A Change D" + to_string(h_artikel.departement, "99 ") +\
                    to_string(h_artikel.artnr) +\
                    "-" + h_artikel.bezeich +\
                    "; Current Price " + to_string(h_artikel.epreis1) +\
                    "; Next Price " + to_string(queasy.deci1) +\
                    "; Happy Hour Price " + to_string(queasy.deci2)
            res_history.action = "Restaurant Article"

            if bediener:
                res_history.nr = bediener.nr
            pass
            pass

            qbuff = db_session.query(Qbuff).filter(
                     (Qbuff._recid == queasy._recid)).first()
            db_session.delete(qbuff)
            pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 142) & (Queasy.date1 == (htparam.fdate + timedelta(days=1))) & (Queasy._recid > curr_recid)).first()

    return generate_output()