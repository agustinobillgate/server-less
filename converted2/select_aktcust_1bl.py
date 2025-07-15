#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Akt_cust

def select_aktcust_1bl(userinit:string):

    prepare_cache ([Guest])

    aktcustlist_data = []
    guest = akt_cust = None

    aktcustlist = None

    aktcustlist_data, Aktcustlist = create_model("Aktcustlist", {"name":string, "gastnr":int, "anrede1":string, "anredefirma":string, "adresse1":string, "plz":string, "wohnort":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal aktcustlist_data, guest, akt_cust
        nonlocal userinit


        nonlocal aktcustlist
        nonlocal aktcustlist_data

        return {"aktcustlist": aktcustlist_data}

    akt_cust_obj_list = {}
    for akt_cust, guest in db_session.query(Akt_cust, Guest).join(Guest,(Guest.gastnr == Akt_cust.gastnr)).filter(
             (Akt_cust.userinit == (userinit).lower())).order_by(Guest.name).all():
        if akt_cust_obj_list.get(akt_cust._recid):
            continue
        else:
            akt_cust_obj_list[akt_cust._recid] = True


        aktcustlist = Aktcustlist()
        aktcustlist_data.append(aktcustlist)

        aktcustlist.name = guest.name
        aktcustlist.gastnr = guest.gastnr
        aktcustlist.anrede1 = guest.anrede1
        aktcustlist.anredefirma = guest.anredefirma
        aktcustlist.adresse1 = guest.adresse1
        aktcustlist.plz = guest.plz
        aktcustlist.wohnort = guest.wohnort

    return generate_output()