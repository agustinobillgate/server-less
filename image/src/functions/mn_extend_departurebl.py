from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Res_line, Bill

def mn_extend_departurebl():
    i = 0
    ci_date:date = None
    htparam = res_line = bill = None

    rline = rline1 = rline2 = None

    Rline = Res_line
    Rline1 = Res_line
    Rline2 = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, res_line, bill
        nonlocal rline, rline1, rline2


        nonlocal rline, rline1, rline2
        return {"i": i}

    def extend_departure():

        nonlocal i, ci_date, htparam, res_line, bill
        nonlocal rline, rline1, rline2


        nonlocal rline, rline1, rline2

        i:int = 0
        Rline = Res_line
        Rline1 = Res_line
        Rline2 = Res_line

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 12)).all():

            rline1 = db_session.query(Rline1).filter(
                    (Rline1.resnr == res_line.resnr) &  (Rline1.zinr == res_line.zinr) &  ((Rline1.resstatus == 6) |  (Rline1.resstatus == 13))).first()

            if not rline1:

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

                if not bill or (bill and bill.saldo == 0):

                    rline2 = db_session.query(Rline2).filter(
                            (Rline2._recid == res_line._recid)).first()
                    rline2.active_flag = 2

                    rline2 = db_session.query(Rline2).first()

                    if bill and bill.flag == 0:

                        bill = db_session.query(Bill).first()
                        bill.flag = 1

                        bill = db_session.query(Bill).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    extend_departure()

    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.abreise < ci_date)).first()
    while None != res_line:
        i = i + 1

        res_line = db_session.query(Res_line).first()
        res_line.abreise = ci_date

        res_line = db_session.query(Res_line).first()


        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.abreise < ci_date)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus == 13)).first()
    while None != res_line:

        rline = db_session.query(Rline).filter(
                (Rline.resnr == res_line.resnr) &  (Rline.reslinnr != res_line.reslinnr) &  (Rline.zinr == res_line.zinr) &  ((Rline.active_flag == 1) |  (Rline.resstatus == 8)) &  (Rline.zimmerfix == False)).first()

        if rline and res_line.zimmerfix == False:

            rline = db_session.query(Rline).filter(
                    (Rline._recid == res_line._recid)).first()
            rline.zimmerfix = True

            rline = db_session.query(Rline).first()

        elif not rline and res_line.zimmerfix :

            rline = db_session.query(Rline).filter(
                    (Rline._recid == res_line._recid)).first()
            rline.zimmerfix = False

            rline = db_session.query(Rline).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 13)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.active_flag == 1) &  (Res_line.resstatus == 6) &  (Res_line.zimmerfix)).first()
    while None != res_line:

        rline = db_session.query(Rline).filter(
                (Rline.resnr == res_line.resnr) &  (Rline.reslinnr != res_line.reslinnr) &  (Rline.zinr == res_line.zinr) &  ((Rline.active_flag == 1) |  (Rline.resstatus == 8)) &  (Rline.zimmerfix == False)).first()

        if not rline:

            rline = db_session.query(Rline).filter(
                    (Rline._recid == res_line._recid)).first()
            rline.zimmerfix = False

            rline = db_session.query(Rline).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 6) &  (Res_line.zimmerfix)).first()

    return generate_output()