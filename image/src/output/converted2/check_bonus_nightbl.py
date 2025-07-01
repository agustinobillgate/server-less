#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Arrangement, Zimkateg, Ratecode

res_dynarate_list, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":Decimal, "rmcat":string, "argt":string, "prcode":string, "rcode":string, "markno":int, "setup":int, "adult":int, "child":int})

def check_bonus_nightbl(ci_date:date, co_date:date, res_dynarate_list:[Res_dynarate]):

    prepare_cache ([Arrangement, Zimkateg, Ratecode])

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
    prcode:string = ""
    ct:string = ""
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    arrangement = zimkateg = ratecode = None

    res_dynarate = stay_pay = None

    stay_pay_list, Stay_pay = create_model("Stay_pay", {"startdate":date, "f_date":date, "t_date":date, "stay":int, "pay":int}, {"startdate": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal niteofstay, niteno, compno, usedcompliment, datum, fdatum, tdatum, argtno, rmcatno, w_day, n, prcode, ct, wd_array, arrangement, zimkateg, ratecode
        nonlocal ci_date, co_date


        nonlocal res_dynarate, stay_pay
        nonlocal stay_pay_list

        return {"Res-Dynarate": res_dynarate_list}


    res_dynarate = query(res_dynarate_list, first=True)

    if res_dynarate:
        pass

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_dynarate.argt)]})

        if arrangement:

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, res_dynarate.rmcat)]})

            if zimkateg:
                niteofstay = (co_date - ci_date).days
                argtno = arrangement.argtnr
                rmcatno = zimkateg.zikatnr
                prcode = res_dynarate.rcode

                for res_dynarate in query(res_dynarate_list, sort_by=[("date1",False)]):
                    datum = res_dynarate.date1
                    w_day = wd_array[get_weekday(datum - 1) - 1]


                    stay_pay_list.clear()

                    ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_dynarate.markno)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)]})

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
                                    stay_pay.startdate = fdatum


                                else:
                                    stay_pay.startdate = ci_date

                                if stay_pay.stay == stay_pay.pay:
                                    stay_pay_list.remove(stay_pay)

                        for stay_pay in query(stay_pay_list, sort_by=[("stay",False)]):
                            niteno = (datum - stay_pay.startDate + 1).days
                            stay_pay.pay = stay_pay.pay + usedcompliment
                            compno = stay_pay.stay - stay_pay.pay

                            if stay_pay.stay < niteno:
                                usedcompliment = usedcompliment + compno

                            elif (niteofstay >= stay_pay.stay) and (niteno > stay_pay.pay):
                                res_dynarate.rate =  to_decimal("0")
                                break
        pass
        pass

    return generate_output()