from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation, Prmarket

def nation_admin_checkbl(pvilanguage:int, kurzbez:str, nationnr:int, natbez:str, untergruppe:int, hauptgruppe:int, language:int, marksegm:str):
    msg_str = ""
    lvcarea:str = "nation_admin_check"
    nation = prmarket = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, nation, prmarket


        return {"msg_str": msg_str}

    def fill_new_nation():

        nonlocal msg_str, lvcarea, nation, prmarket


        nationnr = nationnr
        nation.kurzbez = kurzbez
        nation.bezeich = natbez
        nation.untergruppe = untergruppe
        nation.hauptgruppe = hauptgruppe
        nation.language = language

        prmarket = db_session.query(Prmarket).filter(
                (func.lower(Prmarket.bezeich) == (marksegm).lower())).first()

        if prmarket:
            nation.bezeich = nation.bezeich + ";" + to_string(prmarket.nr)


    nation = db_session.query(Nation).filter(
            (func.lower(Nation.(kurzbez).lower()) == (kurzbez).lower()) &  (Nation.natcode == 0)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr(2) + translateExtended ("Nation code already exists, use other code.", lvcarea, "")

        return generate_output()

    nation = db_session.query(Nation).filter(
            (func.lower(Nation.(kurzbez).lower()) == (kurzbez).lower()) &  (Nation.natcode > 0)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr(2) + translateExtended ("nation code used for a region code, use other code.", lvcarea, "")

        return generate_output()

    if msg_str == "":
        nation = Nation()
        db_session.add(nation)

        fill_new_nation()

    return generate_output()