#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Bill

def mn_extend_departurebl():

    prepare_cache ([Htparam, Res_line, Bill])

    i = 0
    ci_date:date = None
    htparam = res_line = bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, res_line, bill

        return {"i": i}

    def extend_departure():

        nonlocal ci_date, htparam, res_line, bill

        i:int = 0
        rline = None
        rline1 = None
        rline2 = None
        Rline =  create_buffer("Rline",Res_line)
        Rline1 =  create_buffer("Rline1",Res_line)
        Rline2 =  create_buffer("Rline2",Res_line)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus == 12)).order_by(Res_line._recid).all():

            rline1 = db_session.query(Rline1).filter(
                     (Rline1.resnr == res_line.resnr) & (Rline1.zinr == res_line.zinr) & ((Rline1.resstatus == 6) | (Rline1.resstatus == 13))).first()

            if not rline1:

                bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if not bill or (bill and bill.saldo == 0):

                    rline2 = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                    rline2.active_flag = 2


                    pass

                    if bill and bill.flag == 0:
                        pass
                        bill.flag = 1


                        pass

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"abreise": [(lt, ci_date)]})
        while None != res_line:
            i = i + 1
            pass
            res_line.abreise = ci_date
            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.abreise < ci_date) & (Res_line._recid > curr_recid)).first()

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 13)]})
        while None != res_line:

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == res_line.resnr) & (Rline.reslinnr != res_line.reslinnr) & (Rline.zinr == res_line.zinr) & ((Rline.active_flag == 1) | (Rline.resstatus == 8)) & (Rline.zimmerfix == False)).first()

            if rline and res_line.zimmerfix == False:

                rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                rline.zimmerfix = True


                pass

            elif not rline and res_line.zimmerfix :

                rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                rline.zimmerfix = False


                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus == 13) & (Res_line._recid > curr_recid)).first()

        res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"resstatus": [(eq, 6)],"zimmerfix": [(eq, True)]})
        while None != res_line:

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == res_line.resnr) & (Rline.reslinnr != res_line.reslinnr) & (Rline.zinr == res_line.zinr) & ((Rline.active_flag == 1) | (Rline.resstatus == 8)) & (Rline.zimmerfix == False)).first()

            if not rline:

                rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                rline.zimmerfix = False


                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.resstatus == 6) & (Res_line.zimmerfix) & (Res_line._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    extend_departure()

    return generate_output()