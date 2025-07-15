#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def eg_chgreq_stock_nrbl(stock_stock_nr:int):

    prepare_cache ([L_artikel])

    bez = ""
    t_ek_aktuell = to_decimal("0.0")
    avail_inv = False
    l_artikel = None

    inventory = None

    Inventory = create_buffer("Inventory",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bez, t_ek_aktuell, avail_inv, l_artikel
        nonlocal stock_stock_nr
        nonlocal inventory


        nonlocal inventory

        return {"bez": bez, "t_ek_aktuell": t_ek_aktuell, "avail_inv": avail_inv}


    inventory = get_cache (L_artikel, {"artnr": [(eq, stock_stock_nr)]})

    if inventory:
        bez = inventory.bezeich
        t_ek_aktuell =  to_decimal(inventory.ek_aktuell)
        avail_inv = True

    return generate_output()