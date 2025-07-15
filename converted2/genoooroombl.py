#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Outorder, Zimmer, Bediener, Queasy

def genoooroombl(zinr:string):

    prepare_cache ([Htparam, Outorder, Zimmer, Bediener, Queasy])

    sysdate:date = None
    htparam = outorder = zimmer = bediener = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sysdate, htparam, outorder, zimmer, bediener, queasy
        nonlocal zinr

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    sysdate = date_mdy(get_month(htparam.fdate) , get_day(htparam.fdate) , get_year(htparam.fdate))

    for outorder in db_session.query(Outorder).filter(
             (Outorder.zinr == (zinr).lower()) & (Outorder.gespende < sysdate) & (Outorder.betriebsnr != 2)).order_by(Outorder._recid).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

        if zimmer:

            if num_entries(outorder.gespgrund, "$") >= 1:

                bediener = get_cache (Bediener, {"nr": [(eq, to_int(entry(1, outorder.gespgrund, "$")))]})
            else:

                bediener = get_cache (Bediener, {"nr": [(eq, zimmer.bediener_nr_stat)]})

            queasy = get_cache (Queasy, {"key": [(eq, 900)],"date2": [(eq, outorder.gespstart)],"date3": [(eq, outorder.gespende)],"char1": [(eq, outorder.zinr)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 900
                queasy.number1 = zimmer.zikatnr
                queasy.char1 = outorder.zinr
                queasy.char2 = outorder.gespgrund
                queasy.date1 = sysdate
                queasy.date2 = outorder.gespstart
                queasy.date3 = outorder.gespende
                queasy.char3 = bediener.userinit

    return generate_output()