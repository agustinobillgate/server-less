#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_bestand, L_artikel

def reorg_monhand_update_averagebl(art_type:int):

    prepare_cache ([Htparam, L_artikel])

    main_grp:int = 0
    to_grp:int = 0
    to_date:date = None
    from_date:date = None
    htparam = l_bestand = l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel
        nonlocal art_type

        return {}

    def update_average():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel
        nonlocal art_type

        tot_anz:Decimal = to_decimal("0.0")
        tot_wert:Decimal = to_decimal("0.0")
        avrg_price:Decimal = to_decimal("0.0")

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, 0)]})
        while None != l_bestand:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})

            if l_artikel and l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp:
                tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) -\
                        l_bestand.anz_ausgang
                tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang) -\
                        l_bestand.wert_ausgang

                if tot_anz == 0:
                    tot_anz =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang)
                    tot_wert =  to_decimal(l_bestand.val_anf_best) + to_decimal(l_bestand.wert_eingang)

                if tot_anz != 0:
                    avrg_price =  to_decimal(tot_wert) / to_decimal(tot_anz)

                    l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_bestand.artnr)]})
                    l_artikel.vk_preis =  to_decimal(avrg_price)
                    pass
                    pass

            curr_recid = l_bestand._recid
            l_bestand = db_session.query(L_bestand).filter(
                     (L_bestand.lager_nr == 0) & (L_bestand._recid > curr_recid)).first()

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
    update_average()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 232)]})
    htparam.flogical = False
    pass

    return generate_output()