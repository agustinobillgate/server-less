#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/10/2025
# timedelta
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from sqlalchemy import func, text
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
        print(f"Logfile records updated: anz_tage={anz_tage}, hist_tage={hist_tage}, ci_date={ci_date}")
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

        # # queasy = get_cache (Queasy, {"key": [(eq, 39)],"date1": [(lt, (ci_date - anz_tage))]})
        # # queasy = db_session.query(Queasy).filter(
        # #          (Queasy.key == 39) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage)))).order_by(Queasy._recid).first()
        # # while queasy is not None:

        # #     qsy = db_session.query(Qsy).filter(
        # #                  (Qsy._recid == queasy._recid)).first()
        # #     db_session.delete(queasy)
        # #     pass

        # #     curr_recid = queasy._recid
        # #     queasy = db_session.query(Queasy).filter(
        # #              (Queasy.key == 39) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage))) & (Queasy._recid > curr_recid)).first()

        # sql = f"DELETE FROM queasy WHERE key = 39 AND date1 < '{(ci_date - timedelta(days=anz_tage)).strftime('%Y-%m-%d')}'"
        # db_session.execute(text(sql))
        # db_session.commit()

        # # queasy = get_cache (Queasy, {"key": [(eq, 36)],"date1": [(lt, (ci_date - anz_tage))]})
        # queasy = db_session.query(Queasy).filter(
        #          (Queasy.key == 36) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage)))).order_by(Queasy._recid).first()
        # while None != queasy:

        #     qsy = db_session.query(Qsy).filter(
        #                  (Qsy._recid == queasy._recid)).first()
        #     db_session.delete(qsy)
        #     pass

        #     curr_recid = queasy._recid
        #     queasy = db_session.query(Queasy).filter(
        #              (Queasy.key == 36) & (Queasy.date1 < (ci_date - timedelta(days=anz_tage))) & (Queasy._recid > curr_recid)).first()

        # res_history = db_session.query(Res_history).filter(
        #          (Res_history.action == ("HouseKeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (matches(Res_history.aenderung,("*Status Changed*")))).first()
        # while None != res_history:

        #     reshis = db_session.query(Reshis).filter(
        #                  (Reshis._recid == res_history._recid)).first()
        #     db_session.delete(reshis)
        #     pass

        #     curr_recid = res_history._recid
        #     res_history = db_session.query(Res_history).filter(
        #              (Res_history.action == ("HouseKeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (matches(Res_history.aenderung,("*Status Changed*"))) & (Res_history._recid > curr_recid)).first()

        # # res_history = get_cache (Res_history, {"action": [(eq, "housekeeping")],"datum": [(lt, (ci_date - hist_tage))],"zeit": [(ge, 0)]})
        # res_history = db_session.query(Res_history).filter(
        #          (Res_history.action == ("Housekeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0)).first()
        # while None != res_history:

        #     reshis = db_session.query(Reshis).filter(
        #                  (Reshis._recid == res_history._recid)).first()
        #     db_session.delete(reshis)
        #     pass

        #     curr_recid = res_history._recid
        #     res_history = db_session.query(Res_history).filter(
        #              (Res_history.action == ("HouseKeeping")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (Res_history._recid > curr_recid)).first()

        # # res_history = get_cache (Res_history, {"datum": [(lt, (ci_date - hist_tage))],"zeit": [(ge, 0)]})
        # res_history = db_session.query(Res_history).filter(
        #          (Res_history.datum < (ci_date - timedelta(days=hist_tage))) & (Res_history.zeit >= 0)).first()
        # while None != res_history:
        #     do_it = True

        #     if res_history.action  == ("G/L")  and res_history.datum >= (ci_date - timedelta(days=750)):
        #         do_it = False

        #     elif res_history.action  == ("reservation")  and matches(res_history.aenderung,r"*delete*") and res_history.datum >= (ci_date - timedelta(days=365)):
        #         do_it = False

        #     if do_it:

        #         reshis = db_session.query(Reshis).filter(
        #                  (Reshis._recid == res_history._recid)).first()
        #         db_session.delete(reshis)
        #         pass

        #     curr_recid = res_history._recid
        #     res_history = db_session.query(Res_history).filter(
        #              (Res_history.datum < (ci_date - timedelta(days=hist_tage))) & (Res_history.zeit >= 0) & (Res_history._recid > curr_recid)).first()

        # # res_history = get_cache (Res_history, {"action": [(eq, "g/l")],"datum": [(lt, (ci_date - anz_tage))],"zeit": [(ge, 0)]})
        # res_history = db_session.query(Res_history).filter(
        #          (Res_history.action == ("G/L")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0)).first()
        # while None != res_history:

        #     reshis = db_session.query(Reshis).filter(
        #                  (Reshis._recid == res_history._recid)).first()
        #     db_session.delete(reshis)
        #     pass

        #     curr_recid = res_history._recid
        #     res_history = db_session.query(Res_history).filter(
        #              (Res_history.action == ("G/L")) & (Res_history.datum < (ci_date - timedelta(days=anz_tage))) & (Res_history.zeit >= 0) & (Res_history._recid > curr_recid)).first()


        # 1️⃣ Hapus Reshis dengan action = 'HouseKeeping' + Status Changed
        sql_delete_housekeeping_status = text("""
            DELETE FROM res_history
            WHERE LOWER(action) = 'housekeeping'
            AND datum < :limit_date
            AND zeit >= 0
            AND STRPOS(LOWER(aenderung COLLATE "C"), 'status changed') > 0
        """)
        db_session.execute(sql_delete_housekeeping_status, {
            "limit_date": ci_date - timedelta(days=anz_tage)
        })


        # 2️⃣ Hapus Res_history dengan action = 'Housekeeping' (semua data lama)
        sql_delete_housekeeping = text("""
            DELETE FROM res_history
            WHERE _recid IN (
                SELECT r._recid
                FROM res_history r
                WHERE LOWER(r.action) = 'housekeeping'
                AND r.datum < :limit_date
                AND r.zeit >= 0
            )
        """)
        db_session.execute(sql_delete_housekeeping, {
            "limit_date": ci_date - timedelta(days=anz_tage)
        })


        # 3️⃣ Hapus Reshis data lama (tanpa filter action, hanya berdasarkan tanggal)
        sql_delete_general = text("""
            DELETE FROM res_history
            WHERE _recid IN (
                SELECT r._recid
                FROM res_history r
                WHERE r.datum < :limit_date
                AND r.zeit >= 0
            )
        """)
        db_session.execute(sql_delete_general, {
            "limit_date": ci_date - timedelta(days=hist_tage)
        })


        # 4️⃣ Hapus Reshis dengan action = 'G/L' (lebih dari anz_tage hari)
        sql_delete_gl = text("""
            DELETE FROM res_history
            WHERE _recid IN (
                SELECT r._recid
                FROM res_history r
                WHERE LOWER(r.action) = 'g/l'
                AND r.datum < :limit_date
                AND r.zeit >= 0
            )
        """)
        db_session.execute(sql_delete_gl, {
            "limit_date": ci_date - timedelta(days=anz_tage)
        })


        # 5️⃣ Hapus Reshis dengan action = 'reservation' + "delete"
        #     hanya untuk data lebih lama dari 1 tahun (365 hari)
        sql_delete_reservation = text("""
                DELETE FROM res_history
                WHERE _recid IN (
                    SELECT r._recid
                    FROM res_history r
                    WHERE LOWER(r.action) = 'reservation'
                    AND STRPOS(LOWER(r.aenderung COLLATE "C"), 'delete') > 0
                    AND r.datum < :limit_date
                    AND r.zeit >= 0
                )
            """)
        db_session.execute(sql_delete_reservation, {
            "limit_date": ci_date - timedelta(days=365)
        })


        # 6️⃣ Hapus Reshis dengan action = 'G/L' tapi hanya jika lebih lama dari 750 hari
        sql_delete_gl_old = text("""
            DELETE FROM res_history
            WHERE _recid IN (
                SELECT r._recid
                FROM res_history r
                WHERE LOWER(r.action) = 'g/l'
                AND r.datum < :limit_date
                AND r.zeit >= 0
            )
        """)
        db_session.execute(sql_delete_gl_old, {
            "limit_date": ci_date - timedelta(days=750)
        })

        # Commit semua perubahan
        db_session.commit()
        
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

    print(f"mn_update_logfile_recordsbl: Starting update with anz_tage={anz_tage}, hist_tage={hist_tage}, ci_date={ci_date}")
    update_logfile_records()

    return generate_output()
