#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill_line, Billjournal, H_bill_line, H_journal, Zimmer, Debitor, L_kredit, Res_line, Reservation

def check_record_bedienerbl(pvilanguage:int, userinit:string, bed_userinit:string, nr:int):

    prepare_cache ([Zimmer])

    its_ok = True
    msg_str = ""
    lvcarea:string = "check-record-bediener"
    bill_line = billjournal = h_bill_line = h_journal = zimmer = debitor = l_kredit = res_line = reservation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, lvcarea, bill_line, billjournal, h_bill_line, h_journal, zimmer, debitor, l_kredit, res_line, reservation
        nonlocal pvilanguage, userinit, bed_userinit, nr

        return {"its_ok": its_ok, "msg_str": msg_str}

    def check_record():

        nonlocal its_ok, msg_str, lvcarea, bill_line, billjournal, h_bill_line, h_journal, zimmer, debitor, l_kredit, res_line, reservation
        nonlocal pvilanguage, userinit, bed_userinit, nr

        bill_line = get_cache (Bill_line, {"userinit": [(eq, userinit)]})

        if bill_line:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Bill line exists, deleting not possible.", lvcarea, "")

        billjournal = get_cache (Billjournal, {"userinit": [(eq, userinit)]})

        if billjournal:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Bill journal exists, deleting not possible.", lvcarea, "")

        h_bill_line = get_cache (H_bill_line, {"kellner_nr": [(eq, nr)]})

        if h_bill_line:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Restaurant bill line exists, deleting not possible.", lvcarea, "")

        h_journal = get_cache (H_journal, {"kellner_nr": [(eq, nr)]})

        if h_journal:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Restaurant bill journal exists, deleting not possible.", lvcarea, "")

        zimmer = get_cache (Zimmer, {"bediener_nr_stat": [(eq, nr)]})

        if zimmer:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Last status changed of Room-# :", lvcarea, "") + zimmer.zinr + " " + translateExtended ("by this user-id, deleting not possible.", lvcarea, "")

        debitor = get_cache (Debitor, {"bediener_nr": [(eq, nr)]})

        if debitor:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("A/R record exists, deleting not possible.", lvcarea, "")

        l_kredit = get_cache (L_kredit, {"bediener_nr": [(eq, nr)]})

        if l_kredit:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("A/P record exists, deleting not possible.", lvcarea, "")

        res_line = db_session.query(Res_line).filter(
                 (Res_line.cancelled_id == (userinit).lower()) | (Res_line.changed_id == (bed_userinit).lower())).first()

        if res_line:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")

        reservation = db_session.query(Reservation).filter(
                 (Reservation.useridanlage == (userinit).lower()) | (Reservation.useridmutat == (bed_userinit).lower())).first()

        if reservation:
            its_ok = False
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")


    check_record()

    return generate_output()