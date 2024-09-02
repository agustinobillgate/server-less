from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel

def mk_sarticle_bezeichbl(pvilanguage:int, l_bezeich:str):
    str_msg = ""
    lvcarea:str = "mk_sarticle"
    l_artikel = None

    l_art1 = None

    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, lvcarea, l_artikel
        nonlocal l_art1


        nonlocal l_art1
        return {"str_msg": str_msg}


    l_art1 = db_session.query(L_art1).filter(
            (func.lower(L_art1.bezeich) == (l_bezeich).lower())).first()

    if l_art1:
        str_msg = "&W" + translateExtended ("Same Description found with article number: ", lvcarea, "") + to_string(l_art1.artnr)

    return generate_output()