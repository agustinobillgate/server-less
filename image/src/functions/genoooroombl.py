from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Outorder, Zimmer, Bediener, Queasy

def genoooroombl(zinr:str):
    sysdate:date = None
    htparam = outorder = zimmer = bediener = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sysdate, htparam, outorder, zimmer, bediener, queasy


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    sysdate = date_mdy(get_month(htparam.fdate) , get_day(htparam.fdate) , get_year(htparam.fdate))

    for outorder in db_session.query(Outorder).filter(
            (func.lower(Outorder.(zinr).lower()) == (zinr).lower()) &  (Outorder.gespende < sysdate) &  (Outorder.betriebsnr != 2)).all():

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == outorder.zinr)).first()

        if zimmer:

            if num_entries(outorder.gespgrund, "$") >= 1:

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == to_int(entry(1, outorder.gespgrund, "$")))).first()
            else:

                bediener = db_session.query(Bediener).filter(
                        (Bediener.nr == zimmer.bediener_nr_stat)).first()

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 900) &  (Queasy.date2 == outorder.gespstart) &  (Queasy.date3 == outorder.gespende) &  (Queasy.char1 == outorder.zinr)).first()

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