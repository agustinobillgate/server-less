from functions.additional_functions import *
import decimal
from models import Queasy, H_artikel, Htparam, Bediener, Res_history

def nt_changedprice1():
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


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 142) & (Queasy.date1 == (htparam.fdate + 1))).first()
    while None != queasy:

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.artnr == queasy.number1) & (H_artikel.departement == queasy.number2)).first()

        if h_artikel:

            hbuff = db_session.query(Hbuff).filter(
                     (Hbuff._recid == h_artikel._recid)).first()
            hbuff.epreis1 =  to_decimal(queasy.deci1)
            hbuff.epreis2 =  to_decimal(queasy.deci2)


            pass

            bediener = db_session.query(Bediener).filter(
                     (Bediener.userinit == queasy.char2)).first()
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

            qbuff = db_session.query(Qbuff).filter(
                     (Qbuff._recid == queasy._recid)).first()
            qbuff_list.remove(qbuff)
            pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 142) & (Queasy.date1 == (htparam.fdate + 1)) & (Queasy._recid > curr_recid)).first()

    return generate_output()