#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Queasy, Pricecod, Htparam, Arrangement, Waehrung, Argt_line, Reslin_queasy

def pricecod_rate(resnr:int, reslinnr:int, prcode:string, datum:date, ankunft:date, abreise:date, marknr:int, argtno:int, rmcatno:int, adult:int, child1:int, child2:int, reserve_dec:Decimal, wahrno:int):

    prepare_cache ([Res_line, Pricecod, Htparam, Arrangement, Waehrung, Argt_line, Reslin_queasy])

    rmrate = to_decimal("0.0")
    rate_found = False
    exrate1:Decimal = 1
    ex2:Decimal = 1
    do_it:bool = False
    add_it:bool = False
    ebdisc_found:bool = False
    kbdisc_found:bool = False
    argt_defined:bool = False
    qty:int = 0
    niteno:int = 0
    ci_date:date = None
    fdatum:date = None
    tdatum:date = None
    n:int = 0
    ct:string = ""
    rmocc:Decimal = -1
    res_line = queasy = pricecod = htparam = arrangement = waehrung = argt_line = reslin_queasy = None

    early_discount = kickback_discount = stay_pay = kbuff = ebuff = None

    early_discount_list, Early_discount = create_model("Early_discount", {"disc_rate":Decimal, "min_days":int, "min_stay":int, "max_occ":int})
    kickback_discount_list, Kickback_discount = create_model("Kickback_discount", {"disc_rate":Decimal, "max_days":int, "min_stay":int, "max_occ":int})
    stay_pay_list, Stay_pay = create_model("Stay_pay", {"f_date":date, "t_date":date, "stay":int, "pay":int})

    Kbuff = Kickback_discount
    kbuff_list = kickback_discount_list

    Ebuff = Early_discount
    ebuff_list = early_discount_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmrate, rate_found, exrate1, ex2, do_it, add_it, ebdisc_found, kbdisc_found, argt_defined, qty, niteno, ci_date, fdatum, tdatum, n, ct, rmocc, res_line, queasy, pricecod, htparam, arrangement, waehrung, argt_line, reslin_queasy
        nonlocal resnr, reslinnr, prcode, datum, ankunft, abreise, marknr, argtno, rmcatno, adult, child1, child2, reserve_dec, wahrno
        nonlocal kbuff, ebuff


        nonlocal early_discount, kickback_discount, stay_pay, kbuff, ebuff
        nonlocal early_discount_list, kickback_discount_list, stay_pay_list

        return {"rmrate": rmrate, "rate_found": rate_found}

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if res_line:
        rmrate =  to_decimal(res_line.zipreis)

        if substring(prcode, 0, 1) == ("!").lower() :
            prcode = substring(prcode, 1)
        else:
            ct = res_line.zimmer_wunsch

            if matches(ct,r"*$CODE$*"):
                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                prcode = substring(ct, 0, get_index(ct, ";") - 1)

    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, marknr)]})

    if queasy and queasy.logi3:
        datum = ankunft

    pricecod = get_cache (Pricecod, {"code": [(eq, prcode)],"marknr": [(eq, marknr)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, rmcatno)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)]})

    if not pricecod:

        return generate_output()
    rate_found = True
    rmrate =  to_decimal(pricecod.perspreis[adult - 1] + pricecod.kindpreis[0]) * to_decimal(child1 + pricecod.kindpreis[1]) * to_decimal(child2)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

    if waehrung:
        exrate1 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    if reserve_dec != 0:
        ex2 =  to_decimal(ex2) / to_decimal(reserve_dec)
    else:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, wahrno)]})

        if waehrung:
            ex2 = ( to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit))

    for argt_line in db_session.query(Argt_line).filter(
             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind1) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
        add_it = False

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = adult
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = child1

        elif argt_line.vt_percnt == 2:
            qty = child2

        if qty > 0:

            if argt_line.fakt_modus == 1:
                add_it = True

            elif argt_line.fakt_modus == 2:

                if ankunft >= ci_date:
                    add_it = True

            elif argt_line.fakt_modus == 3:

                if (ankunft + 1) >= ci_date:
                    add_it = True

            elif argt_line.fakt_modus == 4 and get_day(datum) == 1:
                add_it = True

            elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                add_it = True

            elif argt_line.fakt_modus == 6:

                if (ankunft + (argt_line.intervall - 1)) >= ci_date:
                    add_it = True

            if add_it:
                argt_defined = False

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, ""),(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:
                    argt_defined = True

                    if argt_line.vt_percnt == 0:
                        rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                    elif argt_line.vt_percnt == 1:
                        rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                    elif argt_line.vt_percnt == 2:
                        rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)

                if not argt_defined:

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, prcode)],"number1": [(eq, marknr)],"number2": [(eq, argtno)],"reslinnr": [(eq, rmcatno)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:

                        if argt_line.vt_percnt == 0:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                        elif argt_line.vt_percnt == 1:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                        elif argt_line.vt_percnt == 2:
                            rmrate =  to_decimal(rmrate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)
                    else:
                        rmrate =  to_decimal(rmrate) + to_decimal((argt_line.betrag) * to_decimal(qty)) * to_decimal(exrate1) / to_decimal(ex2)

    return generate_output()