from functions.additional_functions import *
import decimal
from models import Res_line, Bill

def fo_invoice_mi_transferbl(room:str, case_type:int, bil_recid:int, user_init:str):
    resline_resnr = 0
    resline_reslinnr = 0
    run_create_logfile = False
    memormno:str = ""
    res_line = bill = None

    resline = None

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resline_resnr, resline_reslinnr, run_create_logfile, memormno, res_line, bill
        nonlocal resline


        nonlocal resline
        return {"resline_resnr": resline_resnr, "resline_reslinnr": resline_reslinnr, "run_create_logfile": run_create_logfile}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    if case_type == 1:

        resline = db_session.query(Resline).filter(
                (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.reslinnr)).first()
        room = entry(0, resline.memozinr, ";")
    else:

        resline = db_session.query(Resline).filter(
                (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.reslinnr)).first()
        memormno = entry(1, resline.memozinr, ";")

        resline = db_session.query(Resline).first()
        resline.memozinr = room + ";" + memormno + ";"
        resline.memodatum = get_current_date()
        resline.memousercode = user_init

        resline = db_session.query(Resline).first()


        if resline.resstatus != 12:
            run_create_logfile = True
            resline_resnr = resline.resnr
            resline_reslinnr = resline.reslinnr

    return generate_output()