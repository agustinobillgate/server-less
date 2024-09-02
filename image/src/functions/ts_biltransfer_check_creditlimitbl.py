from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Queasy

def ts_biltransfer_check_creditlimitbl(number3:int, mc_num:str):
    billdate = None
    frdate = None
    todate = None
    saldo = 0
    htparam = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, frdate, todate, saldo, htparam, queasy


        return {"billdate": billdate, "frdate": frdate, "todate": todate, "saldo": saldo}

    def check_creditlimit():

        nonlocal billdate, frdate, todate, saldo, htparam, queasy

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate
        frdate = date_mdy(get_month(billdate) , 1, get_year(billdate))
        todate = frdate + 31
        todate = date_mdy(get_month(todate) , 1, get_year(todate)) - 1

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 197) &  (func.lower(Queasy.char1) == (mc_num).lower()) &  (Queasy.date1 >= frdate) &  (Queasy.date1 <= todate) &  (Queasy.number1 == number3)).all():
            saldo = saldo + queasy.deci1

    check_creditlimit()

    return generate_output()