from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.htplogic import htplogic
from functions.htpint import htpint
from models import Bediener, Htparam, Nation, Guest

def prepare_res_gname1bl(gastno:int, selected_gastnr:int, user_init:str):
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


        return {"def_natcode": def_natcode, "gastid": gastid, "gname": gname, "gnat": gnat, "gland": gland, "gphone": gphone, "bdate_flag": bdate_flag, "search_start": search_start}

    def create_list():

        nonlocal def_natcode, gastid, gname, gnat, gland, gphone, bdate_flag, search_start, bediener, htparam, nation, guest

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == selected_gastnr)).first()

        if guest:
            gastid = guest.ausweis_nr1
            gname = guest.name + ", " + guest.vorname1 + ", " + guest.anrede1
            gnat = guest.nation1
            gland = guest.land

            if guest and guest.karteityp == 0:
                gphone = guest.telefon


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 153)).first()

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == htparam.fchar)).first()

    if nation:
        def_natcode = nation.kurzbez

    if gastno > 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastno)).first()

        if guest:

            if guest.nation1 != "":
                def_natcode = guest.nation1

            elif guest.land != "":
                def_natcode = guest.land
    create_list()
    bdate_flag = get_output(htplogic(937))
    search_start = get_output(htpint(968))

    return generate_output()