from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Bill, Reservation, Res_line, Debitor, Guest, Htparam

def update_gcfname(gastnr:int):
    bill = reservation = res_line = debitor = guest = htparam = None

    bbill = rsev = rline = bdebt = None

    Bbill = Bill
    Rsev = Reservation
    Rline = Res_line
    Bdebt = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill, reservation, res_line, debitor, guest, htparam
        nonlocal bbill, rsev, rline, bdebt


        nonlocal bbill, rsev, rline, bdebt
        return {}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    bill = db_session.query(Bill).filter(
            (Bill.gastnr == gastnr)).first()
    while None != bill:

        bbill = db_session.query(Bbill).filter(
                    (Bbill._recid == bill._recid)).first()
        bbill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1

        bbill = db_session.query(Bbill).first()

        bill = db_session.query(Bill).filter(
                (Bill.gastnr == gastnr)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.gastnr == gastnr) &  (Reservation.activeflag == 0)).first()
    while None != reservation:

        rsev = db_session.query(Rsev).filter(
                    (Rsev._recid == reservation._recid)).first()
        rsev.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1

        rsev = db_session.query(Rsev).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.gastnr == gastnr) &  (Reservation.activeflag == 0)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.gastnrmember == gastnr) &  (Res_line.active_flag <= 1)).first()
    while None != res_line:

        rline = db_session.query(Rline).filter(
                    (Rline._recid == res_line._recid)).first()
        rline.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1

        rline = db_session.query(Rline).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 307)).first()

        if htparam.flogical:

            if res_line.active_flag == 1:
                get_output(intevent_1(1, res_line.zinr, "Change Guestname!", res_line.resnr, res_line.reslinnr))

        res_line = db_session.query(Res_line).filter(
                (Res_line.gastnrmember == gastnr) &  (Res_line.active_flag <= 1)).first()

    debitor = db_session.query(Debitor).filter(
            (Debitor.opart <= 1) &  (Debitor.gastnr == gastnr)).first()
    while None != debitor:

        bdebt = db_session.query(Bdebt).filter(
                    (Bdebt._recid == debitor._recid)).first()
        bdebt.name = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1

        bdebt = db_session.query(Bdebt).first()

        debitor = db_session.query(Debitor).filter(
                (Debitor.opart <= 1) &  (Debitor.gastnr == gastnr)).first()

    return generate_output()