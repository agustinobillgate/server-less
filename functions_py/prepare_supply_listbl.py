#using conversion tools version: 1.0.0.117

#------------------------------------------------
# Rulita, 28/08/2025
# Modify : chg order by filter supplier by liefnr
# Issue Schenario 37
#------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant, Htparam

def prepare_supply_listbl():

    prepare_cache ([Htparam])

    param992 = False
    comments = ""
    first_liefnr = 0
    curr_firma = ""
    supply_list_data = []
    counter:int = 0
    l_lieferant = htparam = None

    supply_list = None

    supply_list_data, Supply_list = create_model_like(L_lieferant, {"t_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal param992, comments, first_liefnr, curr_firma, supply_list_data, counter, l_lieferant, htparam


        nonlocal supply_list
        nonlocal supply_list_data

        return {"param992": param992, "comments": comments, "first_liefnr": first_liefnr, "curr_firma": curr_firma, "supply-list": supply_list_data}

    for l_lieferant in db_session.query(L_lieferant).filter(
            #  (L_lieferant.lief_nr > 0) & (L_lieferant.firma != "")).order_by(L_lieferant.firma).all():
             (L_lieferant.lief_nr > 0) & (L_lieferant.firma != "")).order_by(L_lieferant.lief_nr).all():
        supply_list = Supply_list()
        supply_list_data.append(supply_list)

        buffer_copy(l_lieferant, supply_list)
        supply_list.t_recid = l_lieferant._recid
        curr_firma = l_lieferant.firma
        comments = l_lieferant.notizen[0]

    htparam = get_cache (Htparam, {"paramnr": [(eq, 992)]})
    param992 = htparam.flogical

    return generate_output()