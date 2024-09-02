from functions.additional_functions import *
import decimal
from functions.htpint import htpint
from models import Guest, Artikel

def prepare_ts_restdeposit_paybl(pvilanguage:int, selected_gastnr:int, sorttype:int):
    f_tittle = ""
    artikel_list_list = []
    lvcarea:str = "ts_rest_deposit_pay"
    unallocated_subgrp:int = 0
    guest = artikel = None

    artikel_list = None

    artikel_list_list, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":str, "artart":int, "payment":decimal, "pay_exrate":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_tittle, artikel_list_list, lvcarea, unallocated_subgrp, guest, artikel


        nonlocal artikel_list
        nonlocal artikel_list_list
        return {"f_tittle": f_tittle, "artikel-list": artikel_list_list}

    def display_artikel():

        nonlocal f_tittle, artikel_list_list, lvcarea, unallocated_subgrp, guest, artikel


        nonlocal artikel_list
        nonlocal artikel_list_list

        if sorttype == 1:

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (((Artikel.artart == 6) |  (Artikel.artart == 7)) |  ((Artikel.artart == 2) &  ((Artikel.zwkum == unallocated_subgrp)))) &  (Artikel.activeflag)).all():
                assign_it()
        else:

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == 0) &  (((Artikel.artart == 6) |  (Artikel.artart == 7)) |  ((Artikel.artart == 2) &  ((Artikel.zwkum == unallocated_subgrp)))) &  (Artikel.activeflag)).all():
                assign_it()


    def assign_it():

        nonlocal f_tittle, artikel_list_list, lvcarea, unallocated_subgrp, guest, artikel


        nonlocal artikel_list
        nonlocal artikel_list_list


        artikel_list = Artikel_list()
        artikel_list_list.append(artikel_list)

        artikel_list.artnr = artikel.artnr
        artikel_list.departement = artikel.departement
        artikel_list.bezeich = artikel.bezeich
        artikel_list.artart = artikel.artart
        artikel_list.pay_exrate = 1


    unallocated_subgrp = get_output(htpint(116))
    f_tittle = translateExtended ("Restaurant Deposit Payment", lvcarea, "")

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == selected_gastnr)).first()

    if guest:
        f_tittle = f_tittle + "  -  " + guest.name + "," + guest.vorname1
    display_artikel()

    return generate_output()