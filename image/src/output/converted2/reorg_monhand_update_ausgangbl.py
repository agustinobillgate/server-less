#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_op, L_artikel, L_bestand

def reorg_monhand_update_ausgangbl(art_type:int):

    prepare_cache ([Htparam, L_op, L_artikel, L_bestand])

    main_grp:int = 0
    to_grp:int = 0
    to_date:date = None
    from_date:date = None
    htparam = l_op = l_artikel = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, l_bestand
        nonlocal art_type

        return {}

    def update_ausgang():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_op, l_artikel, l_bestand
        nonlocal art_type

        s_artnr:int = 0
        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        transdate:date = None
        curr_lager:int = 0
        bbest = None
        Bbest =  create_buffer("Bbest",L_bestand)
        s_artnr = l_op.artnr
        anzahl =  to_decimal(l_op.anzahl)
        wert =  to_decimal(l_op.warenwert)
        transdate = l_op.datum
        curr_lager = l_op.lager_nr

        if l_op.op_art == 3 or (l_op.op_art == 4):

            l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)],"artnr": [(eq, s_artnr)]})

            if not l_bestand:
                l_bestand = L_bestand()
                db_session.add(l_bestand)

                l_bestand.artnr = s_artnr
                l_bestand.anf_best_dat = transdate
                l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
                l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)


            else:

                bbest = get_cache (L_bestand, {"_recid": [(eq, l_bestand._recid)]})
                bbest.anz_ausgang =  to_decimal(bbest.anz_ausgang) + to_decimal(anzahl)
                bbest.wert_ausgang =  to_decimal(bbest.wert_ausgang) + to_decimal(wert)


                pass
                pass

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

        if not l_bestand:
            l_bestand = L_bestand()
            db_session.add(l_bestand)

            l_bestand.lager_nr = curr_lager
            l_bestand.artnr = s_artnr
            l_bestand.anf_best_dat = transdate
            l_bestand.anz_ausgang =  to_decimal(l_bestand.anz_ausgang) + to_decimal(anzahl)
            l_bestand.wert_ausgang =  to_decimal(l_bestand.wert_ausgang) + to_decimal(wert)


        else:

            bbest = get_cache (L_bestand, {"_recid": [(eq, l_bestand._recid)]})
            bbest.anz_ausgang =  to_decimal(bbest.anz_ausgang) + to_decimal(anzahl)
            bbest.wert_ausgang =  to_decimal(bbest.wert_ausgang) + to_decimal(wert)


            pass
            pass

    if art_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
        main_grp = htparam.finteger
        to_grp = main_grp

    elif art_type == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
        main_grp = htparam.finteger
        to_grp = main_grp

    elif art_type == 3:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
        main_grp = htparam.finteger
        to_grp = 9

    if art_type <= 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    for l_op in db_session.query(L_op).filter(
             ((L_op.op_art == 3) | (L_op.op_art == 4)) & (L_op.loeschflag < 2) & ((L_op.datum >= from_date) & (L_op.datum <= to_date)) & (L_op.pos >= 1) & (L_op.lager_nr > 0)).order_by(L_op.artnr).all():

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

        if l_artikel and l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp:
            update_ausgang()

    return generate_output()