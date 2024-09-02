from functions.additional_functions import *
import decimal
from models import Debitor, Artikel, Guest

def disp_debitorbl():
    dlist_list = []
    debitor = artikel = guest = None

    dlist = deb_buff = None

    dlist_list, Dlist = create_model("Dlist", {"gastnr":int, "gname":str, "city":str, "gtype":int, "aging":decimal})

    Deb_buff = Debitor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dlist_list, debitor, artikel, guest
        nonlocal deb_buff


        nonlocal dlist, deb_buff
        nonlocal dlist_list
        return {"dlist": dlist_list}

    def create_list():

        nonlocal dlist_list, debitor, artikel, guest
        nonlocal deb_buff


        nonlocal dlist, deb_buff
        nonlocal dlist_list


        dlist_list.clear()
        Deb_buff = Debitor

        debitor_obj_list = []
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.artart == 2) &  (Artikel.departement == 0)).filter(
                (Debitor.opart <= 1) &  (Debitor.saldo != 0)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == debitor.gastnr)).first()

            dlist = query(dlist_list, filters=(lambda dlist :dlist.gastnr == debitor.gastnr), first=True)

            if not dlist:
                dlist = Dlist()
                dlist_list.append(dlist)

                dlist.gastnr = guest.gastnr
                dlist.gname = guest.name + ", " + guest.vorname1 + " " +\
                        guest.anrede1 + guest.anredefirma
                dlist.gtype = guest.karteityp
                dlist.city = guest.wohnort


            dlist.aging = dlist.aging + debitor.saldo


    create_list()

    return generate_output()