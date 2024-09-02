from functions.additional_functions import *
import decimal
from models import L_bestand, L_order, L_op, H_rezlin, H_rezept, L_lager, L_verbrauch, L_artikel

def sarticle_list_delete_articlebl(pvilanguage:int, artnr:int):
    str_msg = ""
    delete_it = False
    lvcarea:str = "sarticle_list"
    l_bestand = l_order = l_op = h_rezlin = h_rezept = l_lager = l_verbrauch = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, delete_it, lvcarea, l_bestand, l_order, l_op, h_rezlin, h_rezept, l_lager, l_verbrauch, l_artikel


        return {"str_msg": str_msg, "delete_it": delete_it}


    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == artnr) &  (L_bestand.lager_nr == 0)).first()

    if l_bestand:
        str_msg = translateExtended ("Stock Onhand exists, deleting not possible.", lvcarea, "")
        delete_it = False

        return generate_output()

    l_order = db_session.query(L_order).filter(
            (L_order.artnr == artnr)).first()

    if l_order:
        str_msg = translateExtended ("Article in used by order file", lvcarea, "") + chr(10) + "Document No: " + l_order.docu_nr
        delete_it = False

        return generate_output()

    if delete_it:

        l_op = db_session.query(L_op).filter(
                (L_op.artnr == artnr)).first()

        if l_op:
            str_msg = translateExtended ("Article in used by stock in-/out operation file", lvcarea, "") + chr(10) + "Document No: " + l_op.docu_nr + chr(10) + "Delivery Note: " + l_op.lscheinnr
            delete_it = False

            return generate_output()

    if delete_it:

        h_rezlin = db_session.query(H_rezlin).filter(
                (H_rezlin.artnrlager == artnr)).first()

        if h_rezlin:

            h_rezept = db_session.query(H_rezept).filter(
                    (H_rezept.artnrrezept == h_rezlin.artnrrezept)).first()
            str_msg = translateExtended ("Article in used by recipe file", lvcarea, "") + chr(10) + to_string(h_rezept.artnrrezept) + " - " + h_rezept.bezeich
            delete_it = False

            return generate_output()

    if delete_it:

        for l_lager in db_session.query(L_lager).all():

            for l_bestand in db_session.query(L_bestand).filter(
                    (L_bestand.artnr == artnr) &  (L_bestand.lager_nr == l_lager.lager_nr)).all():
                db_session.delete(l_bestand)

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                (L_verbrauch.artnr == artnr)).all():
            db_session.delete(l_verbrauch)

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == artnr)).first()
        db_session.delete(l_artikel)
        str_msg = translateExtended ("Article deleted", lvcarea, "")

    return generate_output()