from functions.additional_functions import *
import decimal
from models import Res_line, Bill

def fo_invoice_btn_masbillbl(case_type:int, bill_resnr:int, bill_reslinnr:int):
    master_str = ""
    master_rechnr = ""
    mbill_resnr = 0
    mbill_rechnr = 0
    mbill_gastnr = 0
    mbill_segmentcode = 0
    task = 0
    res_line = bill = None

    resline = mbill = None

    Resline = Res_line
    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal master_str, master_rechnr, mbill_resnr, mbill_rechnr, mbill_gastnr, mbill_segmentcode, task, res_line, bill
        nonlocal resline, mbill


        nonlocal resline, mbill
        return {"master_str": master_str, "master_rechnr": master_rechnr, "mbill_resnr": mbill_resnr, "mbill_rechnr": mbill_rechnr, "mbill_gastnr": mbill_gastnr, "mbill_segmentcode": mbill_segmentcode, "task": task}


    if case_type == 1:

        resline = db_session.query(Resline).filter(
                (Resline.resnr == bill_resnr) &  (Resline.reslinnr == bill_reslinnr)).first()

        if resline.l_zuordnung[4] != 0:

            mbill = db_session.query(Mbill).filter(
                    (Mbill.resnr == resline.l_zuordnung[4]) &  (Mbill.reslinnr == 0)).first()

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

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == bill_resnr) &  (Mbill.reslinnr == 0) &  (Mbill.zinr == "")).first()

        if mbill:
            master_str = "Master Bill"
            master_rechnr = to_string(mbill.rechnr) + " - " + mbill.name
        else:
            master_str = ""
            master_rechnr = ""

    return generate_output()