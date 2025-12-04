#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_bestand, L_artikel, L_verbrauch

def stock_outlist_del_opbl(str_list_op_recid:int, bediener_nr:int):

    prepare_cache ([L_op, L_bestand, L_artikel, L_verbrauch])

    l_op = l_bestand = l_artikel = l_verbrauch = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_bestand, l_artikel, l_verbrauch
        nonlocal str_list_op_recid, bediener_nr

        return {}

    def del_op():

        nonlocal l_op, l_bestand, l_artikel, l_verbrauch
        nonlocal str_list_op_recid, bediener_nr

        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")

        # l_op = get_cache (L_op, {"_recid": [(eq, str_list_op_recid)]})
        l_op = db_session.query(L_op).filter(
                 (L_op._recid == str_list_op_recid)).with_for_update().first()

        if l_op:
            # pass
            l_op.loeschflag = 2
            l_op.fuellflag = bediener_nr
            # pass
            # pass
            db_session.refresh(l_op, with_for_update=True)

            # l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, 0)]})
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.artnr == l_op.artnr) & (L_bestand.lager_nr == 0)).with_for_update().first()

            if l_bestand:
                # pass
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op.warenwert)
                # pass
                qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                val =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) - to_decimal(l_bestand.wert_ausgang)
                # pass
                db_session.refresh(l_bestand, with_for_update=True)

            if qty != 0:

                # l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})
                l_artikel = db_session.query(L_artikel).filter(
                         (L_artikel.artnr == l_op.artnr)).with_for_update().first()
                # pass
                l_artikel.vk_preis =  to_decimal(val) / to_decimal(qty)
                # pass
                # pass
                db_session.refresh(l_artikel, with_for_update=True)

            # l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, l_op.lager_nr)]})
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.artnr == l_op.artnr) & (L_bestand.lager_nr == l_op.lager_nr)).with_for_update().first()

            if l_bestand:
                # pass
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) - to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) - to_decimal(l_op.warenwert)
                # pass
                # pass
                db_session.refresh(l_bestand, with_for_update=True)

            # l_verbrauch = get_cache (L_verbrauch, {"artnr": [(eq, l_op.artnr)],"datum": [(eq, l_op.datum)]})
            l_verbrauch = db_session.query(L_verbrauch).filter(
                     (L_verbrauch.artnr == l_op.artnr) & (L_verbrauch.datum == l_op.datum)).with_for_update().first()

            if l_verbrauch:
                # pass
                l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) - to_decimal(l_op.anzahl)
                l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) + to_decimal(l_op.warenwert)
                # pass
                # pass
                db_session.refresh(l_verbrauch, with_for_update=True)


    del_op()

    return generate_output()
