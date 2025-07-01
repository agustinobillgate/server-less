#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill, Htparam, Guest, Reservation

def splitbill_newbillbl(s_recid:int):

    prepare_cache ([Bill, Htparam, Guest, Reservation])

    bil_recid = 0
    reslinnr:int = 1
    rechnr2:int = 0
    billnr:int = 1
    res_line = bill = htparam = guest = reservation = None

    resline = mainbill = None

    Resline = create_buffer("Resline",Res_line)
    Mainbill = create_buffer("Mainbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bil_recid, reslinnr, rechnr2, billnr, res_line, bill, htparam, guest, reservation
        nonlocal s_recid
        nonlocal resline, mainbill


        nonlocal resline, mainbill

        return {"bil_recid": bil_recid}


    bill = get_cache (Bill, {"_recid": [(eq, s_recid)]})

    resline = db_session.query(Resline).filter(
             (Resline.resnr == bill.resnr) & (Resline.reslinnr == bill.parent_nr)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 799)]})

    if htparam.flogical and htparam.feldtyp == 4:

        mainbill = get_cache (Bill, {"resnr": [(eq, resline.resnr)],"reslinnr": [(eq, resline.reslinnr)]})

        if mainbill:
            rechnr2 = mainbill.rechnr2

    for res_line in db_session.query(Res_line).filter(
             (Res_line.gastnr == resline.gastnr) & (Res_line.resnr == resline.resnr)).order_by(Res_line.reslinnr.desc()).yield_per(100):
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
             (Bill.resnr == resline.resnr) & (Bill.parent_nr == resline.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
        billnr = billnr + 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill = Bill()
    db_session.add(bill)

    bill.flag = 0
    bill.zinr = res_line.zinr
    bill.gastnr = res_line.gastnrpay
    bill.datum = htparam.fdate
    bill.resnr = res_line.resnr
    bill.reslinnr = res_line.reslinnr
    bill.parent_nr = resline.reslinnr
    bill.billnr = billnr
    bill.rgdruck = 1
    bill.rechnr2 = rechnr2

    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
    bill.name = guest.name

    reservation = get_cache (Reservation, {"resnr": [(eq, resline.resnr)],"gastnr": [(eq, resline.gastnr)]})
    bill.segmentcode = reservation.segmentcode
    bil_recid = bill._recid

    return generate_output()