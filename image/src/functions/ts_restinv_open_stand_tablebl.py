from functions.additional_functions import *
import decimal
from models import Tisch, H_bill

def ts_restinv_open_stand_tablebl(curr_dept:int, curr_waiter:int):
    tischno = 0
    openbill_found = False
    fl_code = 0
    tisch = h_bill = None

    tbuff = tbuff1 = hbuff = None

    Tbuff = Tisch
    Tbuff1 = Tisch
    Hbuff = H_bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tischno, openbill_found, fl_code, tisch, h_bill
        nonlocal tbuff, tbuff1, hbuff


        nonlocal tbuff, tbuff1, hbuff
        return {"tischno": tischno, "openbill_found": openbill_found, "fl_code": fl_code}


    tbuff = db_session.query(Tbuff).filter(
            (Tbuff.departement == curr_dept) &  (Tbuff.roomcharge)).first()

    if not tbuff:
        fl_code = 1

        return generate_output()

    tbuff = db_session.query(Tbuff).filter(
            (Tbuff.departement == curr_dept) &  (Tbuff.roomcharge) &  (Tbuff.kellner_nr == curr_waiter)).first()

    if tbuff:
        tischno = tbuff.tischnr

        hbuff = db_session.query(Hbuff).filter(
                (Hbuff.departement == curr_dept) &  (Hbuff.tischnr == tbuff.tischnr) &  (Hbuff.flag == 0)).first()

        if hbuff and hbuff.saldo != 0:
            openbill_found = True
    else:

        for tbuff in db_session.query(Tbuff).filter(
                (Tbuff.departement == curr_dept) &  (Tbuff.roomcharge) &  (Tbuff.kellner_nr == 0)).all():

            hbuff = db_session.query(Hbuff).filter(
                    (Hbuff.departement == curr_dept) &  (Hbuff.tischnr == tbuff.tischnr) &  (Hbuff.flag == 0)).first()

            if not hbuff:
                tischno = tbuff.tischnr

                tbuff1 = db_session.query(Tbuff1).filter(
                        (Tbuff1._recid == tbuff._recid)).first()
                tbuff1.kellner_nr = curr_waiter

                tbuff1 = db_session.query(Tbuff1).first()
                break

    if tischno == 0:
        fl_code = 2

        return generate_output()