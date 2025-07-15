#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Queasy, Htparam, H_artikel

def prepare_print_hbill1bl(hbrecid:int):

    prepare_cache ([H_bill, Queasy, Htparam, H_artikel])

    order_id = ""
    prdisc_flag = False
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    disc_zwkum = 0
    print_balance = False
    incl_service = False
    incl_mwst = False
    service_taxable = False
    print_fbtotal = False
    curr_dept:int = 0
    h_bill = queasy = htparam = h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal order_id, prdisc_flag, disc_art1, disc_art2, disc_art3, disc_zwkum, print_balance, incl_service, incl_mwst, service_taxable, print_fbtotal, curr_dept, h_bill, queasy, htparam, h_artikel
        nonlocal hbrecid

        return {"order_id": order_id, "prdisc_flag": prdisc_flag, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "disc_zwkum": disc_zwkum, "print_balance": print_balance, "incl_service": incl_service, "incl_mwst": incl_mwst, "service_taxable": service_taxable, "print_fbtotal": print_fbtotal}


    h_bill = get_cache (H_bill, {"_recid": [(eq, hbrecid)]})

    if h_bill and h_bill.departement != None:
        curr_dept = h_bill.departement

        if h_bill.betriebsnr != 0:

            queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

            if queasy:
                order_id = "/" + queasy.char2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 857)]})

    if htparam:
        prdisc_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam and htparam.finteger > 0:
        disc_art1 = htparam.finteger

    h_artikel = get_cache (H_artikel, {"artnr": [(eq, disc_art1)],"departement": [(eq, curr_dept)]})

    if h_artikel:
        disc_zwkum = h_artikel.zwkum

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    if htparam and htparam.finteger > 0:
        disc_art2 = htparam.finteger

        if disc_zwkum == 0 and disc_art2 != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, disc_art2)],"departement": [(eq, curr_dept)]})

            if h_artikel:
                disc_zwkum = h_artikel.zwkum

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})

    if htparam and htparam.finteger > 0:
        disc_art3 = htparam.finteger

        if disc_zwkum == 0 and disc_art3 != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, disc_art3)],"departement": [(eq, curr_dept)]})

            if h_artikel:
                disc_zwkum = h_artikel.zwkum

    htparam = get_cache (Htparam, {"paramnr": [(eq, 899)]})

    if htparam:
        print_balance = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

    if htparam:
        incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

    if htparam:
        incl_mwst = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

    if htparam:
        service_taxable = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 948)]})

    if htparam:

        if htparam.paramgruppe == 19 and htparam.flogical:
            print_fbtotal = htparam.flogical

    return generate_output()