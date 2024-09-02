from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, H_journal, H_queasy, Guest_queasy

def mn_del_old_rjournalbl():
    i = 0
    j = 0
    ci_date:date = None
    htparam = h_journal = h_queasy = guest_queasy = None

    jbuff = qbuff = None

    Jbuff = H_journal
    Qbuff = H_queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, ci_date, htparam, h_journal, h_queasy, guest_queasy
        nonlocal jbuff, qbuff


        nonlocal jbuff, qbuff
        return {"i": i, "j": j}

    def del_old_rjournal():

        nonlocal i, j, ci_date, htparam, h_journal, h_queasy, guest_queasy
        nonlocal jbuff, qbuff


        nonlocal jbuff, qbuff

        anz:int = 0
        Jbuff = H_journal
        Qbuff = H_queasy

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 165)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        h_journal = db_session.query(H_journal).filter(
                (H_journal.bill_datum <= (ci_date - anz))).first()
        while None != h_journal:

            guest_queasy = db_session.query(Guest_queasy).filter(
                    (Guest_queasy.betriebsnr == 0) &  (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.char1 == to_string(h_journal.rechnr)) &  (Guest_queasy.number1 == h_journal.departement) &  (Guest_queasy.date1 == h_journal.bill_datum)).first()

            if not guest_queasy:
                i = i + 1

                jbuff = db_session.query(Jbuff).filter(
                        (Jbuff._recid == h_journal._recid)).first()
                db_session.delete(jbuff)


            h_journal = db_session.query(H_journal).filter(
                    (H_journal.bill_datum <= (ci_date - anz))).first()
        j = 0

        h_queasy = db_session.query(H_queasy).filter(
                (H_queasy.datum <= (ci_date - 2))).first()
        while None != h_queasy:
            j = j + 1

            qbuff = db_session.query(Qbuff).filter(
                        (Qbuff._recid == h_queasy._recid)).first()
            db_session.delete(qbuff)

            h_queasy = db_session.query(H_queasy).filter(
                    (H_queasy.datum <= (ci_date - 2))).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_rjournal()

    return generate_output()