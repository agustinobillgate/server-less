#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill, Master

def fo_invoice_btn_masbillbl(case_type:int, bill_resnr:int, bill_reslinnr:int):

    prepare_cache ([Res_line, Bill, Master])

    master_str = ""
    master_rechnr = ""
    mbill_resnr = 0
    mbill_rechnr = 0
    mbill_gastnr = 0
    mbill_segmentcode = 0
    task = 0
    res_line = bill = master = None

    resline = mbill = None

    Resline = create_buffer("Resline",Res_line)
    Mbill = create_buffer("Mbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal master_str, master_rechnr, mbill_resnr, mbill_rechnr, mbill_gastnr, mbill_segmentcode, task, res_line, bill, master
        nonlocal case_type, bill_resnr, bill_reslinnr
        nonlocal resline, mbill


        nonlocal resline, mbill

        return {"master_str": master_str, "master_rechnr": master_rechnr, "mbill_resnr": mbill_resnr, "mbill_rechnr": mbill_rechnr, "mbill_gastnr": mbill_gastnr, "mbill_segmentcode": mbill_segmentcode, "task": task}


    if case_type == 1:

        resline = get_cache (Res_line, {"resnr": [(eq, bill_resnr)],"reslinnr": [(eq, bill_reslinnr)]})

        if resline:

            if resline.l_zuordnung[4] != 0:

                mbill = get_cache (Bill, {"resnr": [(eq, resline.l_zuordnung[4])],"reslinnr": [(eq, 0)]})

                if mbill:
                    task = 1
                    mbill_resnr = mbill.resnr
                    mbill_gastnr = mbill.gastnr
                    mbill_segmentcode = mbill.segmentcode
                    mbill_rechnr = mbill.rechnr


                else:
                    task = 2
            else:
                task = 3

    elif case_type == 2:

        master = get_cache (Master, {"resnr": [(eq, bill_resnr)]})

        if master:

            mbill = get_cache (Bill, {"resnr": [(eq, bill_resnr)],"rechnr": [(eq, master.rechnr),(ne, 0)],"reslinnr": [(eq, 0)],"zinr": [(eq, "")]})

            if not mbill:

                mbill = get_cache (Bill, {"resnr": [(eq, bill_resnr)],"reslinnr": [(eq, 0)],"zinr": [(eq, "")]})
        else:

            mbill = get_cache (Bill, {"resnr": [(eq, bill_resnr)],"reslinnr": [(eq, 0)],"zinr": [(eq, "")]})

        if mbill:
            master_str = "Master Bill"
            master_rechnr = to_string(mbill.rechnr) + " - " + mbill.name
        else:
            master_str = ""
            master_rechnr = ""

    return generate_output()