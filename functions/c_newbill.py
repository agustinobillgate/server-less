from functions.additional_functions import *
import decimal
from models import Res_line, Htparam, Bill, Guest, Reservation

def c_newbill(resl_recid:int, parent_nr:int, billnr:int):
    bil_recid = 0
    reslinnr:int = 1
    its_ok:bool = True
    answer:bool = True
    res_line = htparam = bill = guest = reservation = None

    resline = res_member = None

    Resline = create_buffer("Resline",Res_line)
    Res_member = create_buffer("Res_member",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bil_recid, reslinnr, its_ok, answer, res_line, htparam, bill, guest, reservation
        nonlocal resl_recid, parent_nr, billnr
        nonlocal resline, res_member


        nonlocal resline, res_member

        return {"bil_recid": bil_recid}


    resline = db_session.query(Resline).filter(
             (Resline._recid == resl_recid)).first()

    for res_line in db_session.query(Res_line).filter(
             (Res_line.gastnr == resline.gastnr) & (Res_line.resnr == resline.resnr)).order_by(Res_line._recid).all():

        if reslinnr < res_line.reslinnr:
            reslinnr = res_line.reslinnr
    reslinnr = reslinnr + 1
    res_line = Res_line()
    db_session.add(res_line)

    buffer_copy(resline, res_line,except_fields=["resline.reslinnr","resstatus","active_flag"])
    res_line.reslinnr = reslinnr
    res_line.resstatus = 12
    res_line.active_flag = 1
    res_line.gastnrpay = resline.gastnrmember

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
    bill.parent_nr = parent_nr
    bill.billnr = billnr
    bill.rgdruck = 1

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == res_line.gastnrpay)).first()
    bill.name = guest.name

    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr == resline.resnr) & (Reservation.gastnr == resline.gastnr)).first()
    bill.segmentcode = reservation.segmentcode
    bil_recid = bill._recid

    return generate_output()