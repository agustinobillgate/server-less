#using conversion tools version: 1.0.0.117
# =======================================
# Rd, 21/10/2025
# timedelta
# =======================================

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timedelta
from models import Htparam, H_journal, H_queasy, Guest_queasy

def mn_del_old_rjournalbl():

    prepare_cache ([Htparam])

    i = 0
    j = 0
    ci_date:date = None
    htparam = h_journal = h_queasy = guest_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, ci_date, htparam, h_journal, h_queasy, guest_queasy

        return {"i": i, "j": j}

    def del_old_rjournal():

        nonlocal i, j, ci_date, htparam, h_journal, h_queasy, guest_queasy

        anz:int = 0
        jbuff = None
        qbuff = None
        Jbuff =  create_buffer("Jbuff",H_journal)
        Qbuff =  create_buffer("Qbuff",H_queasy)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 165)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        # h_journal = get_cache (H_journal, {"bill_datum": [(le, (ci_date - anz))]})
        h_journal = db_session.query(H_journal).filter(
                     (H_journal.bill_datum <= (ci_date - timedelta(days=anz)))).first()
        while None != h_journal:

            guest_queasy = get_cache (Guest_queasy, {"betriebsnr": [(eq, 0)],"key": [(eq, "gast-info")],"char1": [(eq, to_string(h_journal.rechnr))],"number1": [(eq, h_journal.departement)],"date1": [(eq, h_journal.bill_datum)]})

            if not guest_queasy:
                i = i + 1

                jbuff = db_session.query(Jbuff).filter(
                         (Jbuff._recid == h_journal._recid)).with_for_update().first()
                db_session.delete(jbuff)
                pass

            curr_recid = h_journal._recid
            h_journal = db_session.query(H_journal).filter(
                     (H_journal.bill_datum <= (ci_date - timedelta(days=anz))) & (H_journal._recid > curr_recid)).first()
        j = 0

        h_queasy = get_cache (H_queasy, {"datum": [(le, (ci_date - timedelta(days=2)))]})
        while None != h_queasy:
            j = j + 1

            qbuff = db_session.query(Qbuff).filter(
                         (Qbuff._recid == h_queasy._recid)).with_for_update().first()
            db_session.delete(qbuff)
            pass

            curr_recid = h_queasy._recid
            h_queasy = db_session.query(H_queasy).filter(
                     (H_queasy.datum <= (ci_date - timedelta(days=2))) & (H_queasy._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_rjournal()

    return generate_output()