#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Artikel, Zwkum

def artikel_admin_check_btn_exitbl(pvilanguage:int):

    prepare_cache ([Artikel])

    msg_str = ""
    lvcarea:string = "artikel-admin"
    hoteldpt = artikel = zwkum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, hoteldpt, artikel, zwkum
        nonlocal pvilanguage

        return {"msg_str": msg_str}


    artikel_obj_list = {}
    for artikel, hoteldpt in db_session.query(Artikel, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == Artikel.departement)).order_by(Artikel._recid).yield_per(100):
        if artikel_obj_list.get(artikel._recid):
            continue
        else:
            artikel_obj_list[artikel._recid] = True

        zwkum = get_cache (Zwkum, {"zknr": [(eq, artikel.zwkum)],"departement": [(eq, artikel.departement)]})

        if not zwkum:
            msg_str = translateExtended ("Wrong subgroup setup!", lvcarea, "") + chr_unicode(10) + translateExtended ("Artno : ", lvcarea, "") + to_string(artikel.artnr) + chr_unicode(10) + translateExtended ("Dept : ", lvcarea, "") + to_string(artikel.departement)

        if msg_str != "":
            break

    return generate_output()