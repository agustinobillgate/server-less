#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Res_line, Master

def fo_invoice_btn_mviewbl(bil_recid:int):

    prepare_cache ([Bill, Res_line, Master])

    mbill_resnr = 0
    mbill_rechnr = 0
    avail_mbill = False
    bill = res_line = master = None

    resline = mbill = None

    Resline = create_buffer("Resline",Res_line)
    Mbill = create_buffer("Mbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mbill_resnr, mbill_rechnr, avail_mbill, bill, res_line, master
        nonlocal bil_recid
        nonlocal resline, mbill


        nonlocal resline, mbill

        return {"mbill_resnr": mbill_resnr, "mbill_rechnr": mbill_rechnr, "avail_mbill": avail_mbill}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if bill:

        resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

        if resline.l_zuordnung[4] != 0:

            mbill = get_cache (Bill, {"resnr": [(eq, resline.l_zuordnung[4])],"reslinnr": [(eq, 0)]})

            if mbill:
                avail_mbill = True
                mbill_resnr = mbill.resnr
                mbill_rechnr = mbill.rechnr
        else:

            master = get_cache (Master, {"resnr": [(eq, bill.resnr)]})

            if master:

                mbill = get_cache (Bill, {"resnr": [(eq, master.resnr)],"reslinnr": [(eq, 0)]})

                if mbill:
                    avail_mbill = True
                    mbill_resnr = mbill.resnr
                    mbill_rechnr = mbill.rechnr
    else:

        return generate_output()

    return generate_output()