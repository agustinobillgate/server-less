from functions.additional_functions import *
import decimal
from models import L_untergrup, Htparam

def prepare_stock_translistbl():
    avail_unter = False
    long_digit = False
    l_untergrup = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_unter, long_digit, l_untergrup, htparam


        return {"avail_unter": avail_unter, "long_digit": long_digit}


    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.betriebsnr == 1)).first()
    avail_unter = None != l_untergrup

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    return generate_output()