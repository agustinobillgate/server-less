#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Guest

def prepare_ts_clguestbl():

    prepare_cache ([Artikel, Guest])

    clguest_list_data = []
    artikel = guest = None

    clguest_list = None

    clguest_list_data, Clguest_list = create_model("Clguest_list", {"gname":string, "zahlungsart":int, "bezeich":string, "address":string, "gastnr":int, "karteityp":int, "bemerk":string, "kreditlimit":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal clguest_list_data, artikel, guest


        nonlocal clguest_list
        nonlocal clguest_list_data

        return {"clguest-list": clguest_list_data}


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
        clguest_list_data.append(clguest_list)

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
        clguest_list_data.append(clguest_list)

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

    return generate_output()