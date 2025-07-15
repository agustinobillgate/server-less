#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Paramtext, Htparam, Bediener

def prepare_main_sales_1bl():

    prepare_cache ([Paramtext, Htparam])

    new_contrate = False
    p_223 = False
    p_999 = False
    p_1459 = 0
    pl_1459 = False
    p1109 = False
    htl_city = ""
    curr_htl_city = ""
    new_setup = False
    paramtext = htparam = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_contrate, p_223, p_999, p_1459, pl_1459, p1109, htl_city, curr_htl_city, new_setup, paramtext, htparam, bediener

        return {"new_contrate": new_contrate, "p_223": p_223, "p_999": p_999, "p_1459": p_1459, "pl_1459": pl_1459, "p1109": p1109, "htl_city": htl_city, "curr_htl_city": curr_htl_city, "new_setup": new_setup}


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    curr_htl_city = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})
    p_223 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 999)]})
    p_999 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1459)]})
    p_1459 = htparam.paramgruppe
    pl_1459 = htparam.flogical

    paramtext = get_cache (Paramtext, {"txtnr": [(ge, 203)]})
    htl_city = paramtext.ptexte
    p1109 = get_output(htplogic(1109))

    bediener = db_session.query(Bediener).filter(
             (matches(Bediener.username,"*" + chr_unicode(2) + "*"))).first()

    if bediener:
        new_setup = True


    else:
        new_setup = False

    return generate_output()