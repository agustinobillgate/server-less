from functions.additional_functions import *
import decimal
from models import Bill, Res_line, Master

def fo_invoice_btn_mviewbl(bil_recid:int):
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


    bill = db_session.query(Bill).filter(
             (Bill._recid == bil_recid)).first()

    resline = db_session.query(Resline).filter(
             (Resline.resnr == bill.resnr) & (Resline.reslinnr == bill.reslinnr)).first()

    if resline.l_zuordnung[4] != 0:

        mbill = db_session.query(Mbill).filter(
                 (Mbill.resnr == resline.l_zuordnung[4]) & (Mbill.reslinnr == 0)).first()

        if mbill:
            avail_mbill = True
            mbill_resnr = mbill.resnr
            mbill_rechnr = mbill.rechnr
    else:

        master = db_session.query(Master).filter(
                 (Master.resnr == bill.resnr)).first()

        if master:

            mbill = db_session.query(Mbill).filter(
                     (Mbill.resnr == master.resnr) & (Mbill.reslinnr == 0)).first()

            if mbill:
                avail_mbill = True
                mbill_resnr = mbill.resnr
                mbill_rechnr = mbill.rechnr

    return generate_output()