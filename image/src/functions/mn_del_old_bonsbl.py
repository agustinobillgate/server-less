from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Queasy

def mn_del_old_bonsbl():
    ci_date:date = None
    active_deposit:bool = False
    htparam = queasy = None

    qsy = q251 = None

    Qsy = Queasy
    Q251 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, active_deposit, htparam, queasy
        nonlocal qsy, q251


        nonlocal qsy, q251
        return {}

    def del_old_bons():

        nonlocal ci_date, active_deposit, htparam, queasy
        nonlocal qsy, q251


        nonlocal qsy, q251

        bill_date:date = None
        anz:int = 0
        Qsy = Queasy
        Q251 = Queasy

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 164)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 7

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 3) &  (Queasy.date1 < bill_date)).first()
        while None != queasy:

            queasy = db_session.query(Queasy).first()
            db_session.delete(queasy)


            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 3) &  (Queasy.date1 < bill_date)).first()

        if active_deposit:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 33) &  (Queasy.date1 <= (ci_date - anz))).first()
            while None != queasy:

                q251 = db_session.query(Q251).filter(
                            (Q251.key == 251) &  (Q251.number2 == to_int(queasy._recid))).first()

                if q251:
                    db_session.delete(q251)


                qsy = db_session.query(Qsy).filter(
                            (Qsy._recid == queasy._recid)).first()
                db_session.delete(qsy)

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 33) &  (Queasy.date1 <= (ci_date - anz))).first()
        else:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 33) &  (Queasy.date1 <= (ci_date - 730))).first()
            while None != queasy:

                qsy = db_session.query(Qsy).filter(
                            (Qsy._recid == queasy._recid)).first()
                db_session.delete(qsy)

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 33) &  (Queasy.date1 <= (ci_date - 730))).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 588)).first()

    if htparam:
        active_deposit = htparam.flogical
    del_old_bons()

    return generate_output()