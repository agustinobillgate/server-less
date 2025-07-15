#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from functions.htpint import htpint
from models import Bediener, Htparam, Nation, Guest

def prepare_res_gname1bl(gastno:int, selected_gastnr:int, user_init:string):

    prepare_cache ([Htparam, Nation, Guest])

    def_natcode = ""
    gastid = ""
    gname = ""
    gnat = ""
    gland = ""
    gphone = ""
    bdate_flag = False
    search_start = 0
    bediener = htparam = nation = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal def_natcode, gastid, gname, gnat, gland, gphone, bdate_flag, search_start, bediener, htparam, nation, guest
        nonlocal gastno, selected_gastnr, user_init

        return {"def_natcode": def_natcode, "gastid": gastid, "gname": gname, "gnat": gnat, "gland": gland, "gphone": gphone, "bdate_flag": bdate_flag, "search_start": search_start}

    def create_list():

        nonlocal def_natcode, gastid, gname, gnat, gland, gphone, bdate_flag, search_start, bediener, htparam, nation, guest
        nonlocal gastno, selected_gastnr, user_init

        guest = get_cache (Guest, {"gastnr": [(eq, selected_gastnr)]})

        if guest:
            gastid = guest.ausweis_nr1
            gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1
            gnat = guest.nation1
            gland = guest.land

            if guest and guest.karteityp == 0:
                gphone = guest.telefon

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

    if nation:
        def_natcode = nation.kurzbez

    if gastno > 0:

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

        if guest:

            if guest.nation1 != "":
                def_natcode = guest.nation1

            elif guest.land != "":
                def_natcode = guest.land
    create_list()
    bdate_flag = get_output(htplogic(937))
    search_start = get_output(htpint(968))

    return generate_output()