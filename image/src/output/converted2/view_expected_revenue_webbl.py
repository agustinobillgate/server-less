#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from models import Waehrung, Htparam, Reservation, Res_line, Guest_pr, Zimkateg, Arrangement, Reslin_queasy, Queasy, Katpreis, Argt_line, Artikel, Fixleist

def view_expected_revenue_webbl(pvilanguage:int, resno:int):

    prepare_cache ([Htparam, Reservation, Res_line, Guest_pr, Zimkateg, Arrangement, Reslin_queasy, Katpreis, Argt_line, Artikel, Fixleist])

    ci_date = None
    title_str = ""
    t_res_line_list = []
    expectedrev_list_list = []
    new_contrate:bool = False
    bonus_array:List[bool] = create_empty_list(9999, False)
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    zim_wunsch:string = ""
    rsv_name:string = ""
    str_common:string = ""
    tot_rate:Decimal = to_decimal("0.0")
    abreise_date:date = None
    curr_datum:date = None
    datum:date = None
    co_date:date = None
    argt_rate:Decimal = to_decimal("0.0")
    argt_rate2:Decimal = to_decimal("0.0")
    rm_rate:Decimal = to_decimal("0.0")
    daily_rate:Decimal = to_decimal("0.0")
    add_it:bool = False
    c:string = ""
    fixed_rate:bool = False
    argt_defined:bool = False
    delta:int = 0
    start_date:date = None
    qty:int = 0
    it_exist:bool = False
    exrate1:Decimal = 1
    ex2:Decimal = 1
    pax:int = 0
    child1:int = 0
    n:int = 0
    created_date:date = None
    bill_date:date = None
    curr_zikatnr:int = 0
    curr_i:int = 0
    w_day:int = 0
    rack_rate:bool = False
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    rate_found:bool = False
    early_flag:bool = False
    kback_flag:bool = False
    ratecode_qsy:string = ""
    count_break:Decimal = to_decimal("0.0")
    fixcost_rate:Decimal = to_decimal("0.0")
    waehrung = htparam = reservation = res_line = guest_pr = zimkateg = arrangement = reslin_queasy = queasy = katpreis = argt_line = artikel = fixleist = None

    output_list = expectedrev_list = t_res_line = argt_list = w1 = buf_list = buf_out = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "datum":date, "rmtype_no":int, "article_no":int, "dept_no":int, "str_rmtype":string, "str_desc":string, "str_amount":string, "str1":string, "calc_rmrate":Decimal, "calc_argtrate":Decimal, "calc_argtrate2":Decimal, "calc_argtrate_all":Decimal, "calc_qty":Decimal, "calc_fixcost":Decimal, "calc_lodg":Decimal, "calc_totrev":Decimal, "count_break":Decimal}, {"flag": -1, "dept_no": -1})
    expectedrev_list_list, Expectedrev_list = create_model("Expectedrev_list", {"flag":int, "datum":date, "rmtype_no":int, "article_no":int, "dept_no":int, "str_rmtype":string, "str_desc":string, "str_amount":string, "str1":string, "calc_rmrate":Decimal, "calc_argtrate":Decimal, "calc_argtrate2":Decimal, "calc_argtrate_all":Decimal, "calc_qty":Decimal, "calc_fixcost":Decimal, "calc_lodg":Decimal, "calc_totrev":Decimal, "count_break":Decimal}, {"flag": -1, "dept_no": -1})
    t_res_line_list, T_res_line = create_model("T_res_line", {"resnr":int, "reslinnr":int, "name":string, "zinr":string, "ankunft":date, "abreise":date, "contcode":string, "str_argt":string, "ct_code":string, "kurzbez":string, "curr_rmcat":string, "rmcat_bez":string, "bonus_array":[bool,9999], "curr_date":date, "rmcat_no":int})
    argt_list_list, Argt_list = create_model("Argt_list", {"argtnr":int, "argt_artnr":int, "resnr":int, "reslinnr":int, "departement":int, "is_charged":int, "period":int, "vt_percnt":int})

    W1 = create_buffer("W1",Waehrung)
    Buf_list = Output_list
    buf_list_list = output_list_list

    Buf_out = Output_list
    buf_out_list = output_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, title_str, t_res_line_list, expectedrev_list_list, new_contrate, bonus_array, wd_array, zim_wunsch, rsv_name, str_common, tot_rate, abreise_date, curr_datum, datum, co_date, argt_rate, argt_rate2, rm_rate, daily_rate, add_it, c, fixed_rate, argt_defined, delta, start_date, qty, it_exist, exrate1, ex2, pax, child1, n, created_date, bill_date, curr_zikatnr, curr_i, w_day, rack_rate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, ratecode_qsy, count_break, fixcost_rate, waehrung, htparam, reservation, res_line, guest_pr, zimkateg, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resno
        nonlocal w1, buf_list, buf_out


        nonlocal output_list, expectedrev_list, t_res_line, argt_list, w1, buf_list, buf_out
        nonlocal output_list_list, expectedrev_list_list, t_res_line_list, argt_list_list

        return {"ci_date": ci_date, "title_str": title_str, "t-res-line": t_res_line_list, "expectedrev-list": expectedrev_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal ci_date, title_str, t_res_line_list, expectedrev_list_list, new_contrate, bonus_array, wd_array, zim_wunsch, rsv_name, str_common, tot_rate, abreise_date, curr_datum, datum, co_date, argt_rate, argt_rate2, rm_rate, daily_rate, add_it, c, fixed_rate, argt_defined, delta, start_date, qty, it_exist, exrate1, ex2, pax, child1, n, created_date, bill_date, curr_zikatnr, curr_i, w_day, rack_rate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, ratecode_qsy, count_break, fixcost_rate, waehrung, htparam, reservation, res_line, guest_pr, zimkateg, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resno
        nonlocal w1, buf_list, buf_out


        nonlocal output_list, expectedrev_list, t_res_line, argt_list, w1, buf_list, buf_out
        nonlocal output_list_list, expectedrev_list_list, t_res_line_list, argt_list_list

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def check_bonus():

        nonlocal ci_date, title_str, t_res_line_list, expectedrev_list_list, new_contrate, bonus_array, wd_array, zim_wunsch, rsv_name, str_common, tot_rate, abreise_date, curr_datum, datum, co_date, argt_rate, argt_rate2, rm_rate, daily_rate, add_it, c, fixed_rate, argt_defined, delta, start_date, qty, it_exist, exrate1, ex2, pax, child1, created_date, bill_date, curr_zikatnr, curr_i, w_day, rack_rate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, ratecode_qsy, count_break, fixcost_rate, waehrung, htparam, reservation, res_line, guest_pr, zimkateg, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resno
        nonlocal w1, buf_list, buf_out


        nonlocal output_list, expectedrev_list, t_res_line, argt_list, w1, buf_list, buf_out
        nonlocal output_list_list, expectedrev_list_list, t_res_line_list, argt_list_list

        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0

        arrangement_obj_list = {}
        for arrangement in db_session.query(Arrangement).filter(
                 ((Arrangement.arrangement.in_(list(set([t_res_line.str_argt for t_res_line in t_res_line_list])))))).order_by(t_res_line.reslinnr).all():
            if arrangement_obj_list.get(arrangement._recid):
                continue
            else:
                arrangement_obj_list[arrangement._recid] = True

            t_res_line = query(t_res_line_list, (lambda t_res_line: (arrangement.arrangement == t_res_line.str_argt)), first=True)
            j = 1
            for i in range(1,4 + 1) :
                stay = to_int(substring(arrangement.options, j - 1, 2))
                pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

                if (stay - pay) > 0:
                    n = num_bonus + pay + 1
                    for k in range(n,stay + 1) :
                        t_res_line.bonus_array[k - 1] = True
                    num_bonus = stay - pay
                j = j + 4


    def cal_revenue():

        nonlocal ci_date, title_str, t_res_line_list, expectedrev_list_list, new_contrate, bonus_array, wd_array, zim_wunsch, rsv_name, str_common, tot_rate, abreise_date, curr_datum, datum, co_date, argt_rate, argt_rate2, rm_rate, daily_rate, add_it, c, fixed_rate, argt_defined, delta, start_date, qty, it_exist, exrate1, ex2, pax, child1, n, created_date, bill_date, curr_zikatnr, curr_i, w_day, rack_rate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, ratecode_qsy, count_break, fixcost_rate, waehrung, htparam, reservation, res_line, guest_pr, zimkateg, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resno
        nonlocal w1, buf_list, buf_out


        nonlocal output_list, expectedrev_list, t_res_line, argt_list, w1, buf_list, buf_out
        nonlocal output_list_list, expectedrev_list_list, t_res_line_list, argt_list_list


        curr_i = curr_i + 1
        bill_date = t_res_line.curr_date
        argt_rate =  to_decimal("0")
        daily_rate =  to_decimal("0")
        fixcost_rate =  to_decimal("0")
        pax = res_line.erwachs
        fixed_rate = False
        ratecode_qsy = "Undefined"
        argt_rate2 =  to_decimal("0")
        n = 0

        if matches(res_line.zimmer_wunsch,r"*DATE,*"):
            n = get_index(res_line.zimmer_wunsch, "Date,")

        if n > 0:
            c = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
            created_date = date_mdy(to_int(substring(c, 4, 2)) , to_int(substring(c, 6, 2)) , to_int(substring(c, 0, 4)))
        else:
            created_date = reservation.resdat
        ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
        kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr
        rm_rate =  to_decimal(res_line.zipreis)
        daily_rate =  to_decimal(res_line.zipreis)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:
            fixed_rate = True
            rm_rate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.char2 != "":
                ratecode_qsy = reslin_queasy.char2
            else:
                ratecode_qsy = "Undefined"

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            if reslin_queasy.char1 != "":

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_queasy.char1)]})
            rm_rate, it_exist = usr_prog1(t_res_line.curr_date, rm_rate)

        if not fixed_rate:
            rm_rate, it_exist = usr_prog1(t_res_line.curr_date, rm_rate)

            if not it_exist:

                if guest_pr:

                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                    if queasy and queasy.logi3:
                        bill_date = res_line.ankunft

                    if new_contrate:
                        rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, t_res_line.contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                    else:
                        rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                        rm_rate, it_exist = usr_prog2(t_res_line.curr_date, rm_rate)

                        if it_exist:
                            rate_found = True

                        if not it_exist and t_res_line.bonus_array[curr_i - 1] :
                            rm_rate =  to_decimal("0")

                if not rate_found:
                    w_day = wd_array[get_weekday(bill_date) - 1]

                    if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                        rm_rate =  to_decimal(res_line.zipreis)

                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                        if not katpreis:

                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                            rack_rate = True

                    elif rack_rate:

                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                        if not katpreis:

                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                            rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                    if t_res_line.bonus_array[curr_i - 1] :
                        rm_rate =  to_decimal("0")

        output_list = query(output_list_list, filters=(lambda output_list: output_list.datum == t_res_line.curr_date), first=True)

        if not output_list:
            count_break =  to_decimal("0")
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = t_res_line.curr_date
            output_list.str_rmtype = to_string(t_res_line.curr_date)
            output_list.rmtype_no = t_res_line.rmcat_no

            output_list = query(output_list_list, filters=(lambda output_list: output_list.rmtype_no == t_res_line.rmcat_no and output_list.flag == 0 and output_list.datum == t_res_line.curr_date), first=True)

            if not output_list:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 0
                output_list.datum = t_res_line.curr_date
                output_list.rmtype_no = t_res_line.rmcat_no
                output_list.str_rmtype = t_res_line.rmcat_bez


            output_list.str_desc = "Room rate"
            output_list.calc_rmrate =  to_decimal(rm_rate)
            output_list.str_amount = trim(to_string(rm_rate, "->>>,>>>,>>>,>>9.99"))

            if rm_rate != 0:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = pax
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = res_line.kind1

                    elif argt_line.vt_percnt == 2:
                        qty = res_line.kind2

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if res_line.ankunft == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(t_res_line.curr_date) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(t_res_line.curr_date + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.resnr == res_line.resnr and argt_list.reslinnr == res_line.reslinnr and argt_list.is_charged == 0), first=True)

                            if not argt_list:
                                argt_list = Argt_list()
                                argt_list_list.append(argt_list)

                                argt_list.argtnr = argt_line.argtnr
                                argt_list.departement = argt_line.departement
                                argt_list.argt_artnr = argt_line.argt_artnr
                                argt_list.vt_percnt = argt_line.vt_percnt
                                argt_list.is_charged = 0
                                argt_list.period = 0
                                argt_list.resnr = res_line.resnr
                                argt_list.reslinnr = res_line.reslinnr

                            if argt_list.period < argt_line.intervall:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                                if reslin_queasy:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                                    if reslin_queasy:

                                        if (reslin_queasy.date1 + (argt_line.intervall - 1)) >= curr_date:
                                            add_it = True
                                            argt_list.period = argt_list.period + 1
                                else:

                                    if (res_line.ankunft + (argt_line.intervall - 1)) >= curr_date:
                                        add_it = True
                                        argt_list.period = argt_list.period + 1

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        argt_rate =  to_decimal("0")
                        argt_rate2 =  to_decimal(argt_line.betrag)
                        argt_defined = False

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                argt_defined = True

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                                    argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                if argt_rate > 0:
                                    argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                else:
                                    argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                if argt_rate != 0:
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.flag = 1
                                    output_list.datum = t_res_line.curr_date
                                    output_list.article_no = artikel.artnr
                                    output_list.dept_no = artikel.departement
                                    output_list.rmtype_no = t_res_line.rmcat_no
                                    output_list.calc_qty =  to_decimal(qty)
                                    str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                    output_list.str_desc = "Incl." + " " + str_common
                                    output_list.calc_argtrate_all =  to_decimal(argt_rate)
                                    output_list.str_amount = trim(to_string(argt_rate, "->>>,>>>,>>>,>>9.99"))
                                    output_list.calc_argtrate =  to_decimal(argt_rate)
                                    count_break =  to_decimal(argt_rate)

                        if guest_pr and not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                    argt_defined = True

                                    if argt_line.vt_percnt == 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif argt_line.vt_percnt == 1:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif argt_line.vt_percnt == 2:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                    if argt_rate > 0:
                                        argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                    else:
                                        argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                    if argt_rate != 0:
                                        output_list = Output_list()
                                        output_list_list.append(output_list)

                                        output_list.flag = 1
                                        output_list.datum = t_res_line.curr_date
                                        output_list.article_no = artikel.artnr
                                        output_list.dept_no = artikel.departement
                                        output_list.rmtype_no = t_res_line.rmcat_no
                                        output_list.calc_qty =  to_decimal(qty)
                                        str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                        output_list.str_desc = "Incl." + " " + str_common
                                        output_list.calc_argtrate_all =  to_decimal(argt_rate)
                                        output_list.str_amount = trim(to_string(argt_rate, "->>>,>>>,>>>,>>9.99"))
                                        output_list.calc_argtrate =  to_decimal(argt_rate)
                                        count_break =  to_decimal(argt_rate)

                        if argt_rate2 > 0:
                            argt_rate2 =  to_decimal(argt_rate2) * to_decimal(qty)
                        else:
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                        if argt_rate2 != 0 and argt_rate == 0:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = 1
                            output_list.datum = t_res_line.curr_date
                            output_list.article_no = artikel.artnr
                            output_list.dept_no = artikel.departement
                            output_list.rmtype_no = t_res_line.rmcat_no
                            output_list.calc_qty =  to_decimal(qty)
                            str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                            output_list.str_desc = "Incl." + " " + str_common
                            output_list.calc_argtrate_all =  to_decimal(argt_rate2)
                            output_list.str_amount = trim(to_string(argt_rate2, "->>>,>>>,>>>,>>9.99"))
                            output_list.calc_argtrate2 =  to_decimal(argt_rate2)
                            count_break =  to_decimal(argt_rate2)
                            output_list.count_break =  to_decimal(argt_rate2)

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & (Argt_line.kind2)).order_by(Argt_line._recid).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = pax
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = res_line.kind1

                    elif argt_line.vt_percnt == 2:
                        qty = res_line.kind2

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if res_line.ankunft == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(t_res_line.curr_date) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(t_res_line.curr_date + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.resnr == res_line.resnr and argt_list.reslinnr == res_line.reslinnr and argt_list.is_charged == 1), first=True)

                            if not argt_list:
                                argt_list = Argt_list()
                                argt_list_list.append(argt_list)

                                argt_list.argtnr = argt_line.argtnr
                                argt_list.departement = argt_line.departement
                                argt_list.argt_artnr = argt_line.argt_artnr
                                argt_list.vt_percnt = argt_line.vt_percnt
                                argt_list.is_charged = 1
                                argt_list.period = 0
                                argt_list.resnr = res_line.resnr
                                argt_list.reslinnr = res_line.reslinnr

                            if argt_list.period < argt_line.intervall:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                                if reslin_queasy:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                                    if reslin_queasy:

                                        if (reslin_queasy.date1 + (argt_line.intervall - 1)) >= curr_date:
                                            add_it = True
                                            argt_list.period = argt_list.period + 1
                                else:

                                    if (res_line.ankunft + (argt_line.intervall - 1)) >= curr_date:
                                        add_it = True
                                        argt_list.period = argt_list.period + 1

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        argt_rate =  to_decimal("0")
                        argt_rate2 =  to_decimal(argt_line.betrag)
                        argt_defined = False

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                argt_defined = True

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                                    argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                if argt_rate > 0:
                                    argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                else:
                                    argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                if argt_rate != 0:
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.flag = 3
                                    output_list.datum = t_res_line.curr_date
                                    output_list.article_no = artikel.artnr
                                    output_list.dept_no = artikel.departement
                                    output_list.rmtype_no = t_res_line.rmcat_no
                                    output_list.calc_qty =  to_decimal(qty)
                                    str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                    output_list.str_desc = "Excl." + " " + str_common
                                    output_list.str_amount = trim(to_string(argt_rate, "->>>,>>>,>>>,>>9.99"))
                                    output_list.calc_argtrate =  to_decimal(argt_rate)
                                    count_break =  to_decimal(argt_rate)

                        if guest_pr and not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                    argt_defined = True

                                    if argt_line.vt_percnt == 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif argt_line.vt_percnt == 1:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif argt_line.vt_percnt == 2:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                    if argt_rate > 0:
                                        argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                    else:
                                        argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                    if argt_rate != 0:
                                        output_list = Output_list()
                                        output_list_list.append(output_list)

                                        output_list.flag = 3
                                        output_list.datum = t_res_line.curr_date
                                        output_list.article_no = artikel.artnr
                                        output_list.dept_no = artikel.departement
                                        output_list.rmtype_no = t_res_line.rmcat_no
                                        output_list.calc_qty =  to_decimal(qty)
                                        str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                        output_list.str_desc = "Excl." + " " + str_common
                                        output_list.str_amount = trim(to_string(argt_rate, "->>>,>>>,>>>,>>9.99"))
                                        output_list.calc_argtrate =  to_decimal(argt_rate)
                                        count_break =  to_decimal(argt_rate)

                        if argt_rate2 > 0:
                            argt_rate2 =  to_decimal(argt_rate2) * to_decimal(qty)
                        else:
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                        if argt_rate2 != 0 and argt_rate == 0:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = 3
                            output_list.datum = t_res_line.curr_date
                            output_list.article_no = artikel.artnr
                            output_list.dept_no = artikel.departement
                            output_list.rmtype_no = t_res_line.rmcat_no
                            output_list.calc_qty =  to_decimal(qty)
                            str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                            output_list.str_desc = "Excl." + " " + str_common
                            output_list.str_amount = trim(to_string(argt_rate2, "->>>,>>>,>>>,>>9.99"))
                            output_list.calc_argtrate2 =  to_decimal(argt_rate2)
                            count_break =  to_decimal(argt_rate2)
                            output_list.count_break =  to_decimal(argt_rate2)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                    add_it = False
                    argt_rate =  to_decimal("0")

                    if fixleist.sequenz == 1:
                        add_it = True

                    elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                        if res_line.ankunft == t_res_line.curr_date:
                            add_it = True

                    elif fixleist.sequenz == 4 and get_day(t_res_line.curr_date) == 1:
                        add_it = True

                    elif fixleist.sequenz == 5 and get_day(t_res_line.curr_date + 1) == 1:
                        add_it = True

                    elif fixleist.sequenz == 6:

                        if fixleist.lfakt == None:
                            delta = 0
                        else:
                            delta = fixleist.lfakt - res_line.ankunft

                            if delta < 0:
                                delta = 0
                        start_date = res_line.ankunft + timedelta(days=delta)

                        if (res_line.abreise - start_date) < fixleist.dekade:
                            start_date = res_line.ankunft

                        if t_res_line.curr_date <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                            add_it = True

                        if t_res_line.curr_date < start_date:
                            add_it = False

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                        argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                    if argt_rate != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.flag = 3
                        output_list.datum = t_res_line.curr_date
                        output_list.article_no = artikel.artnr
                        output_list.dept_no = artikel.departement
                        output_list.str_desc = artikel.bezeich
                        output_list.rmtype_no = t_res_line.rmcat_no
                        output_list.str_amount = trim(to_string(argt_rate, "->>>,>>>,>>>,>>9.99"))
                        output_list.calc_fixcost =  to_decimal(argt_rate)
                        tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate)
                        fixcost_rate =  to_decimal(fixcost_rate) + to_decimal(argt_rate)
        else:

            output_list = query(output_list_list, filters=(lambda output_list: output_list.rmtype_no == t_res_line.rmcat_no and output_list.flag == 0 and output_list.datum == t_res_line.curr_date), first=True)

            if not output_list:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 0
                output_list.datum = t_res_line.curr_date
                output_list.rmtype_no = t_res_line.rmcat_no
                output_list.str_rmtype = t_res_line.rmcat_bez


            output_list.str_desc = "Room rate"
            output_list.calc_rmrate =  to_decimal(output_list.calc_rmrate) + to_decimal(rm_rate)
            output_list.str_amount = trim(to_string(output_list.calc_rmrate, "->>>,>>>,>>>,>>9.99"))

            if rm_rate != 0:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = pax
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = res_line.kind1

                    elif argt_line.vt_percnt == 2:
                        qty = res_line.kind2

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if res_line.ankunft == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(t_res_line.curr_date) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(t_res_line.curr_date + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.resnr == res_line.resnr and argt_list.reslinnr == res_line.reslinnr and argt_list.is_charged == 0), first=True)

                            if not argt_list:
                                argt_list = Argt_list()
                                argt_list_list.append(argt_list)

                                argt_list.argtnr = argt_line.argtnr
                                argt_list.departement = argt_line.departement
                                argt_list.argt_artnr = argt_line.argt_artnr
                                argt_list.vt_percnt = argt_line.vt_percnt
                                argt_list.is_charged = 0
                                argt_list.period = 0
                                argt_list.resnr = res_line.resnr
                                argt_list.reslinnr = res_line.reslinnr

                            if argt_list.period < argt_line.intervall:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                                if reslin_queasy:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                                    if reslin_queasy:

                                        if (reslin_queasy.date1 + (argt_line.intervall - 1)) >= curr_date:
                                            add_it = True
                                            argt_list.period = argt_list.period + 1
                                else:

                                    if (res_line.ankunft + (argt_line.intervall - 1)) >= curr_date:
                                        add_it = True
                                        argt_list.period = argt_list.period + 1

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        argt_rate =  to_decimal("0")
                        argt_rate2 =  to_decimal(argt_line.betrag)
                        argt_defined = False

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                argt_defined = True

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                                    argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                if argt_rate > 0:
                                    argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                else:
                                    argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                if argt_rate != 0:

                                    output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 1 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                                    if not output_list:
                                        output_list = Output_list()
                                        output_list_list.append(output_list)

                                        output_list.flag = 1
                                        output_list.article_no = artikel.artnr
                                        output_list.dept_no = artikel.departement
                                        output_list.datum = t_res_line.curr_date
                                        output_list.rmtype_no = t_res_line.rmcat_no
                                    output_list.calc_qty =  to_decimal(output_list.calc_qty) + to_decimal(qty)
                                    str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                    output_list.str_desc = "Incl." + " " + str_common
                                    output_list.calc_argtrate =  to_decimal(output_list.calc_argtrate) + to_decimal(argt_rate)
                                    output_list.calc_argtrate_all =  to_decimal(output_list.calc_argtrate_all) + to_decimal(argt_rate)
                                    output_list.str_amount = trim(to_string(output_list.calc_argtrate, "->>>,>>>,>>>,>>9.99"))
                                    count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if guest_pr and not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                    argt_defined = True

                                    if argt_line.vt_percnt == 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif argt_line.vt_percnt == 1:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif argt_line.vt_percnt == 2:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                    if argt_rate > 0:
                                        argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                    else:
                                        argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                    if argt_rate != 0:

                                        output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 1 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                                        if not output_list:
                                            output_list = Output_list()
                                            output_list_list.append(output_list)

                                            output_list.flag = 1
                                            output_list.article_no = artikel.artnr
                                            output_list.dept_no = artikel.departement
                                            output_list.datum = t_res_line.curr_date
                                            output_list.rmtype_no = t_res_line.rmcat_no
                                        output_list.calc_qty =  to_decimal(output_list.calc_qty) + to_decimal(qty)
                                        str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                        output_list.str_desc = "Incl." + " " + str_common
                                        output_list.calc_argtrate =  to_decimal(output_list.calc_argtrate) + to_decimal(argt_rate)
                                        output_list.calc_argtrate_all =  to_decimal(output_list.calc_argtrate_all) + to_decimal(argt_rate)
                                        output_list.str_amount = trim(to_string(output_list.calc_argtrate, "->>>,>>>,>>>,>>9.99"))
                                        count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if argt_rate2 > 0:
                            argt_rate2 =  to_decimal(argt_rate2) * to_decimal(qty)
                        else:
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                        if argt_rate2 != 0 and argt_rate == 0:

                            output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 1 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                            if not output_list:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.flag = 1
                                output_list.article_no = artikel.artnr
                                output_list.dept_no = artikel.departement
                                output_list.datum = t_res_line.curr_date
                                output_list.rmtype_no = t_res_line.rmcat_no
                            output_list.calc_qty =  to_decimal(output_list.calc_qty) + to_decimal(qty)
                            str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                            output_list.str_desc = "Incl." + " " + str_common
                            output_list.calc_argtrate2 =  to_decimal(output_list.calc_argtrate2) + to_decimal(argt_rate2)
                            output_list.calc_argtrate_all =  to_decimal(output_list.calc_argtrate_all) + to_decimal(argt_rate2)
                            output_list.str_amount = trim(to_string(output_list.calc_argtrate2, "->>>,>>>,>>>,>>9.99"))
                            count_break =  to_decimal(count_break) + to_decimal(argt_rate2)
                            output_list.count_break =  to_decimal(output_list.count_break) + to_decimal(argt_rate2)
                        output_list.str_amount = trim(to_string(output_list.calc_argtrate_all, "->>>,>>>,>>>,>>9.99"))

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & (Argt_line.kind2)).order_by(Argt_line._recid).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = pax
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = res_line.kind1

                    elif argt_line.vt_percnt == 2:
                        qty = res_line.kind2

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if res_line.ankunft == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == t_res_line.curr_date:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(t_res_line.curr_date) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(t_res_line.curr_date + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.resnr == res_line.resnr and argt_list.reslinnr == res_line.reslinnr and argt_list.is_charged == 1), first=True)

                            if not argt_list:
                                argt_list = Argt_list()
                                argt_list_list.append(argt_list)

                                argt_list.argtnr = argt_line.argtnr
                                argt_list.departement = argt_line.departement
                                argt_list.argt_artnr = argt_line.argt_artnr
                                argt_list.vt_percnt = argt_line.vt_percnt
                                argt_list.is_charged = 1
                                argt_list.period = 0
                                argt_list.resnr = res_line.resnr
                                argt_list.reslinnr = res_line.reslinnr

                            if argt_list.period < argt_line.intervall:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                                if reslin_queasy:

                                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                                    if reslin_queasy:

                                        if (reslin_queasy.date1 + (argt_line.intervall - 1)) >= curr_date:
                                            add_it = True
                                            argt_list.period = argt_list.period + 1
                                else:

                                    if (res_line.ankunft + (argt_line.intervall - 1)) >= curr_date:
                                        add_it = True
                                        argt_list.period = argt_list.period + 1

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                        argt_rate =  to_decimal("0")
                        argt_rate2 =  to_decimal(argt_line.betrag)
                        argt_defined = False

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                argt_defined = True

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                                    argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                if argt_rate > 0:
                                    argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                else:
                                    argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                if argt_rate != 0:

                                    output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 1 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                                    if not output_list:
                                        output_list = Output_list()
                                        output_list_list.append(output_list)

                                        output_list.flag = 3
                                        output_list.article_no = artikel.artnr
                                        output_list.dept_no = artikel.departement
                                        output_list.datum = t_res_line.curr_date
                                        output_list.rmtype_no = t_res_line.rmcat_no
                                    output_list.calc_qty =  to_decimal(output_list.calc_qty) + to_decimal(qty)
                                    str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                    output_list.str_desc = "Excl." + " " + str_common
                                    output_list.calc_argtrate =  to_decimal(output_list.calc_argtrate) + to_decimal(argt_rate)
                                    output_list.str_amount = trim(to_string(output_list.calc_argtrate, "->>>,>>>,>>>,>>9.99"))
                                    count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if guest_pr and not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                    argt_defined = True

                                    if argt_line.vt_percnt == 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif argt_line.vt_percnt == 1:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif argt_line.vt_percnt == 2:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)

                                    if argt_rate > 0:
                                        argt_rate =  to_decimal(argt_rate) * to_decimal(qty)
                                    else:
                                        argt_rate = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                    if argt_rate != 0:

                                        output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 1 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                                        if not output_list:
                                            output_list = Output_list()
                                            output_list_list.append(output_list)

                                            output_list.flag = 3
                                            output_list.article_no = artikel.artnr
                                            output_list.dept_no = artikel.departement
                                            output_list.datum = t_res_line.curr_date
                                            output_list.rmtype_no = t_res_line.rmcat_no
                                        output_list.calc_qty =  to_decimal(output_list.calc_qty) + to_decimal(qty)
                                        str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                                        output_list.str_desc = "Excl." + " " + str_common
                                        output_list.calc_argtrate =  to_decimal(output_list.calc_argtrate) + to_decimal(argt_rate)
                                        output_list.str_amount = trim(to_string(output_list.calc_argtrate, "->>>,>>>,>>>,>>9.99"))
                                        count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if argt_rate2 > 0:
                            argt_rate2 =  to_decimal(argt_rate2) * to_decimal(qty)
                        else:
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                        if argt_rate2 != 0 and argt_rate == 0:

                            output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 1 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                            if not output_list:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.flag = 3
                                output_list.article_no = artikel.artnr
                                output_list.dept_no = artikel.departement
                                output_list.datum = t_res_line.curr_date
                                output_list.rmtype_no = t_res_line.rmcat_no
                            output_list.calc_qty =  to_decimal(output_list.calc_qty) + to_decimal(qty)
                            str_common = to_string(output_list.calc_qty) + " " + artikel.bezeich
                            output_list.str_desc = "Excl." + " " + str_common
                            output_list.calc_argtrate2 =  to_decimal(output_list.calc_argtrate2) + to_decimal(argt_rate2)
                            output_list.str_amount = trim(to_string(output_list.calc_argtrate2, "->>>,>>>,>>>,>>9.99"))
                            count_break =  to_decimal(count_break) + to_decimal(argt_rate2)
                            output_list.count_break =  to_decimal(output_list.count_break) + to_decimal(argt_rate2)

                for fixleist in db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                    add_it = False
                    argt_rate =  to_decimal("0")

                    if fixleist.sequenz == 1:
                        add_it = True

                    elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                        if res_line.ankunft == t_res_line.curr_date:
                            add_it = True

                    elif fixleist.sequenz == 4 and get_day(t_res_line.curr_date) == 1:
                        add_it = True

                    elif fixleist.sequenz == 5 and get_day(t_res_line.curr_date + 1) == 1:
                        add_it = True

                    elif fixleist.sequenz == 6:

                        if fixleist.lfakt == None:
                            delta = 0
                        else:
                            delta = fixleist.lfakt - res_line.ankunft

                            if delta < 0:
                                delta = 0
                        start_date = res_line.ankunft + timedelta(days=delta)

                        if (res_line.abreise - start_date) < fixleist.dekade:
                            start_date = res_line.ankunft

                        if t_res_line.curr_date <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                            add_it = True

                        if t_res_line.curr_date < start_date:
                            add_it = False

                    if add_it:

                        artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                        argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                    if argt_rate != 0:

                        output_list = query(output_list_list, filters=(lambda output_list: output_list.flag == 2 and output_list.article_no == artikel.artnr and output_list.dept_no == artikel.departement and output_list.datum == t_res_line.curr_date and output_list.rmtype_no == t_res_line.rmcat_no), first=True)

                        if not output_list:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = 3
                            output_list.article_no = artikel.artnr
                            output_list.dept_no = artikel.departement
                            output_list.str_desc = artikel.bezeich
                            output_list.datum = t_res_line.curr_date
                            output_list.rmtype_no = t_res_line.rmcat_no
                        output_list.calc_fixcost =  to_decimal(output_list.calc_fixcost) + to_decimal(argt_rate)
                        output_list.str_amount = trim(to_string(output_list.calc_fixcost, "->>>,>>>,>>>,>>9.99"))
                        tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate)
                        fixcost_rate =  to_decimal(fixcost_rate) + to_decimal(argt_rate)


    def usr_prog1(bill_date:date, roomrate:Decimal):

        nonlocal ci_date, title_str, t_res_line_list, expectedrev_list_list, new_contrate, bonus_array, wd_array, zim_wunsch, rsv_name, str_common, tot_rate, abreise_date, curr_datum, datum, co_date, argt_rate, argt_rate2, rm_rate, daily_rate, add_it, c, fixed_rate, argt_defined, delta, start_date, qty, it_exist, exrate1, ex2, pax, child1, n, created_date, curr_zikatnr, curr_i, w_day, rack_rate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, ratecode_qsy, count_break, fixcost_rate, waehrung, htparam, reservation, res_line, guest_pr, zimkateg, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resno
        nonlocal w1, buf_list, buf_out


        nonlocal output_list, expectedrev_list, t_res_line, argt_list, w1, buf_list, buf_out
        nonlocal output_list_list, expectedrev_list_list, t_res_line_list, argt_list_list

        it_exist = False
        prog_str:string = ""
        i:int = 0

        def generate_inner_output():
            return (roomrate, it_exist)


        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "rate-prog")],"number1": [(eq, resnr)],"number2": [(eq, 0)],"char1": [(eq, "")],"reslinnr": [(eq, 1)]})

        if reslin_queasy:
            prog_str = reslin_queasy.char3

        if prog_str != "":
            pass

        return generate_inner_output()


    def usr_prog2(bill_date:date, roomrate:Decimal):

        nonlocal ci_date, title_str, t_res_line_list, expectedrev_list_list, new_contrate, bonus_array, wd_array, zim_wunsch, rsv_name, str_common, tot_rate, abreise_date, curr_datum, datum, co_date, argt_rate, argt_rate2, rm_rate, daily_rate, add_it, c, fixed_rate, argt_defined, delta, start_date, qty, it_exist, exrate1, ex2, pax, child1, n, created_date, curr_zikatnr, curr_i, w_day, rack_rate, ebdisc_flag, kbdisc_flag, rate_found, early_flag, kback_flag, ratecode_qsy, count_break, fixcost_rate, waehrung, htparam, reservation, res_line, guest_pr, zimkateg, arrangement, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resno
        nonlocal w1, buf_list, buf_out


        nonlocal output_list, expectedrev_list, t_res_line, argt_list, w1, buf_list, buf_out
        nonlocal output_list_list, expectedrev_list_list, t_res_line_list, argt_list_list

        it_exist = False
        prog_str:string = ""
        i:int = 0

        def generate_inner_output():
            return (roomrate, it_exist)


        return generate_inner_output()


    output_list_list.clear()
    expectedrev_list_list.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam and htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

    if reservation:
        rsv_name = reservation.name

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resno) & (Res_line.resstatus != 99) & (not_ (Res_line.resstatus <= 12) & (Res_line.resstatus >= 9))).order_by(Res_line.reslinnr).all():

        if res_line.abreise > res_line.ankunft:
            abreise_date = res_line.abreise - timedelta(days=1)
        else:
            abreise_date = res_line.abreise
        for curr_datum in date_range(res_line.ankunft,abreise_date) :
            t_res_line = T_res_line()
            t_res_line_list.append(t_res_line)

            t_res_line.name = res_line.name
            t_res_line.zinr = res_line.zinr
            t_res_line.ankunft = res_line.ankunft
            t_res_line.abreise = res_line.abreise
            t_res_line.resnr = res_line.resnr
            t_res_line.reslinnr = res_line.reslinnr
            t_res_line.curr_date = curr_datum
            t_res_line.rmcat_no = res_line.zikatnr

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

            if guest_pr:
                t_res_line.contcode = guest_pr.code
                t_res_line.ct_code = res_line.zimmer_wunsch
                zim_wunsch = res_line.zimmer_wunsch

                if matches(zim_wunsch,r"*$CODE$*"):
                    t_res_line.ct_code = substring(zim_wunsch, get_index(zim_wunsch, "$CODE$") + 6 - 1)
                    t_res_line.contcode = substring(zim_wunsch, 0, get_index(zim_wunsch, ";") - 1)

            if res_line.l_zuordnung[0] != 0:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})

                if zimkateg:
                    t_res_line.curr_rmcat = zimkateg.kurzbez
                    t_res_line.rmcat_bez = zimkateg.bezeichnung

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            if zimkateg:
                t_res_line.kurzbez = zimkateg.kurzbez
                t_res_line.rmcat_bez = zimkateg.bezeichnung

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            if arrangement:
                t_res_line.str_argt = arrangement.arrangement
    title_str = "Expected Room Revenue" + " " + rsv_name
    check_bonus()

    res_line_obj_list = {}
    for res_line, arrangement in db_session.query(Res_line, Arrangement).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).filter(
             ((Res_line.resnr.in_(list(set([t_res_line.resnr for t_res_line in t_res_line_list])))) & (Res_line.reslinnr == t_res_line.reslinnr))).order_by(t_res_line.curr_date, t_res_line.rmcat_no).all():
        if res_line_obj_list.get(res_line._recid):
            continue
        else:
            res_line_obj_list[res_line._recid] = True

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})
        cal_revenue()

    for output_list in query(output_list_list, sort_by=[("datum",False),("rmtype_no",False),("flag",False)]):

        if output_list.flag == 0 or output_list.flag == 1:

            buf_list = query(buf_list_list, filters=(lambda buf_list: buf_list.flag == 2 and buf_list.datum == output_list.datum and buf_list.rmtype_no == output_list.rmtype_no), first=True)

            if not buf_list:
                buf_list = Buf_list()
                buf_list_list.append(buf_list)

                buf_list.flag = 2
                buf_list.str_desc = "Lodging"
                buf_list.datum = output_list.datum
                buf_list.rmtype_no = output_list.rmtype_no
                buf_list.calc_lodg =  to_decimal(to_decimal(output_list.str_amount))
                buf_list.str_amount = trim(to_string(buf_list.calc_lodg, "->>>,>>>,>>>,>>9.99"))
            else:
                buf_list.calc_lodg =  to_decimal(buf_list.calc_lodg) - to_decimal(to_decimal(output_list.str_amount))
                buf_list.str_amount = trim(to_string(buf_list.calc_lodg, "->>>,>>>,>>>,>>9.99"))

    for output_list in query(output_list_list, sort_by=[("datum",False),("rmtype_no",False),("flag",False)]):

        if output_list.flag == 0 or output_list.flag == 3:

            buf_out = query(buf_out_list, filters=(lambda buf_out: buf_out.flag == 4 and buf_out.datum == output_list.datum and buf_out.rmtype_no == output_list.rmtype_no), first=True)

            if not buf_out:
                buf_out = Buf_out()
                buf_out_list.append(buf_out)

                buf_out.flag = 4
                buf_out.str_desc = "Total Revenue"
                buf_out.datum = output_list.datum
                buf_out.rmtype_no = output_list.rmtype_no
                buf_out.calc_totrev =  to_decimal(to_decimal(output_list.str_amount))
                buf_out.str_amount = trim(to_string(buf_out.calc_totrev, "->>>,>>>,>>>,>>9.99"))
            else:
                buf_out.calc_totrev =  to_decimal(buf_out.calc_totrev) + to_decimal(to_decimal(output_list.str_amount))
                buf_out.str_amount = trim(to_string(buf_out.calc_totrev, "->>>,>>>,>>>,>>9.99"))
    tot_rate =  to_decimal("0")

    for output_list in query(output_list_list, filters=(lambda output_list: output_list.flag == 0)):
        tot_rate =  to_decimal(tot_rate) + to_decimal(to_decimal(output_list.str_amount))
    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.flag = 10
    output_list = Output_list()
    output_list_list.append(output_list)

    output_list.flag = 99
    output_list.str_desc = "Expected Total Revenue"
    output_list.str_amount = trim(to_string(tot_rate, "->>>,>>>,>>>,>>9.99"))

    for output_list in query(output_list_list, sort_by=[("datum",False),("rmtype_no",False),("flag",False)]):
        expectedrev_list = Expectedrev_list()
        expectedrev_list_list.append(expectedrev_list)

        buffer_copy(output_list, expectedrev_list)

    return generate_output()