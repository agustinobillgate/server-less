#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill, Htparam, Guest, Reservation

def create_newbillbl(resno:int, reslinno:int, parent_nr:int, billnr:int):

    prepare_cache ([Bill, Htparam, Guest, Reservation])

    bil_recid = 0
    reslinnr:int = 1
    its_ok:bool = True
    answer:bool = True
    rechnr2:int = 0
    res_line = bill = htparam = guest = reservation = None

    res_member = resline = mainbill = None

    Res_member = create_buffer("Res_member",Res_line)
    Resline = create_buffer("Resline",Res_line)
    Mainbill = create_buffer("Mainbill",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bil_recid, reslinnr, its_ok, answer, rechnr2, res_line, bill, htparam, guest, reservation
        nonlocal resno, reslinno, parent_nr, billnr
        nonlocal res_member, resline, mainbill


        nonlocal res_member, resline, mainbill

        return {"bil_recid": bil_recid}


    resline = db_session.query(Resline).filter(
             (Resline.resnr == resno) & (Resline.reslinnr == parent_nr)).first()

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
    res_line.gastnrpay = resline.gastnrpay

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill = Bill()
    db_session.add(bill)

    bill.flag = 0
    bill.zinr = res_line.zinr
    bill.gastnr = res_line.gastnrpay
    bill.datum = htparam.fdate
    bill.resnr = res_line.resnr
    bill.reslinnr = res_line.reslinnr
    bill.parent_nr = parent_nr
    bill.billnr = billnr
    bill.rgdruck = 1
    bill.rechnr2 = rechnr2

    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
    bill.name = guest.name

    reservation = get_cache (Reservation, {"resnr": [(eq, resline.resnr)],"gastnr": [(eq, resline.gastnr)]})
    bill.segmentcode = reservation.segmentcode
    bil_recid = bill._recid

    return generate_output()