#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Bill_line, Htparam, Res_line, Arrangement

def fo_invoice_update_bill1bl(bill_resnr:int, bill_reslinnr:int, billdatum:date):

    prepare_cache ([Artikel, Htparam, Res_line, Arrangement])

    skip_it = False
    buff_rechnr = -1
    na_running:bool = False
    artikel = bill_line = htparam = res_line = arrangement = None

    buf_artikel = buf_bill_line = None

    Buf_artikel = create_buffer("Buf_artikel",Artikel)
    Buf_bill_line = create_buffer("Buf_bill_line",Bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal skip_it, buff_rechnr, na_running, artikel, bill_line, htparam, res_line, arrangement
        nonlocal bill_resnr, bill_reslinnr, billdatum
        nonlocal buf_artikel, buf_bill_line


        nonlocal buf_artikel, buf_bill_line

        return {"skip_it": skip_it, "buff_rechnr": buff_rechnr}

    skip_it = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 253)]})
    na_running = htparam.flogical

    if na_running:

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, bill_resnr)],"reslinnr": [(eq, bill_reslinnr)]})

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    buf_artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

    buf_bill_line = db_session.query(Buf_bill_line).filter(
             (Buf_bill_line.departement == 0) & (Buf_bill_line.artnr == buf_artikel.artnr) & (Buf_bill_line.bill_datum == billdatum) & (Buf_bill_line.zinr != "") & (Buf_bill_line.massnr == res_line.resnr) & (Buf_bill_line.billin_nr == res_line.reslinnr)).first()
    skip_it = None != buf_bill_line

    if skip_it:
        buff_rechnr = buf_bill_line.rechnr

    return generate_output()