from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Outorder, Zimmer, Queasy

def genoooroom_dailybl(roomnumber:str, userinit:str):
    sysdate:date = None
    htparam = outorder = zimmer = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sysdate, htparam, outorder, zimmer, queasy


        return {}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    sysdate = date_mdy(get_month(htparam.fdate) , get_day(htparam.fdate) , get_year(htparam.fdate))

    for outorder in db_session.query(Outorder).filter(
            (func.lower(Outorder.zinr) == (roomnumber).lower()) &  (Outorder.sysdate >= Outorder.gespstart) &  (Outorder.sysdate <= Outorder.gespende) &  (Outorder.betriebsnr != 2)).all():

        zimmer = db_session.query(Zimmer).filter(
                (outorder.zinr == Zimmer.zinr)).first()
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