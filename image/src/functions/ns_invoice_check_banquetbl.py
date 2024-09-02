from functions.additional_functions import *
import decimal
from functions.ba_npartikel import ba_npartikel
from models import Htparam, Bk_veran, Bk_reser, Bk_rart

def ns_invoice_check_banquetbl(bill_rechnr:int):
    answer = False
    htparam = bk_veran = bk_reser = bk_rart = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal answer, htparam, bk_veran, bk_reser, bk_rart


        return {"answer": answer}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.rechnr == bill_rechnr)).first()

    if bk_veran and bk_veran.activeflag == 0:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.datum > htparam.fdate) &  (Bk_reser.resstatus <= 3)).first()

        if bk_reser:
            answer = False

            return generate_output()

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == bk_veran.veran_nr) &  (Bk_reser.datum == htparam.fdate) &  (Bk_reser.resstatus == 1) &  ((Bk_reser.bis_i * 1800) > get_current_time_in_seconds())).first()

        if bk_reser:
            answer = False

            return generate_output()

        bk_rart = db_session.query(Bk_rart).filter(
                (Bk_rart.veran_nr == bk_veran.veran_nr) &  (Bk_rart.preis > 0) &  (Bk_rart.anzahl != 0) &  (Bk_rart.fakturiert == 0)).first()

        if bk_rart:
            get_output(ba_npartikel(bk_veran.veran_nr))

    return generate_output()