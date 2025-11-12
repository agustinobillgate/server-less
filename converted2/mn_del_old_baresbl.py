#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.nt_bahistory import nt_bahistory
from models import Htparam, Bk_func, Bk_reser, Bk_veran

def mn_del_old_baresbl():

    prepare_cache ([Htparam])

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

        htparam = get_cache (Htparam, {"paramnr": [(eq, 722)]})
        anz = htparam.finteger

        if anz == 0:
            anz = 60

        for bk_func in db_session.query(Bk_func).filter(
                 (Bk_func.datum <= (ci_date - timedelta(days=anz)))).order_by(Bk_func.veran_nr).all():

            if curr_nr == 0:
                curr_nr = bk_func.veran_nr

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_func.veran_nr)],"veran_resnr": [(eq, bk_func.veran_seite)],"resstatus": [(le, 1)]})

            if bk_reser:
                db_session.delete(bk_reser)

            if curr_nr != bk_func.veran_nr:

                bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, curr_nr)]})

                if bk_veran:

                    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"datum": [(gt, (ci_date - anz))]})

                    if not bk_reser:
                        pass
                        db_session.delete(bk_veran)
                        pass
                        curr_nr = bk_func.veran_nr
                        i = i + 1
            db_session.delete(bk_func)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    get_output(nt_bahistory())
    del_old_bares()

    return generate_output()