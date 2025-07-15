#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Htparam

def prepare_ts_disc1bl(room:string, dept:int, tischnr:int):

    prepare_cache ([Htparam])

    disc_alert = True
    disc_service = False
    disc_tax = False
    voucher_art = 0
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    prefix_rm = ""
    procent = to_decimal("0.0")
    t_h_bill_data = []
    h_bill = htparam = None

    t_h_bill = None

    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal disc_alert, disc_service, disc_tax, voucher_art, disc_art1, disc_art2, disc_art3, prefix_rm, procent, t_h_bill_data, h_bill, htparam
        nonlocal room, dept, tischnr


        nonlocal t_h_bill
        nonlocal t_h_bill_data

        return {"disc_alert": disc_alert, "disc_service": disc_service, "disc_tax": disc_tax, "voucher_art": voucher_art, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "prefix_rm": prefix_rm, "procent": procent, "t-h-bill": t_h_bill_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1203)]})

    if htparam.paramgruppe == 19 and htparam.feldtyp == 4:
        disc_alert = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})
    disc_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})
    disc_tax = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
    voucher_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 790)]})

    if htparam.finteger != 0:
        prefix_rm = to_string(htparam.finteger)

        if substring(room, 0, 1) == (prefix_rm).lower() :

            htparam = get_cache (Htparam, {"paramnr": [(eq, 791)]})
            procent =  to_decimal(htparam.fdecimal)

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, tischnr)],"flag": [(eq, 0)]})

    if h_bill:
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    return generate_output()