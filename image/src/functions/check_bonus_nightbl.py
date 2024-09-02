from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Arrangement, Zimkateg, Ratecode

res_dynarate_list, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":decimal, "rmcat":str, "argt":str, "prcode":str, "rcode":str, "markno":int, "setup":int, "adult":int, "child":int})
def check_bonus_nightbl(ci_date:date, co_date:date, res_dynarate:[Res_dynarate]):
    niteofstay:int = 0
    niteno:int = 0
    compno:int = 0
    usedcompliment:int = 0
    datum:date = None
    fdatum:date = None
    tdatum:date = None
    argtno:int = 0
    rmcatno:int = 0
    w_day:int = 0
    n:int = 0
    prcode:str = ""
    ct:str = ""
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    arrangement = zimkateg = ratecode = None

    res_dynarate = stay_pay = None

    stay_pay_list, Stay_pay = create_model("Stay_pay", {"startdate":date, "f_date":date, "t_date":date, "stay":int, "pay":int}, {"startdate": None})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal niteofstay, niteno, compno, usedcompliment, datum, fdatum, tdatum, argtno, rmcatno, w_day, n, prcode, ct, wd_array, arrangement, zimkateg, ratecode


        nonlocal res_dynarate, stay_pay
        nonlocal stay_pay_list
        global res_dynarate_list
        return {}


    res_dynarate = query(res_dynarate_list, first=True)

    if not res_dynarate:

        return generate_output()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == res_dynarate.argt)).first()

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.kurzbez == res_dynarate.rmCat)).first()
    niteofstay = co_date - ci_date
    argtno = arrangement.argtnr
    rmcatno = zimkateg.zikatnr
    prcode = res_dynarate.rcode

    for res_dynarate in query(res_dynarate_list):
        datum = res_dynarate.date1
        w_day = wd_array[get_weekday(datum - 1) - 1]


        stay_pay_list.clear()

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_dynarate.markNo) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum)).first()

        if ratecode and (num_entries(ratecode.char1[2], ";") >= 2):
            for n in range(1,num_entries(ratecode.char1[2], ";") - 1 + 1) :
                ct = entry(n - 1, ratecode.char1[2], ";")
                fdatum = date_mdy(to_int(substring(entry(0, ct, ",") , 4, 2)) , to_int(substring(entry(0, ct, ",") , 6, 2)) , to_int(substring(entry(0, ct, ",") , 0, 4)))
                tdatum = date_mdy(to_int(substring(entry(1, ct, ",") , 4, 2)) , to_int(substring(entry(1, ct, ",") , 6, 2)) , to_int(substring(entry(1, ct, ",") , 0, 4)))

                if datum > fdatum and datum <= tdatum:
                    stay_pay = Stay_pay()
                    stay_pay_list.append(stay_pay)

                    stay_pay.f_date = fdatum
                    stay_pay.t_date = tdatum
                    stay_pay.stay = to_int(entry(2, ct, ","))
                    stay_pay.pay = to_int(entry(3, ct, ","))

                    if ci_date < fdatum:
                        stay_pay.startDate = fdatum


                    else:
                        stay_pay.startDate = ci_date

                    if stay_pay.stay == stay_pay.pay:
                        stay_pay_list.remove(stay_pay)

            for stay_pay in query(stay_pay_list):
                niteno = datum - stay_pay.startDate + 1
                stay_pay.pay = stay_pay.pay + usedcompliment
                compno = stay_pay.stay - stay_pay.pay

                if stay_pay.stay < niteno:
                    usedcompliment = usedcompliment + compno

                elif (niteofstay >= stay_pay.stay) and (niteno > stay_pay.pay):
                    res_dynarate.rate = 0
                    break

    return generate_output()