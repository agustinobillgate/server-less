#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation, Prmarket

def nation_admin_checkbl(pvilanguage:int, kurzbez:string, nationnr:int, natbez:string, untergruppe:int, hauptgruppe:int, language:int, marksegm:string):

    prepare_cache ([Nation, Prmarket])

    msg_str = ""
    lvcarea:string = "nation-admin-check"
    nation = prmarket = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, nation, prmarket
        nonlocal pvilanguage, kurzbez, nationnr, natbez, untergruppe, hauptgruppe, language, marksegm

        return {"msg_str": msg_str}

    def fill_new_nation():

        nonlocal msg_str, lvcarea, nation, prmarket
        nonlocal pvilanguage, kurzbez, nationnr, natbez, untergruppe, hauptgruppe, language, marksegm


        nation.nationnr = nationnr
        nation.kurzbez = kurzbez
        nation.bezeich = natbez
        nation.untergruppe = untergruppe
        nation.hauptgruppe = hauptgruppe
        nation.language = language

        prmarket = get_cache (Prmarket, {"bezeich": [(eq, marksegm)]})

        if prmarket:
            nation.bezeich = nation.bezeich + ";" + to_string(prmarket.nr)

    nation = get_cache (Nation, {"kurzbez": [(eq, kurzbez)],"natcode": [(eq, 0)]})

    if nation and kurzbez != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Nation code already exists, use other code.", lvcarea, "")

        return generate_output()

    nation = db_session.query(Nation).filter(
             (Nation.kurzbez == (kurzbez).lower()) & (Nation.natcode > 0)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr_unicode(2) + translateExtended ("nation code used for a region code, use other code.", lvcarea, "")

        return generate_output()

    if msg_str == "":
        nation = Nation()
        db_session.add(nation)

        fill_new_nation()

    return generate_output()