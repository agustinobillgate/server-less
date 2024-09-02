from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bill_line, Billjournal, H_bill_line, H_journal, Zimmer, Debitor, L_kredit, Res_line, Reservation

def check_record_bedienerbl(pvilanguage:int, userinit:str, bed_userinit:str, nr:int):
    its_ok = False
    msg_str = ""
    lvcarea:str = "check_record_bediener"
    bill_line = billjournal = h_bill_line = h_journal = zimmer = debitor = l_kredit = res_line = reservation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, lvcarea, bill_line, billjournal, h_bill_line, h_journal, zimmer, debitor, l_kredit, res_line, reservation


        return {"its_ok": its_ok, "msg_str": msg_str}

    def check_record():

        nonlocal its_ok, msg_str, lvcarea, bill_line, billjournal, h_bill_line, h_journal, zimmer, debitor, l_kredit, res_line, reservation

        bill_line = db_session.query(Bill_line).filter(
                (func.lower(Bill_line.(userinit).lower()) == (userinit).lower())).first()

        if bill_line:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Bill line exists, deleting not possible.", lvcarea, "")

        billjournal = db_session.query(Billjournal).filter(
                (func.lower(Billjournal.(userinit).lower()) == (userinit).lower())).first()

        if billjournal:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Bill journal exists, deleting not possible.", lvcarea, "")

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.kellner_nr == nr)).first()

        if h_bill_line:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Restaurant bill line exists, deleting not possible.", lvcarea, "")

        h_journal = db_session.query(H_journal).filter(
                (H_journal.kellner_nr == nr)).first()

        if h_journal:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Restaurant bill journal exists, deleting not possible.", lvcarea, "")

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.bediener_nr_stat == nr)).first()

        if zimmer:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Last status changed of Room-# :", lvcarea, "") + zimmer.zinr + " " + translateExtended ("by this user_id, deleting not possible.", lvcarea, "")

        debitor = db_session.query(Debitor).filter(
                (Debitor.bediener_nr == nr)).first()

        if debitor:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("A/R record exists, deleting not possible.", lvcarea, "")

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.bediener_nr == nr)).first()

        if l_kredit:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("A/P record exists, deleting not possible.", lvcarea, "")

        res_line = db_session.query(Res_line).filter(
                (func.lower(Res_line.cancelled_id) == (userinit).lower()) |  (func.lower(Res_line.changed_id) == (bed_userinit).lower())).first()

        if res_line:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")

        reservation = db_session.query(Reservation).filter(
                (func.lower(Reservation.useridanlage) == (userinit).lower()) |  (func.lower(Reservation.useridmutat) == (bed_userinit).lower())).first()

        if reservation:
            its_ok = False
            msg_str = msg_str + chr(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")

    check_record()

    return generate_output()