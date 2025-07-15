#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Outorder, Zimmer, Queasy

def genoooroom_dailybl(roomnumber:string, userinit:string):

    prepare_cache ([Htparam, Outorder, Zimmer, Queasy])

    sysdate:date = None
    htparam = outorder = zimmer = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sysdate, htparam, outorder, zimmer, queasy
        nonlocal roomnumber, userinit

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    sysdate = date_mdy(get_month(htparam.fdate) , get_day(htparam.fdate) , get_year(htparam.fdate))

    for outorder in db_session.query(Outorder).filter(
             (Outorder.zinr == (roomnumber).lower()) & (Outorder.gespstart <= sysdate) & (Outorder.gespende >= sysdate) & (Outorder.betriebsnr != 2)).order_by(Outorder._recid).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 900
        queasy.number1 = zimmer.zikatnr
        queasy.char1 = outorder.zinr
        queasy.char2 = outorder.gespgrund
        queasy.char3 = userinit
        queasy.date1 = sysdate
        queasy.date2 = outorder.gespstart
        queasy.date3 = outorder.gespende

    return generate_output()