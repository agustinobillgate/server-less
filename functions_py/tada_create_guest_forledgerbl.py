#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guest

def tada_create_guest_forledgerbl(order_name:string, order_phone:string, order_email:string):

    prepare_cache ([Queasy, Guest])

    msg_str = ""
    payment_param:int = 0
    curr_gastnr:int = 0
    queasy = guest = None

    bguest = None

    Bguest = create_buffer("Bguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, payment_param, curr_gastnr, queasy, guest
        nonlocal order_name, order_phone, order_email
        nonlocal bguest


        nonlocal bguest

        return {"msg_str": msg_str}


    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 26)]})

    if queasy:
        payment_param = to_int(queasy.char2)
    else:
        msg_str = "Artikel Number For Guest Ledger Not Available!"

        return generate_output()

    # guest = get_cache (Guest, {"mobil_telefon": [(eq, order_phone)],"karteityp": [(eq, 0)]})
    guest = db_session.query(Guest).filter(Guest.mobil_telefon == order_phone, Guest.karteityp == 0).with_for_update().first()

    if not guest:

        # guest = get_cache (Guest, {"telefon": [(eq, order_phone)],"karteityp": [(eq, 0)]})
        guest = db_session.query(Guest).filter(Guest.telefon == order_phone, Guest.karteityp == 0).with_for_update().first()

        if not guest:

            for bguest in db_session.query(Bguest).order_by(Bguest.gastnr.desc()).all():
                curr_gastnr = bguest.gastnr
                break

            if curr_gastnr == 0:
                curr_gastnr = 1
            else:
                curr_gastnr = curr_gastnr + 1
            guest = Guest()
            db_session.add(guest)

            guest.karteityp = 0
            guest.name = order_name
            guest.email_adr = order_email
            guest.telefon = order_phone
            guest.mobil_telefon = order_phone
            guest.gastnr = curr_gastnr
            guest.zahlungsart = payment_param
            guest.point_gastnr = payment_param
        else:
            guest.name = order_name
            guest.email_adr = order_email
            guest.telefon = order_phone
            guest.mobil_telefon = order_phone
            guest.zahlungsart = payment_param
            guest.point_gastnr = payment_param
    else:
        guest.name = order_name
        guest.email_adr = order_email
        guest.telefon = order_phone
        guest.mobil_telefon = order_phone
        guest.zahlungsart = payment_param
        guest.point_gastnr = payment_param
    pass
    pass

    return generate_output()