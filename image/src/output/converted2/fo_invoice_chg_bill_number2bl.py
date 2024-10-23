from functions.additional_functions import *
import decimal
from models import Guest

def fo_invoice_chg_bill_number2bl(bill_gastnr:int):
    resname = ""
    g_address:str = ""
    g_wonhort:str = ""
    g_plz:str = ""
    g_land:str = ""
    guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, g_address, g_wonhort, g_plz, g_land, guest
        nonlocal bill_gastnr


        return {"resname": resname}


    guest = db_session.query(Guest).filter(
             (Guest.gastnr == bill_gastnr)).first()
    g_address = guest.adresse1
    g_wonhort = guest.wohnort
    g_plz = guest.plz
    g_land = guest.land

    if g_address == None:
        g_address = ""

    if g_wonhort == None:
        g_wonhort = ""

    if g_plz == None:
        g_plz = ""

    if g_land == None:
        g_land = ""
    resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr (10) + g_address + chr (10) + g_wonhort + " " + g_plz + chr (10) + g_land

    return generate_output()