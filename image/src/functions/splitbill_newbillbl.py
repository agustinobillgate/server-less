from functions.additional_functions import *
import decimal
from models import Res_line, Bill, Htparam, Guest, Reservation

def splitbill_newbillbl(s_recid:int):
    bil_recid = 0
    reslinnr:int = 1
    rechnr2:int = 0
    billnr:int = 1
    res_line = bill = htparam = guest = reservation = None

    resline = mainbill = None

    Resline = Res_line
    Mainbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bil_recid, reslinnr, rechnr2, billnr, res_line, bill, htparam, guest, reservation
        nonlocal resline, mainbill


        nonlocal resline, mainbill
        return {"bil_recid": bil_recid}


    bill = db_session.query(Bill).filter(
            (Bill._recid == s_recid)).first()

    resline = db_session.query(Resline).filter(
            (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.parent_nr)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 799)).first()

    if htparam.flogical and htparam.feldtyp == 4:

        mainbill = db_session.query(Mainbill).filter(
                (Mainbill.resnr == resline.resnr) &  (Mainbill.reslinnr == resline.reslinnr)).first()

        if mainbill:
            rechnr2 = mainbill.rechnr2

    for res_line in db_session.query(Res_line).filter(
            (Res_line.gastnr == resline.gastnr) &  (Res_line.resnr == resline.resnr)).all():
        reslinnr = res_line.reslinnr + 1
        break
    res_line = Res_line()
    db_session.add(res_line)

    buffer_copy(resline, res_line,except_fields=["resline.reslinnr","resstatus","active_flag","zipreis"])
    res_line.reslinnr = reslinnr
    res_line.resstatus = 12
    res_line.active_flag = 1
    res_line.gastnrpay = resline.gastnrmember

    for bill in db_session.query(Bill).filter(
            (Bill.resnr == resline.resnr) &  (Bill.parent_nr == resline.reslinnr) &  (Bill.flag == 0)).all():
        billnr = billnr + 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill = Bill()
    db_session.add(bill)

    bill.flag = 0
    bill.zinr = res_line.zinr
    bill.gastnr = res_line.gastnrpay
    bill.datum = htparam.fdate
    bill.resnr = res_line.resnr
    bill.reslinnr = res_line.reslinnr
    bill.parent_nr = resline.reslinnr
    billnr = billnr
    bill.rgdruck = 1
    bill.rechnr2 = rechnr2

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == res_line.gastnrpay)).first()
    bill.name = guest.name

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resline.resnr) &  (Reservation.gastnr == resline.gastnr)).first()
    bill.segmentcode = reservation.segmentcode
    bil_recid = bill._recid

    return generate_output()