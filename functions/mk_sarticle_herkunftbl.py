from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation

def mk_sarticle_herkunftbl(pvilanguage:int, land:str, l_herkunft:str, land_bezeich:str):
    str_msg = ""
    lvcarea:str = "mk-sarticle"
    land_ok:bool = False
    nation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, lvcarea, land_ok, nation
        nonlocal pvilanguage, land, l_herkunft, land_bezeich


        return {"str_msg": str_msg, "l_herkunft": l_herkunft, "land_bezeich": land_bezeich}


    nation = db_session.query(Nation).filter(
             (func.lower(Nation.kurzbez) == (l_herkunft).lower())).first()

    if nation:
        land_ok = True
        land_bezeich = nation.bezeich

    if not land_ok:
        str_msg = translateExtended ("Wrong Entry", lvcarea, "")
        l_herkunft = land

    return generate_output()