#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from sqlalchemy import func
from models import Htparam, Res_history, Reslin_queasy, Queasy

def mn_update_logfile_recordsbl():

    prepare_cache ([Htparam, Reslin_queasy])

    anz_tage:int = 60
    hist_tage:int = 180
    ci_date:date = None
    htparam = res_history = reslin_queasy = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anz_tage, hist_tage, ci_date, htparam, res_history, reslin_queasy, queasy

        return {}

    def update_logfile_records():

        nonlocal anz_tage, hist_tage, ci_date, htparam, res_history, reslin_queasy, queasy

        do_it:bool = False
        reshis = None
        r_queasy = None
        qsy = None
        Reshis =  create_buffer("Reshis",Res_history)
        R_queasy =  create_buffer("R_queasy",Reslin_queasy)
        Qsy =  create_buffer("Qsy",Queasy)

        # queasy = get_cache (Queasy, {"key": [(eq, 39)],"date1": [(lt, (ci_date - anz_tage))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 39) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 39) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage))) & (Queasy._recid > curr_recid)).first()

        # queasy = get_cache (Queasy, {"key": [(eq, 36)],"date1": [(lt, (ci_date - anz_tage))]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 36) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage)))).order_by(Queasy._recid).first()
        while None != queasy:

            qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).first()
            db_session.delete(qsy)
            pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 36) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage))) & (Queasy._recid > curr_recid)).first()

        res_history = db_session.query(Res_history).filter(
                 (Res_history.action == ("HouseKeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (matches(Res_history.aenderung,("*Status Changed*")))).first()
        while None != res_history:

            reshis = db_session.query(Reshis).filter(
                         (Reshis._recid == res_history._recid)).first()
            db_session.delete(reshis)
            pass

            curr_recid = res_history._recid
            res_history = db_session.query(Res_history).filter(
                     (Res_history.action == ("HouseKeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (matches(Res_history.aenderung,("*Status Changed*"))) & (Res_history._recid > curr_recid)).first()

        # res_history = get_cache (Res_history, {"action": [(eq, "housekeeping")],"datum": [(lt, (ci_date - hist_tage))],"zeit": [(ge, 0)]})
        res_history = db_session.query(Res_history).filter(
                 (Res_history.action == ("Housekeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0)).first()
        while None != res_history:

            reshis = db_session.query(Reshis).filter(
                         (Reshis._recid == res_history._recid)).first()
            db_session.delete(reshis)
            pass

            curr_recid = res_history._recid
            res_history = db_session.query(Res_history).filter(
                     (Res_history.action == ("HouseKeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (Res_history._recid > curr_recid)).first()

        res_history = get_cache (Res_history, {"datum": [(lt, (ci_date - hist_tage))],"zeit": [(ge, 0)]})
        while None != res_history:
            do_it = True

            if res_history.action  == ("G/L")  and res_history.datum >= (ci_date - timedelta(days=750)):
                do_it = False

            elif res_history.action  == ("reservation")  and matches(res_history.aenderung,r"*delete*") and res_history.datum >= (ci_date - timedelta(days=365)):
                do_it = False

            if do_it:

                reshis = db_session.query(Reshis).filter(
                         (Reshis._recid == res_history._recid)).first()
                db_session.delete(reshis)
                pass

            curr_recid = res_history._recid
            res_history = db_session.query(Res_history).filter(
                     (Res_history.datum < (ci_date - timedelta(days=hist_tage))) & (Res_history.zeit >= 0) & (Res_history._recid > curr_recid)).first()

        # res_history = get_cache (Res_history, {"action": [(eq, "g/l")],"datum": [(lt, (ci_date - anz_tage))],"zeit": [(ge, 0)]})
        res_history = db_session.query(Res_history).filter(
                 (Res_history.action == ("G/L")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0)).first()
        while None != res_history:

            reshis = db_session.query(Reshis).filter(
                         (Reshis._recid == res_history._recid)).first()
            db_session.delete(reshis)
            pass

            curr_recid = res_history._recid
            res_history = db_session.query(Res_history).filter(
                     (Res_history.action == ("G/L")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (Res_history._recid > curr_recid)).first()

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "reschanges")],"char1": [(ne, "")]})

        if not reslin_queasy:

            return
        while None != reslin_queasy:

            r_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, reslin_queasy._recid)]})
            r_queasy.char3 = reslin_queasy.char1
            r_queasy.char1 = ""
            pass

            curr_recid = reslin_queasy._recid
            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("ResChanges")) & (Reslin_queasy.char1 != "") & (Reslin_queasy._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 371)]})

    if htparam.paramgruppe == 9 and htparam.finteger != 0:
        anz_tage = htparam.finteger

    if hist_tage < anz_tage:
        hist_tage = anz_tage
    update_logfile_records()

    return generate_output()