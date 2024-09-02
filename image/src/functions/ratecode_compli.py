from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Htparam, Res_line, Arrangement, Ratecode

def ratecode_compli(resnr:int, reslinnr:int, prcode:str, rmcatno:int, datum:date):
    bonus = False
    ct:str = ""
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
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    htparam = res_line = arrangement = ratecode = None

    stay_pay = None

    stay_pay_list, Stay_pay = create_model("Stay_pay", {"startdate":date, "f_date":date, "t_date":date, "stay":int, "pay":int}, {"startdate": None})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bonus, ct, n, compno, niteno, usedcompliment, paidnite, niteofstay, fdatum, tdatum, argtno, w_day, wd_array, htparam, res_line, arrangement, ratecode


        nonlocal stay_pay
        nonlocal stay_pay_list
        return {"bonus": bonus}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 933)).first()

    if htparam.feldtyp == 4 and htparam.flogical:

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == res_line.arrangement)).first()
    niteofstay = res_line.abreise - res_line.ankunft
    argtno = arrangement.argtnr
    w_day = wd_array[get_weekday(datum - 1) - 1]
    ct = res_line.zimmer_wunsch

    if re.match(".*\$CODE\$.*",ct):
        ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
        prcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

    ratecode = db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == res_line.erwachs) &  (Ratecode.kind1 == res_line.kind1) &  (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == res_line.erwachs) &  (Ratecode.kind1 == res_line.kind1) &  (Ratecode.kind2 == res_line.kind2)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == w_day) &  (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.marknr == res_line.reserve_int) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == rmcatno) &  (Ratecode.startperiode <= datum) &  (Ratecode.endperiode >= datum) &  (Ratecode.wday == 0) &  (Ratecode.erwachs == res_line.erwachs)).first()

    if not ratecode:

        return generate_output()

    if datum > res_line.ankunft and (num_entries(ratecode.char1[2], ";") >= 2):
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

                if res_line.ankunft < fdatum:
                    stay_pay.startDate = fdatum


                else:
                    stay_pay.startDate = res_line.ankunft

                if stay_pay.stay == stay_pay.pay:
                    stay_pay_list.remove(stay_pay)

    stay_pay = query(stay_pay_list, first=True)

    if not stay_pay:

        return generate_output()

    for stay_pay in query(stay_pay_list):
        niteno = datum - stay_pay.startDate + 1
        stay_pay.pay = stay_pay.pay + usedcompliment
        compno = stay_pay.stay - stay_pay.pay

        if stay_pay.stay < niteno:
            usedcompliment = usedcompliment + compno

        elif (niteofstay >= stay_pay.stay) and (niteno > stay_pay.pay):
            bonus = True
            break

    return generate_output()