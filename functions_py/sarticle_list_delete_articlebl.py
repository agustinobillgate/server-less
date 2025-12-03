#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, L_order, L_op, H_rezlin, H_rezept, L_lager, L_verbrauch, L_artikel

def sarticle_list_delete_articlebl(pvilanguage:int, artnr:int):

    prepare_cache ([L_order, L_op, H_rezlin, H_rezept, L_lager])

    str_msg = ""
    delete_it = True
    lvcarea:string = "sarticle-list"
    l_bestand = l_order = l_op = h_rezlin = h_rezept = l_lager = l_verbrauch = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, delete_it, lvcarea, l_bestand, l_order, l_op, h_rezlin, h_rezept, l_lager, l_verbrauch, l_artikel
        nonlocal pvilanguage, artnr

        return {"str_msg": str_msg, "delete_it": delete_it}


    l_bestand = get_cache (L_bestand, {"artnr": [(eq, artnr)],"lager_nr": [(eq, 0)]})

    if l_bestand:
        str_msg = translateExtended ("Stock Onhand exists, deleting not possible.", lvcarea, "")
        delete_it = False

        return generate_output()

    l_order = get_cache (L_order, {"artnr": [(eq, artnr)]})

    if l_order:
        str_msg = translateExtended ("Article in used by order file", lvcarea, "") + chr_unicode(10) + "Document No: " + l_order.docu_nr
        delete_it = False

        return generate_output()

    if delete_it:

        l_op = get_cache (L_op, {"artnr": [(eq, artnr)]})

        if l_op:
            str_msg = translateExtended ("Article in used by stock in-/out operation file", lvcarea, "") + chr_unicode(10) + "Document No: " + l_op.docu_nr + chr_unicode(10) + "Delivery Note: " + l_op.lscheinnr
            delete_it = False

            return generate_output()

    if delete_it:

        h_rezlin = get_cache (H_rezlin, {"artnrlager": [(eq, artnr)]})

        if h_rezlin:

            h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrrezept)]})
            str_msg = translateExtended ("Article in used by recipe file", lvcarea, "") + chr_unicode(10) + to_string(h_rezept.artnrrezept) + " - " + h_rezept.bezeich
            delete_it = False

            return generate_output()

    if delete_it:

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            for l_bestand in db_session.query(L_bestand).filter(
                     (L_bestand.artnr == artnr) & (L_bestand.lager_nr == l_lager.lager_nr)).with_for_update().order_by(L_bestand._recid).all():
                db_session.delete(l_bestand)

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == artnr)).with_for_update().order_by(L_verbrauch._recid).all():
            db_session.delete(l_verbrauch)

        l_artikel = db_session.query(L_artikel).filter(
                 (L_artikel.artnr == artnr)).with_for_update().first()

        if l_artikel:
            db_session.delete(l_artikel)
            str_msg = translateExtended ("Article deleted", lvcarea, "")

    return generate_output()