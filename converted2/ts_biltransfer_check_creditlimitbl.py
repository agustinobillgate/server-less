#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy

def ts_biltransfer_check_creditlimitbl(number3:int, mc_num:string):

    prepare_cache ([Htparam, Queasy])

    billdate = None
    frdate = None
    todate = None
    saldo = to_decimal("0.0")
    htparam = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, frdate, todate, saldo, htparam, queasy
        nonlocal number3, mc_num

        return {"billdate": billdate, "frdate": frdate, "todate": todate, "saldo": saldo}

    def check_creditlimit():

        nonlocal billdate, frdate, todate, saldo, htparam, queasy
        nonlocal number3, mc_num

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate
        frdate = date_mdy(get_month(billdate) , 1, get_year(billdate))
        todate = frdate + timedelta(days=31)
        todate = date_mdy(get_month(todate) , 1, get_year(todate)) - timedelta(days=1)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 197) & (Queasy.char1 == (mc_num).lower()) & (Queasy.date1 >= frdate) & (Queasy.date1 <= todate) & (Queasy.number1 == number3)).order_by(Queasy._recid).all():
            saldo =  to_decimal(saldo) + to_decimal(queasy.deci1)


    check_creditlimit()

    return generate_output()