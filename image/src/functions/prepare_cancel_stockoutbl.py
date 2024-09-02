from functions.additional_functions import *
import decimal
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

    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.betriebsnr == 1)).first()

    if l_untergrup:
        avail_l_untergrup = True

    return generate_output()