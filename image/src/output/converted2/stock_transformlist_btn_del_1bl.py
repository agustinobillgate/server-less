#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_bestand, L_verbrauch

def stock_transformlist_btn_del_1bl(t_list_datum:date, t_list_lscheinnr:string):

    prepare_cache ([L_op, L_bestand, L_verbrauch])

    successflag = False
    l_op = l_bestand = l_verbrauch = None

    l_op1 = None

    L_op1 = create_buffer("L_op1",L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, l_op, l_bestand, l_verbrauch
        nonlocal t_list_datum, t_list_lscheinnr
        nonlocal l_op1


        nonlocal l_op1

        return {"successflag": successflag}


    for l_op in db_session.query(L_op).filter(
                 (L_op.datum == t_list_datum) & ((L_op.op_art == 2) | (L_op.op_art == 4)) & (L_op.lscheinnr == (t_list_lscheinnr).lower()) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

        if l_op.op_art == 2:

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, l_op.lager_nr)]})

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)
                pass

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                l_bestand.anz_eingang =  to_decimal(l_bestand.anz_eingang) - to_decimal(l_op.anzahl)
                l_bestand.wert_eingang =  to_decimal(l_bestand.wert_eingang) - to_decimal(l_op.warenwert)
                pass

        elif l_op.op_art == 4:

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, l_op.lager_nr)]})

            if l_bestand:
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(l_op.warenwert)
                pass

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(l_op.anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(l_op.warenwert)
                pass

            l_verbrauch = get_cache (L_verbrauch, {"artnr": [(eq, l_op.artnr)],"datum": [(eq, l_op.datum)]})

            if l_verbrauch:
                l_verbrauch.anz_verbrau =  to_decimal(l_verbrauch.anz_verbrau) - to_decimal(l_op.anzahl)
                l_verbrauch.wert_verbrau =  to_decimal(l_verbrauch.wert_verbrau) - to_decimal(l_op.warenwert)
                pass

        l_op1 = get_cache (L_op, {"_recid": [(eq, l_op._recid)]})

        if l_op1:
            l_op1.loeschflag = 2


            successflag = True


            pass
        else:
            successflag = False

    return generate_output()