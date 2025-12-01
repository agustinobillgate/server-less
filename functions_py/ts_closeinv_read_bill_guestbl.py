#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Guest

def ts_closeinv_read_bill_guestbl(guestnr:int, rec_h_bill:int):

    prepare_cache ([Guest])

    rec_bill_guest = 0
    t_h_bill_data = []
    h_bill = guest = None

    t_h_bill = bill_guest = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_bill_guest, t_h_bill_data, h_bill, guest
        nonlocal guestnr, rec_h_bill
        nonlocal bill_guest


        nonlocal t_h_bill, bill_guest
        nonlocal t_h_bill_data

        return {"rec_bill_guest": rec_bill_guest, "t-h-bill": t_h_bill_data}

    bill_guest = get_cache (Guest, {"gastnr": [(eq, guestnr)]})
    rec_bill_guest = bill_guest._recid

    # h_bill = get_cache (H_bill, {"_recid": [(eq, rec_h_bill)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill._recid == rec_h_bill)).with_for_update().first()
    h_bill.bilname = bill_guest.name + ", " + bill_guest.vorname1 + " " + bill_guest.anrede1
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()