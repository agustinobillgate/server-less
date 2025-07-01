#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Debitor, Artikel, Guest

def disp_debitorbl():

    prepare_cache ([Debitor, Guest])

    dlist_list = []
    debitor = artikel = guest = None

    dlist = None

    dlist_list, Dlist = create_model("Dlist", {"gastnr":int, "gname":string, "city":string, "gtype":int, "aging":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dlist_list, debitor, artikel, guest


        nonlocal dlist
        nonlocal dlist_list

        return {"dlist": dlist_list}

    def create_list():

        nonlocal dlist_list, debitor, artikel, guest


        nonlocal dlist
        nonlocal dlist_list

        deb_buff = None
        dlist_list.clear()
        Deb_buff =  create_buffer("Deb_buff",Debitor)

        debitor_obj_list = {}
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.artart == 2) & (Artikel.departement == 0)).filter(
                 (Debitor.opart <= 1) & (Debitor.saldo != 0)).order_by(Debitor._recid).all():
            if debitor_obj_list.get(debitor._recid):
                continue
            else:
                debitor_obj_list[debitor._recid] = True

            guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

            dlist = query(dlist_list, filters=(lambda dlist: dlist.gastnr == debitor.gastnr), first=True)

            if not dlist:
                dlist = Dlist()
                dlist_list.append(dlist)

                dlist.gastnr = guest.gastnr
                dlist.gname = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                dlist.gtype = guest.karteityp
                dlist.city = guest.wohnort


            dlist.aging =  to_decimal(dlist.aging) + to_decimal(debitor.saldo)

    create_list()

    return generate_output()