#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_bestand, L_artikel

def reorg_monhand_init_onhandbl(art_type:int):

    prepare_cache ([Htparam, L_bestand, L_artikel])

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

    def init_onhand():

        nonlocal main_grp, to_grp, to_date, from_date, htparam, l_bestand, l_artikel
        nonlocal art_type

        l_oh = None
        buf_lart = None
        loopi:int = 0
        L_oh =  create_buffer("L_oh",L_bestand)
        Buf_lart =  create_buffer("Buf_lart",L_artikel)

        l_bestand_obj_list = {}
        l_bestand = L_bestand()
        l_artikel = L_artikel()
        for l_bestand.anz_eingang, l_bestand.wert_eingang, l_bestand.anz_ausgang, l_bestand.wert_ausgang, l_bestand._recid, l_artikel.endkum, l_artikel._recid in db_session.query(L_bestand.anz_eingang, L_bestand.wert_eingang, L_bestand.anz_ausgang, L_bestand.wert_ausgang, L_bestand._recid, L_artikel.endkum, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).order_by(L_bestand._recid).all():
            if l_bestand_obj_list.get(l_bestand._recid):
                continue
            else:
                l_bestand_obj_list[l_bestand._recid] = True

            if l_artikel.endkum >= main_grp and l_artikel.endkum <= to_grp:
                l_bestand.anz_eingang =  to_decimal("0")
                l_bestand.wert_eingang =  to_decimal("0")
                l_bestand.anz_ausgang =  to_decimal("0")
                l_bestand.wert_ausgang =  to_decimal("0")


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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 232)]})
    htparam.flogical = True
    pass

    if art_type <= 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
    init_onhand()

    return generate_output()