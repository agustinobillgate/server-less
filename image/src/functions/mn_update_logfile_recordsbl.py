from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Htparam, Res_history, Reslin_queasy, Queasy

def mn_update_logfile_recordsbl():
    anz_tage:int = 60
    hist_tage:int = 180
    ci_date:date = None
    htparam = res_history = reslin_queasy = queasy = None

    reshis = r_queasy = qsy = None

    Reshis = Res_history
    R_queasy = Reslin_queasy
    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anz_tage, hist_tage, ci_date, htparam, res_history, reslin_queasy, queasy
        nonlocal reshis, r_queasy, qsy


        nonlocal reshis, r_queasy, qsy
        return {}

    def update_logfile_records():

        nonlocal anz_tage, hist_tage, ci_date, htparam, res_history, reslin_queasy, queasy
        nonlocal reshis, r_queasy, qsy


        nonlocal reshis, r_queasy, qsy

        do_it:bool = False
        Reshis = Res_history
        R_queasy = Reslin_queasy
        Qsy = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 39) &  (Queasy.date1 < (ci_date - anz_tage))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 39) &  (Queasy.date1 < (ci_date - anz_tage))).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 36) &  (Queasy.date1 < (ci_date - anz_tage))).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 36) &  (Queasy.date1 < (ci_date - anz_tage))).first()

        res_history = db_session.query(Res_history).filter(
                (func.lower(Res_history.action) == "HouseKeeping") &  (Res_history.datum < (ci_date - anz_tage)) &  (Res_history.zeit >= 0) &  (Res_history.aenderung.op("~")(".*Status Changed.*"))).first()
        while None != res_history:

            reshis = db_session.query(Reshis).filter(
                        (Reshis._recid == res_history._recid)).first()
            db_session.delete(reshis)

            res_history = db_session.query(Res_history).filter(
                    (func.lower(Res_history.action) == "HouseKeeping") &  (Res_history.datum < (ci_date - anz_tage)) &  (Res_history.zeit >= 0) &  (Res_history.aenderung.op("~")(".*Status Changed.*"))).first()

        res_history = db_session.query(Res_history).filter(
                (func.lower(Res_history.action) == "HouseKeeping") &  (Res_history.datum < (ci_date - hist_tage)) &  (Res_history.zeit >= 0)).first()
        while None != res_history:

            reshis = db_session.query(Reshis).filter(
                        (Reshis._recid == res_history._recid)).first()
            db_session.delete(reshis)

            res_history = db_session.query(Res_history).filter(
                    (func.lower(Res_history.action) == "HouseKeeping") &  (Res_history.datum < (ci_date - anz_tage)) &  (Res_history.zeit >= 0)).first()

        res_history = db_session.query(Res_history).filter(
                (Res_history.datum < (ci_date - hist_tage)) &  (Res_history.zeit >= 0)).first()
        while None != res_history:
            do_it = True

            if res_history.action.lower()  == "G/L" and res_history.datum >= (ci_date - 750):
                do_it = False

            elif res_history.action.lower()  == "reservation" and re.match(".*delete.*",res_history.aenderung) and res_history.datum >= (ci_date - 365):
                do_it = False

            if do_it:

                reshis = db_session.query(Reshis).filter(
                        (Reshis._recid == res_history._recid)).first()
                db_session.delete(reshis)


            res_history = db_session.query(Res_history).filter(
                    (Res_history.datum < (ci_date - hist_tage)) &  (Res_history.zeit >= 0)).first()

        res_history = db_session.query(Res_history).filter(
                (func.lower(Res_history.action) == "G/L") &  (Res_history.datum < (ci_date - anz_tage)) &  (Res_history.zeit >= 0)).first()
        while None != res_history:

            reshis = db_session.query(Reshis).filter(
                        (Reshis._recid == res_history._recid)).first()
            db_session.delete(reshis)

            res_history = db_session.query(Res_history).filter(
                    (func.lower(Res_history.action) == "G/L") &  (Res_history.datum < (ci_date - anz_tage)) &  (Res_history.zeit >= 0)).first()

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "ResChanges") &  (Reslin_queasy.char1 != "")).first()

        if not reslin_queasy:

            return
        while None != reslin_queasy:

            r_queasy = db_session.query(R_queasy).filter(
                        (R_queasy._recid == reslin_queasy._recid)).first()
            r_queasy.char3 = reslin_queasy.char1
            r_queasy.char1 = ""

            r_queasy = db_session.query(R_queasy).first()


            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "ResChanges") &  (Reslin_queasy.char1 != "")).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 371)).first()

    if htparam.paramgruppe == 9 and htparam.finteger != 0:
        anz_tage = htparam.finteger

    if hist_tage < anz_tage:
        hist_tage = anz_tage
    update_logfile_records()

    return generate_output()