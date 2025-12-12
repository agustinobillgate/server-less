#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Htparam, Bill, Zimmer, Zimplan

def release_zinrbl(res_mode:string, resno:int, reslinno:int, new_zinr:string):

    prepare_cache ([Res_line, Htparam, Bill, Zimmer])

    res_line = htparam = bill = zimmer = zimplan = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, htparam, bill, zimmer, zimplan
        nonlocal res_mode, resno, reslinno, new_zinr

        return {}

    def release_zinr():

        nonlocal res_line, htparam, bill, zimmer, zimplan
        nonlocal res_mode, resno, reslinno, new_zinr

        res_recid1:int = 0
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        rline = None
        res_line1 = None
        res_line2 = None
        Rline =  create_buffer("Rline",Res_line)
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 87)).first()

        # rline = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})
        rline = db_session.query(Res_line).filter(
                 (Res_line.resnr == resno) & (Res_line.reslinnr == reslinno)).with_for_update().first()

        if rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == ("delete").lower()  or res_mode.lower()  == ("cancel").lower()  and rline.resstatus == 1:

                # res_line1 = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 11)]})
                res_line1 = db_session.query(Res_line).filter(
                         (Res_line.resnr == resno) & (Res_line.zinr == rline.zinr) & (Res_line.resstatus == 11)).with_for_update().first()

                if res_line1:
                    db_session.refresh(res_line1, with_for_update=True)
                    res_line1.resstatus = 1
                    db_session.flush()
                    res_recid1 = res_line1._recid

            if res_mode.lower()  == ("inhouse").lower() :
                answer = True
                beg_datum = htparam.fdate

                if rline.resstatus == 6 and (rline.zinr.lower()  != (new_zinr).lower()):

                    # res_line1 = get_cache (Res_line, {"resnr": [(eq, resno)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 13)]})
                    res_line1 = db_session.query(Res_line).filter(
                             (Res_line.resnr == resno) & (Res_line.zinr == rline.zinr) & (Res_line.resstatus == 13)).first()
                    if res_line1:

                        for res_line2 in db_session.query(Res_line2).filter(
                                 (Res_line2.resnr == resno) & (Res_line2.zinr == rline.zinr) & (Res_line2.resstatus == 13)).order_by(Res_line2._recid).with_for_update().all():

                            # bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, res_line2.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line2.zinr)]})
                            bill = db_session.query(Bill).filter(
                                     (Bill.resnr == resno) & (Bill.reslinnr == res_line2.reslinnr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).with_for_update().first()
                            bill.zinr = new_zinr
                            parent_nr = bill.parent_nr
                            pass

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == resno) & (Bill.parent_nr == parent_nr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).order_by(Bill._recid).all():
                                bill.zinr = new_zinr
                                pass
                            res_line2.zinr = new_zinr
                            pass

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})
                        zimmer.zistatus = 2
                        pass

            for zimplan in db_session.query(Zimplan).filter(
                         (Zimplan.zinr == rline.zinr) & (Zimplan.datum >= beg_datum) & (Zimplan.datum < rline.abreise)).order_by(Zimplan._recid).with_for_update().all():

                if res_recid1 != 0:
                    zimplan.res_recid = res_recid1
                else:
                    db_session.delete(zimplan)

    release_zinr()

    return generate_output()