#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Bk_veran, Bk_reser

def ns_invoice_check_banquetbl(bill_rechnr:int):

    prepare_cache ([Htparam, Bk_veran])

    answer = True
    htparam = bk_veran = bk_reser = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal answer, htparam, bk_veran, bk_reser
        nonlocal bill_rechnr

        return {"answer": answer}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    bk_veran = get_cache (Bk_veran, {"rechnr": [(eq, bill_rechnr)]})

    if bk_veran and bk_veran.activeflag == 0:

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"datum": [(gt, htparam.fdate)],"resstatus": [(le, 3)]})

        if bk_reser:
            answer = False

            return generate_output()

        bk_reser = db_session.query(Bk_reser).filter(
                 (Bk_reser.veran_nr == bk_veran.veran_nr) & (Bk_reser.datum == htparam.fdate) & (Bk_reser.resstatus == 1) & ((Bk_reser.bis_i * 1800) > get_current_time_in_seconds())).first()

        if bk_reser:
            answer = False

            return generate_output()

    return generate_output()