#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Arrangement, Ratecode

def ratecode_compli(resnr:int, reslinnr:int, prcode:string, rmcatno:int, datum:date):

    prepare_cache ([Htparam, Res_line, Arrangement, Ratecode])

    bonus = False
    ct:string = ""
    n:int = 0
    compno:int = 0
    niteno:int = 0
    usedcompliment:int = 0
    paidnite:int = 0
    niteofstay:int = 0
    fdatum:date = None
    tdatum:date = None
    argtno:int = 0
    w_day:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    htparam = res_line = arrangement = ratecode = None

    stay_pay = None

    stay_pay_data, Stay_pay = create_model("Stay_pay", {"startdate":date, "f_date":date, "t_date":date, "stay":int, "pay":int}, {"startdate": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bonus, ct, n, compno, niteno, usedcompliment, paidnite, niteofstay, fdatum, tdatum, argtno, w_day, wd_array, htparam, res_line, arrangement, ratecode
        nonlocal resnr, reslinnr, prcode, rmcatno, datum


        nonlocal stay_pay
        nonlocal stay_pay_data

        return {"bonus": bonus}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 933)]})

    if htparam.feldtyp == 4 and htparam.flogical:

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
    niteofstay = (res_line.abreise - res_line.ankunft).days
    argtno = arrangement.argtnr
    w_day = wd_array[get_weekday(datum - 1) - 1]
    ct = res_line.zimmer_wunsch

    if matches(ct,r"*$CODE$*"):
        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
        prcode = substring(ct, 0, get_index(ct, ";") - 1)

    ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, res_line.erwachs)],"kind1": [(eq, res_line.kind1)],"kind2": [(eq, res_line.kind2)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, res_line.erwachs)],"kind1": [(eq, res_line.kind1)],"kind2": [(eq, res_line.kind2)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, w_day)],"erwachs": [(eq, res_line.erwachs)]})

    if not ratecode:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"wday": [(eq, 0)],"erwachs": [(eq, res_line.erwachs)]})

    if not ratecode:

        return generate_output()

    if datum > res_line.ankunft and (num_entries(ratecode.char1[2], ";") >= 2):
        for n in range(1,num_entries(ratecode.char1[2], ";") - 1 + 1) :
            ct = entry(n - 1, ratecode.char1[2], ";")
            fdatum = date_mdy(to_int(substring(entry(0, ct, ",") , 4, 2)) , to_int(substring(entry(0, ct, ",") , 6, 2)) , to_int(substring(entry(0, ct, ",") , 0, 4)))
            tdatum = date_mdy(to_int(substring(entry(1, ct, ",") , 4, 2)) , to_int(substring(entry(1, ct, ",") , 6, 2)) , to_int(substring(entry(1, ct, ",") , 0, 4)))

            if datum > fdatum and datum <= tdatum:
                stay_pay = Stay_pay()
                stay_pay_data.append(stay_pay)

                stay_pay.f_date = fdatum
                stay_pay.t_date = tdatum
                stay_pay.stay = to_int(entry(2, ct, ","))
                stay_pay.pay = to_int(entry(3, ct, ","))

                if res_line.ankunft < fdatum:
                    stay_pay.startdate = fdatum


                else:
                    stay_pay.startdate = res_line.ankunft

                if stay_pay.stay == stay_pay.pay:
                    stay_pay_data.remove(stay_pay)

    stay_pay = query(stay_pay_data, first=True)

    if not stay_pay:

        return generate_output()

    for stay_pay in query(stay_pay_data, sort_by=[("stay",False)]):
        niteno = (datum - stay_pay.startDate + 1).days
        stay_pay.pay = stay_pay.pay + usedcompliment
        compno = stay_pay.stay - stay_pay.pay

        if stay_pay.stay < niteno:
            usedcompliment = usedcompliment + compno

        elif (niteofstay >= stay_pay.stay) and (niteno > stay_pay.pay):
            bonus = True
            break

    return generate_output()