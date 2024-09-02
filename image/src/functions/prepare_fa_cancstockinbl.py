from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam

def prepare_fa_cancstockinbl():
    price_decimal = 0
    from_date = None
    to_date = None
    beg_date = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, from_date, to_date, beg_date, htparam


        return {"price_decimal": price_decimal, "from_date": from_date, "to_date": to_date, "beg_date": beg_date}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    from_date = htparam.fdate
    to_date = from_date

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    beg_date = date_mdy(get_month(fdate) , 1, get_year(fdate))

    return generate_output()