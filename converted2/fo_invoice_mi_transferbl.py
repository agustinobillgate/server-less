#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill

def fo_invoice_mi_transferbl(room:string, case_type:int, bil_recid:int, user_init:string):

    prepare_cache ([Res_line, Bill])

    resline_resnr = 0
    resline_reslinnr = 0
    run_create_logfile = False
    memormno:string = ""
    res_line = bill = None

    resline = None

    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resline_resnr, resline_reslinnr, run_create_logfile, memormno, res_line, bill
        nonlocal room, case_type, bil_recid, user_init
        nonlocal resline


        nonlocal resline

        return {"room": room, "resline_resnr": resline_resnr, "resline_reslinnr": resline_reslinnr, "run_create_logfile": run_create_logfile}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if not bill:

        return generate_output()

    if case_type == 1:

        resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
        room = entry(0, resline.memozinr, ";")
    else:

        resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})
        pass

        if resline.memozinr == None:
            resline.memozinr = ";;"
        pass

        if room == None:
            room = ""
        memormno = entry(1, resline.memozinr, ";")

        if memormno == None:
            memormno = ""
        pass
        resline.memozinr = room + ";" + memormno + ";"
        resline.memodatum = get_current_date()
        resline.memousercode = user_init


        pass

        if resline.resstatus != 12:
            run_create_logfile = True
            resline_resnr = resline.resnr
            resline_reslinnr = resline.reslinnr

    return generate_output()