#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Artikel, Guest

def prepare_ts_clguestbl(dept_number:int, bill_number:int):

    prepare_cache ([Queasy, Artikel, Guest])

    clguest_list_list = []
    tada_flag:bool = False
    tada_guest:string = ""
    queasy = artikel = guest = None

    clguest_list = orderhdr = None

    clguest_list_list, Clguest_list = create_model("Clguest_list", {"gname":string, "zahlungsart":int, "bezeich":string, "address":string, "gastnr":int, "karteityp":int, "bemerk":string, "kreditlimit":Decimal})

    Orderhdr = create_buffer("Orderhdr",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal clguest_list_list, tada_flag, tada_guest, queasy, artikel, guest
        nonlocal dept_number, bill_number
        nonlocal orderhdr


        nonlocal clguest_list, orderhdr
        nonlocal clguest_list_list

        return {"clguest-list": clguest_list_list}

    guest_obj_list = {}
    guest = Guest()
    artikel = Artikel()
    for guest.name, guest.vorname1, guest.zahlungsart, guest.adresse1, guest.gastnr, guest.karteityp, guest.bemerkung, guest.kreditlimit, guest._recid, artikel.bezeich, artikel._recid in db_session.query(Guest.name, Guest.vorname1, Guest.zahlungsart, Guest.adresse1, Guest.gastnr, Guest.karteityp, Guest.bemerkung, Guest.kreditlimit, Guest._recid, Artikel.bezeich, Artikel._recid).join(Artikel,(Artikel.artnr == Guest.zahlungsart) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
             (Guest.karteityp == 0) & (Guest.gastnr > 0) & (Guest.point_gastnr > 0)).order_by(Guest.name).all():
        if guest_obj_list.get(guest._recid):
            continue
        else:
            guest_obj_list[guest._recid] = True


        clguest_list = Clguest_list()
        clguest_list_list.append(clguest_list)

        clguest_list.gname = guest.name + ", " + guest.vorname1 +\
                " " + guest.anrede1 +\
                guest.anredefirma
        clguest_list.zahlungsart = guest.zahlungsart
        clguest_list.bezeich = artikel.bezeich
        clguest_list.address = trim(guest.adresse1 +\
                " " + guest.adresse2 +\
                " " + guest.wohnort)
        clguest_list.gastnr = guest.gastnr
        clguest_list.karteityp = guest.karteityp
        clguest_list.bemerk = guest.bemerkung
        clguest_list.kreditlimit =  to_decimal(guest.kreditlimit)

    guest_obj_list = {}
    guest = Guest()
    artikel = Artikel()
    for guest.name, guest.vorname1, guest.zahlungsart, guest.adresse1, guest.gastnr, guest.karteityp, guest.bemerkung, guest.kreditlimit, guest._recid, artikel.bezeich, artikel._recid in db_session.query(Guest.name, Guest.vorname1, Guest.zahlungsart, Guest.adresse1, Guest.gastnr, Guest.karteityp, Guest.bemerkung, Guest.kreditlimit, Guest._recid, Artikel.bezeich, Artikel._recid).join(Artikel,(Artikel.artnr == Guest.zahlungsart) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
             (Guest.karteityp > 0) & (Guest.gastnr > 0) & (Guest.zahlungsart > 0)).order_by(Guest.name).all():
        if guest_obj_list.get(guest._recid):
            continue
        else:
            guest_obj_list[guest._recid] = True


        clguest_list = Clguest_list()
        clguest_list_list.append(clguest_list)

        clguest_list.gname = guest.name + ", " + guest.vorname1 +\
                " " + guest.anrede1 +\
                guest.anredefirma
        clguest_list.zahlungsart = guest.zahlungsart
        clguest_list.bezeich = artikel.bezeich
        clguest_list.address = trim(guest.adresse1 +\
                " " + guest.adresse2 +\
                " " + guest.wohnort)
        clguest_list.gastnr = guest.gastnr
        clguest_list.karteityp = guest.karteityp
        clguest_list.bemerk = guest.bemerkung
        clguest_list.kreditlimit =  to_decimal(guest.kreditlimit)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 26)]})

    if queasy:
        tada_flag = True
    else:
        tada_flag = False

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 4)]})

    if queasy:
        dept_number = to_int(queasy.char2)

    if tada_flag:

        orderhdr = get_cache (Queasy, {"key": [(eq, 271)],"betriebsnr": [(eq, 1)],"number1": [(eq, dept_number)],"number3": [(eq, bill_number)]})

        if orderhdr:
            tada_guest = entry(2, orderhdr.char2, "|")

        for clguest_list in query(clguest_list_list, filters=(lambda clguest_list: not matches(clguest_list.gname,r"*" + tada_guest + r",*"))):
            clguest_list_list.remove(clguest_list)

    return generate_output()