from functions.additional_functions import *
import decimal
from models import L_artikel

def pchase_book_sartnrbl(pvilanguage:int, s_artnr:int):
    s_bezeich = ""
    lvcarea:str = "pchase_book"
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_bezeich, lvcarea, l_artikel


        return {"s_bezeich": s_bezeich}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if l_artikel:
        s_bezeich = l_artikel.bezeich
    else:
        s_bezeich = translateExtended ("Article Description", lvcarea, "")

    return generate_output()