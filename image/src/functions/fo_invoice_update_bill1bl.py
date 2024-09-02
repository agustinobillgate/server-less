from functions.additional_functions import *
import decimal
from datetime import date
from models import Artikel, Bill_line, Htparam, Res_line, Arrangement

def fo_invoice_update_bill1bl(bill_resnr:int, bill_reslinnr:int, billdatum:date):
    skip_it = False
    buff_rechnr = 0
    na_running:bool = False
    artikel = bill_line = htparam = res_line = arrangement = None

    buf_artikel = buf_bill_line = None

    Buf_artikel = Artikel
    Buf_bill_line = Bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal skip_it, buff_rechnr, na_running, artikel, bill_line, htparam, res_line, arrangement
        nonlocal buf_artikel, buf_bill_line


        nonlocal buf_artikel, buf_bill_line
        return {"skip_it": skip_it, "buff_rechnr": buff_rechnr}

    skip_it = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 253)).first()
    na_running = htparam.flogical

    if na_running:

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == bill_resnr) &  (Res_line.reslinnr == bill_reslinnr)).first()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == res_line.arrangement)).first()

    buf_artikel = db_session.query(Buf_artikel).filter(
            (Buf_artikel.artnr == arrangement.argt_artikelnr) &  (Buf_artikel.departement == 0)).first()

    buf_bill_line = db_session.query(Buf_bill_line).filter(
            (Buf_bill_line.departement == 0) &  (Buf_bill_line.artnr == buf_artikel.artnr) &  (Buf_bill_line.bill_datum == billdatum) &  (Buf_bill_line.zinr != "") &  (Buf_bill_line.massnr == res_line.resnr) &  (Buf_bill_line.billin_nr == res_line.reslinnr)).first()
    skip_it = None != buf_bill_line

    if skip_it:
        buff_rechnr = buf_bill_line.rechnr

    return generate_output()