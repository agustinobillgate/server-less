from functions.additional_functions import *
import decimal
from datetime import date
from functions.nt_bahistory import nt_bahistory
from models import Htparam, Bk_func, Bk_reser, Bk_veran

def mn_del_old_baresbl():
    i = 0
    ci_date:date = None
    htparam = bk_func = bk_reser = bk_veran = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, bk_func, bk_reser, bk_veran


        return {"i": i}

    def del_old_bares():

        nonlocal i, ci_date, htparam, bk_func, bk_reser, bk_veran

        anz:int = 0
        curr_nr:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 722)).first()
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        for bk_func in db_session.query(Bk_func).filter(
                (Bk_func.datum <= (ci_date - anz))).all():

            if curr_nr == 0:
                curr_nr = bk_func.veran_nr

            bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == bk_func.veran_nr) &  (Bk_reser.veran_resnr == bk_func.veran_seite) &  (Bk_reser.resstatus <= 1)).first()

            if bk_reser:
                db_session.delete(bk_reser)

            if curr_nr != bk_func.veran_nr:

                bk_veran = db_session.query(Bk_veran).filter(
                        (Bk_veran.veran_nr == curr_nr)).first()

                if bk_veran:

                    bk_reser = db_session.query(Bk_reser).filter(
                            (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.datum > (ci_date - anz))).first()

                    if not bk_reser:

                        bk_veran = db_session.query(Bk_veran).first()
                        db_session.delete(bk_veran)

                        curr_nr = bk_func.veran_nr
                        i = i + 1
            db_session.delete(bk_func)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    get_output(nt_bahistory())
    del_old_bares()

    return generate_output()