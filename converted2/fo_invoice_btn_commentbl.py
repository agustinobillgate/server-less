#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Guest

def fo_invoice_btn_commentbl(bil_recid:int):

    prepare_cache ([Bill, Guest])

    resname = ""
    g_address:string = ""
    g_wonhort:string = ""
    g_plz:string = ""
    g_land:string = ""
    bill = guest = None

    guestmember = None

    Guestmember = create_buffer("Guestmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, g_address, g_wonhort, g_plz, g_land, bill, guest
        nonlocal bil_recid
        nonlocal guestmember


        nonlocal guestmember

        return {"resname": resname}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
    pass

    guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})
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