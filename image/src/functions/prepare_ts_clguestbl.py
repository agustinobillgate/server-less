from functions.additional_functions import *
import decimal
from models import Artikel, Guest

def prepare_ts_clguestbl():
    clguest_list_list = []
    artikel = guest = None

    clguest_list = None

    clguest_list_list, Clguest_list = create_model("Clguest_list", {"gname":str, "zahlungsart":int, "bezeich":str, "address":str, "gastnr":int, "karteityp":int, "bemerk":str, "kreditlimit":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal clguest_list_list, artikel, guest


        nonlocal clguest_list
        nonlocal clguest_list_list
        return {"clguest-list": clguest_list_list}

    pass


    guest_obj_list = []
    for guest, artikel in db_session.query(Guest, Artikel).join(Artikel,(Artikel.artnr == Guest.zahlungsart) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).filter(
            (Guest.karteityp == 0) &  (Guest.gastnr > 0) &  (Guest.point_gastnr > 0)).all():
        if guest._recid in guest_obj_list:
            continue
        else:
            guest_obj_list.append(guest._recid)


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
        clguest_list.bemerk = guest.bemerk
        clguest_list.kreditlimit = guest.kreditlimit

    guest_obj_list = []
    for guest, artikel in db_session.query(Guest, Artikel).join(Artikel,(Artikel.artnr == Guest.zahlungsart) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).filter(
            (Guest.karteityp > 0) &  (Guest.gastnr > 0) &  (Guest.zahlungsart > 0)).all():
        if guest._recid in guest_obj_list:
            continue
        else:
            guest_obj_list.append(guest._recid)


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
        clguest_list.bemerk = guest.bemerk
        clguest_list.kreditlimit = guest.kreditlimit

    return generate_output()