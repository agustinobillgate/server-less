#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Guest, Artikel

def chg_gcf_btn_helpbl(curr_select:string, int1:int, char1:string):

    prepare_cache ([Bediener, Guest, Artikel])

    char2 = ""
    bediener = guest = artikel = None

    usr = guest0 = None

    Usr = create_buffer("Usr",Bediener)
    Guest0 = create_buffer("Guest0",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal char2, bediener, guest, artikel
        nonlocal curr_select, int1, char1
        nonlocal usr, guest0


        nonlocal usr, guest0

        return {"char2": char2}


    if curr_select.lower()  == ("sales-id").lower() :

        if int1 > 0:

            usr = get_cache (Bediener, {"userinit": [(eq, char1)]})
            char2 = usr.username

    elif curr_select.lower()  == ("master").lower() :

        guest0 = get_cache (Guest, {"gastnr": [(eq, int1)]})
        char2 = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1

    if curr_select.lower()  == ("payment").lower() :

        artikel = get_cache (Artikel, {"artnr": [(eq, int1)],"departement": [(eq, 0)]})
        char2 = artikel.bezeich

    return generate_output()