#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint
from models import Guest, Artikel

def prepare_ts_restdeposit_paybl(pvilanguage:int, selected_gastnr:int, sorttype:int):

    prepare_cache ([Guest, Artikel])

    f_tittle = ""
    artikel_list_data = []
    lvcarea:string = "ts-rest-deposit-pay"
    unallocated_subgrp:int = 0
    guest = artikel = None

    artikel_list = None

    artikel_list_data, Artikel_list = create_model("Artikel_list", {"artnr":int, "departement":int, "bezeich":string, "artart":int, "payment":Decimal, "pay_exrate":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_tittle, artikel_list_data, lvcarea, unallocated_subgrp, guest, artikel
        nonlocal pvilanguage, selected_gastnr, sorttype


        nonlocal artikel_list
        nonlocal artikel_list_data

        return {"f_tittle": f_tittle, "artikel-list": artikel_list_data}

    def display_artikel():

        nonlocal f_tittle, artikel_list_data, lvcarea, unallocated_subgrp, guest, artikel
        nonlocal pvilanguage, selected_gastnr, sorttype


        nonlocal artikel_list
        nonlocal artikel_list_data

        if sorttype == 1:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & (((Artikel.artart == 6) | (Artikel.artart == 7)) | ((Artikel.artart == 2) & ((Artikel.zwkum == unallocated_subgrp)))) & (Artikel.activeflag)).order_by(Artikel.artnr).all():
                assign_it()
        else:

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & (((Artikel.artart == 6) | (Artikel.artart == 7)) | ((Artikel.artart == 2) & ((Artikel.zwkum == unallocated_subgrp)))) & (Artikel.activeflag)).order_by(Artikel.bezeich).all():
                assign_it()

    def assign_it():

        nonlocal f_tittle, artikel_list_data, lvcarea, unallocated_subgrp, guest, artikel
        nonlocal pvilanguage, selected_gastnr, sorttype


        nonlocal artikel_list
        nonlocal artikel_list_data


        artikel_list = Artikel_list()
        artikel_list_data.append(artikel_list)

        artikel_list.artnr = artikel.artnr
        artikel_list.departement = artikel.departement
        artikel_list.bezeich = artikel.bezeich
        artikel_list.artart = artikel.artart
        artikel_list.pay_exrate = 1

    unallocated_subgrp = get_output(htpint(116))
    f_tittle = translateExtended ("Restaurant Deposit Payment", lvcarea, "")

    guest = get_cache (Guest, {"gastnr": [(eq, selected_gastnr)]})

    if guest:
        f_tittle = f_tittle + " - " + guest.name + "," + guest.vorname1
    display_artikel()

    return generate_output()