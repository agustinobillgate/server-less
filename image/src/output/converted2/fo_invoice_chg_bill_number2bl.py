#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def fo_invoice_chg_bill_number2bl(bill_gastnr:int):

    prepare_cache ([Guest])

    resname = ""
    g_address:string = ""
    g_wonhort:string = ""
    g_plz:string = ""
    g_land:string = ""
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, g_address, g_wonhort, g_plz, g_land, guest
        nonlocal bill_gastnr

        return {"resname": resname}


    guest = get_cache (Guest, {"gastnr": [(eq, bill_gastnr)]})
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
    resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr_unicode(10) + g_address + chr_unicode(10) + g_wonhort + " " + g_plz + chr_unicode(10) + g_land

    return generate_output()