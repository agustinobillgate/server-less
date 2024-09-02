from functions.additional_functions import *
import decimal
from models import Guest, Akt_cust

def select_aktcustbl():
    aktcustlist_list = []
    guest = akt_cust = None

    aktcustlist = None

    aktcustlist_list, Aktcustlist = create_model("Aktcustlist", {"name":str, "gastnr":int, "anrede1":str, "anredefirma":str, "adresse1":str, "plz":str, "wohnort":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal aktcustlist_list, guest, akt_cust


        nonlocal aktcustlist
        nonlocal aktcustlist_list
        return {"aktcustlist": aktcustlist_list}

    akt_cust_obj_list = []
    for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr)).filter(
            (Akt_cust.userinit == userinit)).all():
        if akt_cust._recid in akt_cust_obj_list:
            continue
        else:
            akt_cust_obj_list.append(akt_cust._recid)


        aktcustlist = Aktcustlist()
        aktcustlist_list.append(aktcustlist)

        aktcustlist.name = guest.name
        aktcustlist.gastnr = guest.gastnr
        aktcustlist.anrede1 = guest.anrede1
        aktcustlist.anredefirma = guest.anredefirma
        aktcustlist.adresse1 = guest.adresse1
        aktcustlist.plz = guest.plz
        aktcustlist.wohnort = guest.wohnort

    return generate_output()