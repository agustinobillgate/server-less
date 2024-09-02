from functions.additional_functions import *
import decimal
from models import L_artikel

def eg_chgreq_stock_nrbl(stock_stock_nr:int):
    bez = ""
    t_ek_aktuell = 0
    avail_inv = False
    l_artikel = None

    inventory = None

    Inventory = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bez, t_ek_aktuell, avail_inv, l_artikel
        nonlocal inventory


        nonlocal inventory
        return {"bez": bez, "t_ek_aktuell": t_ek_aktuell, "avail_inv": avail_inv}


    inventory = db_session.query(Inventory).filter(
            (Inventory.artnr == stock_stock_nr)).first()

    if inventory:
        bez = inventory.bezeich
        t_ek_aktuell = inventory.ek_aktuell
        avail_inv = True

    return generate_output()