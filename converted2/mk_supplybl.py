from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant, Nation, L_segment

def mk_supplybl(pvilanguage:int, casetype:int, schar:str, intvar:int, bezeich:str):
    msg_str = ""
    lvcarea:str = "mk-supply"
    l_lieferant = nation = l_segment = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, l_lieferant, nation, l_segment
        nonlocal pvilanguage, casetype, schar, intvar, bezeich


        return {"msg_str": msg_str, "bezeich": bezeich}


    if casetype == 1:

        l_lieferant = db_session.query(L_lieferant).filter(
                 (func.lower(L_lieferant.firma) == (schar).lower())).first()

        if l_lieferant:
            msg_str = msg_str + translateExtended ("Other Supplier with the same company name exists.", lvcarea, "") + chr(2)
    elif casetype == 2:

        nation = db_session.query(Nation).filter(
                 (func.lower(Nation.kurzbez) == (schar).lower())).first()

        if not nation:
            msg_str = msg_str + translateExtended ("Wrong Entry.", lvcarea, "") + chr(2)
    elif casetype == 3:

        l_segment = db_session.query(L_segment).filter(
                 (L_segment.l_segmentcode == intvar)).first()

        if l_segment:
            bezeich = l_segment.l_bezeich
        else:
            msg_str = msg_str + translateExtended ("Wrong Entry.", lvcarea, "") + chr(2)

    return generate_output()