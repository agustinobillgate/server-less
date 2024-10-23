from functions.additional_functions import *
import decimal
from models import Hoteldpt, Artikel, Zwkum

def artikel_admin_check_btn_exitbl(pvilanguage:int):
    msg_str = ""
    lvcarea:str = "artikel-admin"
    hoteldpt = artikel = zwkum = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, hoteldpt, artikel, zwkum
        nonlocal pvilanguage


        return {"msg_str": msg_str}


    artikel_obj_list = []
    for artikel, hoteldpt in db_session.query(Artikel, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == Artikel.departement)).order_by(Artikel._recid).all():
        if artikel._recid in artikel_obj_list:
            continue
        else:
            artikel_obj_list.append(artikel._recid)

        zwkum = db_session.query(Zwkum).filter(
                 (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement)).first()

        if not zwkum:
            msg_str = translateExtended ("Wrong subgroup setup!", lvcarea, "") + chr(10) + translateExtended ("Artno : ", lvcarea, "") + to_string(artikel.artnr) + chr(10) + translateExtended ("Dept : ", lvcarea, "") + to_string(artikel.departement)

        if msg_str != "":
            break

    return generate_output()