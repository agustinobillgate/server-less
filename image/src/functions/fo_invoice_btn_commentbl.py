from functions.additional_functions import *
import decimal
from models import Bill, Guest

def fo_invoice_btn_commentbl(bil_recid:int):
    resname = ""
    g_address:str = ""
    g_wonhort:str = ""
    g_plz:str = ""
    g_land:str = ""
    bill = guest = None

    guestmember = None

    Guestmember = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resname, g_address, g_wonhort, g_plz, g_land, bill, guest
        nonlocal guestmember


        nonlocal guestmember
        return {"resname": resname}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    bill = db_session.query(Bill).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == bill.gastnr)).first()
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
    resname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr(10) + g_address + chr(10) + g_wonhort + " " + g_plz + chr(10) + g_land

    return generate_output()