#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_bestand, L_order, L_op, H_rezlin, H_rezept, H_artikel, Dml_art, Reslin_queasy, Dml_artdep, L_lager, L_verbrauch

t_l_artikel_list, T_l_artikel = create_model_like(L_artikel, {"is_delete":bool, "is_select":bool})

def sarticle_list_bulk_delete_article_webbl(pvilanguage:int, t_l_artikel_list:[T_l_artikel]):

    prepare_cache ([L_order, L_op, H_rezlin, H_rezept, H_artikel, L_lager])

    str_msg = ""
    delete_it = True
    lvcarea:string = "sarticle-list"
    l_artikel = l_bestand = l_order = l_op = h_rezlin = h_rezept = h_artikel = dml_art = reslin_queasy = dml_artdep = l_lager = l_verbrauch = None

    t_l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, delete_it, lvcarea, l_artikel, l_bestand, l_order, l_op, h_rezlin, h_rezept, h_artikel, dml_art, reslin_queasy, dml_artdep, l_lager, l_verbrauch
        nonlocal pvilanguage


        nonlocal t_l_artikel

        return {"str_msg": str_msg, "delete_it": delete_it}

    t_l_artikel = query(t_l_artikel_list, filters=(lambda t_l_artikel: t_l_artikel.is_select  and t_l_artikel.is_delete), first=True)

    if not t_l_artikel:
        str_msg = translateExtended ("Select at least 1 article to delete", lvcarea, "")
        delete_it = False

        return generate_output()

    for t_l_artikel in query(t_l_artikel_list, filters=(lambda t_l_artikel: t_l_artikel.is_select  and t_l_artikel.is_delete)):

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, t_l_artikel.artnr)],"lager_nr": [(eq, 0)]})

        if l_bestand:
            str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Stock Onhand exists, deleting not possible.", lvcarea, "")
            delete_it = False

            return generate_output()

        l_order = get_cache (L_order, {"artnr": [(eq, t_l_artikel.artnr)]})

        if l_order:
            str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by order file", lvcarea, "") + chr_unicode(10) + "Document No: " + l_order.docu_nr
            delete_it = False

            return generate_output()

        if delete_it:

            l_op = get_cache (L_op, {"artnr": [(eq, t_l_artikel.artnr)]})

            if l_op:
                str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by stock in-/out operation file", lvcarea, "") + chr_unicode(10) + "Document No: " + l_op.docu_nr + chr_unicode(10) + "Delivery Note: " + l_op.lscheinnr
                delete_it = False

                return generate_output()

        if delete_it:

            h_rezlin = get_cache (H_rezlin, {"artnrlager": [(eq, t_l_artikel.artnr)]})

            if h_rezlin:

                h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, h_rezlin.artnrrezept)]})
                str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by recipe file", lvcarea, "") + chr_unicode(10) + to_string(h_rezept.artnrrezept) + " - " + h_rezept.bezeich
                delete_it = False

                return generate_output()

        if delete_it:

            h_artikel = get_cache (H_artikel, {"artnrlager": [(eq, t_l_artikel.artnr)]})

            if h_artikel:
                str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by outlet artikel stock item", lvcarea, "") + chr_unicode(10) + to_string(h_artikel.artnr) + " - " + h_artikel.bezeich
                delete_it = False

                return generate_output()

        if delete_it:

            dml_art = get_cache (Dml_art, {"artnr": [(eq, t_l_artikel.artnr)]})

            if dml_art:
                str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by DML", lvcarea, "")
                delete_it = False

                return generate_output()

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == t_l_artikel.artnr)).first()

            if reslin_queasy:
                str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by DML", lvcarea, "")
                delete_it = False

                return generate_output()

            dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, t_l_artikel.artnr)]})

            if dml_artdep:
                str_msg = "Unable to delete " + to_string(t_l_artikel.artnr) + chr_unicode(10) + translateExtended ("Article in used by DML", lvcarea, "")
                delete_it = False

                return generate_output()

    for t_l_artikel in query(t_l_artikel_list, filters=(lambda t_l_artikel: t_l_artikel.is_select  and t_l_artikel.is_delete)):

        for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():

            for l_bestand in db_session.query(L_bestand).filter(
                     (L_bestand.artnr == t_l_artikel.artnr) & (L_bestand.lager_nr == l_lager.lager_nr)).order_by(L_bestand._recid).all():
                db_session.delete(l_bestand)

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == t_l_artikel.artnr)).order_by(L_verbrauch._recid).all():
            db_session.delete(l_verbrauch)

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, t_l_artikel.artnr)]})

        if l_artikel:
            pass
            db_session.delete(l_artikel)
    str_msg = translateExtended ("Article deleted", lvcarea, "")

    return generate_output()