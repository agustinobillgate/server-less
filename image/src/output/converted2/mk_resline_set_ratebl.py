#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.ratecode_rate import ratecode_rate
from models import Res_line, Arrangement, Reslin_queasy, Guest_pr, Queasy, Katpreis

reslin_list_list, Reslin_list = create_model_like(Res_line)

def mk_resline_set_ratebl(direct_change:bool, fixed_rate:bool, ebdisc_flag:bool, kbdisc_flag:bool, rate_readonly:bool, gastnr:int, res_mode:string, argt:string, contcode:string, bookdate:date, reslin_list_list:[Reslin_list]):

    prepare_cache ([Arrangement, Reslin_queasy, Katpreis])

    restricted_disc = False
    new_rate = None
    rate_tooltip = "?"
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    res_line = arrangement = reslin_queasy = guest_pr = queasy = katpreis = None

    reslin_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal restricted_disc, new_rate, rate_tooltip, wd_array, res_line, arrangement, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal direct_change, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, gastnr, res_mode, argt, contcode, bookdate


        nonlocal reslin_list

        return {"restricted_disc": restricted_disc, "new_rate": new_rate, "rate_tooltip": rate_tooltip}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal restricted_disc, new_rate, rate_tooltip, wd_array, res_line, arrangement, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal direct_change, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, gastnr, res_mode, argt, contcode, bookdate


        nonlocal reslin_list

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def set_roomrate():

        nonlocal restricted_disc, new_rate, rate_tooltip, wd_array, res_line, arrangement, reslin_queasy, guest_pr, queasy, katpreis
        nonlocal direct_change, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, gastnr, res_mode, argt, contcode, bookdate


        nonlocal reslin_list

        ci_date:date = None
        datum:date = None
        curr_zikatnr:int = 0
        current_rate:Decimal = to_decimal("0.0")
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argt)]})

        if not arrangement:

            return
        ci_date = get_output(htpdate(87))

        reslin_list = query(reslin_list_list, first=True)
        current_rate =  to_decimal(reslin_list.zipreis)
        datum = reslin_list.ankunft

        if res_mode.lower()  == ("inhouse").lower() :
            datum = ci_date

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        if reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0:
            new_rate =  to_decimal("0")

            return

        if fixed_rate:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

            if reslin_queasy:
                new_rate =  to_decimal(reslin_queasy.deci1)
                rate_tooltip = ""

                return

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr)]})

        if guest_pr:

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, reslin_list.reserve_int)]})

            if queasy and queasy.logi3:
                datum = reslin_list.ankunft

            if bookdate != None:
                rate_found, new_rate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + contcode), bookdate, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))
            else:
                rate_found, new_rate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + contcode), ci_date, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

            if rate_found:

                return

        if res_mode.lower()  == ("inhouse").lower() :

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})
        else:

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})

        if katpreis:
            new_rate =  to_decimal(get_rackrate (reslin_list.erwachs , reslin_list.kind1 , reslin_list.kind2))
        else:
            new_rate =  to_decimal("0")

        if not direct_change and not rate_readonly:

            if current_rate != 0 and new_rate == 0:
                new_rate =  to_decimal(current_rate)

    set_roomrate()

    return generate_output()