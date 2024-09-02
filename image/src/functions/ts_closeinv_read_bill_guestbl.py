from functions.additional_functions import *
import decimal
from models import H_bill, Guest

def ts_closeinv_read_bill_guestbl(guestnr:int, rec_h_bill:int):
    rec_bill_guest = 0
    t_h_bill_list = []
    h_bill = guest = None

    t_h_bill = bill_guest = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Bill_guest = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_bill_guest, t_h_bill_list, h_bill, guest
        nonlocal bill_guest


        nonlocal t_h_bill, bill_guest
        nonlocal t_h_bill_list
        return {"rec_bill_guest": rec_bill_guest, "t-h-bill": t_h_bill_list}

    bill_guest = db_session.query(Bill_guest).filter(
            (Bill_guest.gastnr == guestnr)).first()
    rec_bill_guest = bill_guest._recid

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_h_bill)).first()
    h_bill.bilname = bill_guest.name + ", " + bill_guest.vorname1 + " " + bill_guest.anrede1

    h_bill = db_session.query(H_bill).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    return generate_output()