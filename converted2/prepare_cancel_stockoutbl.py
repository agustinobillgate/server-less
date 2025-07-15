#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from models import L_untergrup

def prepare_cancel_stockoutbl():
    show_price = False
    avail_l_untergrup = False
    l_untergrup = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, avail_l_untergrup, l_untergrup

        return {"show_price": show_price, "avail_l_untergrup": avail_l_untergrup}

    show_price = get_output(htplogic(43))

    l_untergrup = get_cache (L_untergrup, {"betriebsnr": [(eq, 1)]})

    if l_untergrup:
        avail_l_untergrup = True

    return generate_output()