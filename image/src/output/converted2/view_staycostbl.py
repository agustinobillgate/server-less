#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from sqlalchemy import func
from models import Reservation, Htparam, Res_line, Arrangement, Guest_pr, Waehrung, Genstat, Reslin_queasy, Queasy, Katpreis, Argt_line, Artikel, Zwkum, Fixleist

def view_staycostbl(pvilanguage:int, resnr:int, reslinnr:int, contcode:string):

    prepare_cache ([Reservation, Htparam, Res_line, Arrangement, Guest_pr, Genstat, Reslin_queasy, Katpreis, Argt_line, Artikel, Fixleist])

    output_list_list = []
    ci_date:date = None
    new_contrate:bool = False
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    bonus_array:List[bool] = create_empty_list(999, False)
    lvcarea:string = "view-staycost"
    reservation = htparam = res_line = arrangement = guest_pr = waehrung = genstat = reslin_queasy = queasy = katpreis = argt_line = artikel = zwkum = fixleist = None

    output_list = argt_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":string, "str1":string})
    argt_list_list, Argt_list = create_model("Argt_list", {"argtnr":int, "argt_artnr":int, "departement":int, "is_charged":int, "period":int, "vt_percnt":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, zwkum, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode


        nonlocal output_list, argt_list
        nonlocal output_list_list, argt_list_list

        return {"output-list": output_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, zwkum, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode


        nonlocal output_list, argt_list
        nonlocal output_list_list, argt_list_list

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def check_bonus():

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, zwkum, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode


        nonlocal output_list, argt_list
        nonlocal output_list_list, argt_list_list

        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        j = 1
        for i in range(1,4 + 1) :
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4


    def cal_revenue():

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, zwkum, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode


        nonlocal output_list, argt_list
        nonlocal output_list_list, argt_list_list

        datum:date = None
        co_date:date = None
        argt_rate:Decimal = to_decimal("0.0")
        argt_rate2:Decimal = to_decimal("0.0")
        rm_rate:Decimal = to_decimal("0.0")
        daily_rate:Decimal = to_decimal("0.0")
        tot_rate:Decimal = to_decimal("0.0")
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
        tmpint:int = 0
        tmpdate:date = None
        w1 = None
        W1 =  create_buffer("W1",Waehrung)
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

        if res_line.abreise > res_line.ankunft:
            co_date = res_line.abreise - timedelta(days=1)
        else:
            co_date = res_line.abreise
        rm_rate =  to_decimal(res_line.zipreis)
        for datum in date_range(res_line.ankunft,co_date) :
            curr_i = curr_i + 1
            bill_date = datum
            argt_rate =  to_decimal("0")
            daily_rate =  to_decimal("0")
            fixcost_rate =  to_decimal("0")
            pax = res_line.erwachs
            fixed_rate = False
            ratecode_qsy = "Undefined"
            argt_rate2 =  to_decimal("0")

            if datum < ci_date:
                rm_rate =  to_decimal(None)

                genstat = get_cache (Genstat, {"datum": [(eq, datum)],"resnr": [(eq, res_line.resnr)],"res_int[0]": [(eq, res_line.reslinnr)]})

                if genstat:
                    rm_rate =  to_decimal(genstat.zipreis)
                    pax = genstat.erwachs

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:

                        if reslin_queasy.char2 != "":
                            ratecode_qsy = reslin_queasy.char2
                        else:
                            ratecode_qsy = "Undefined"

                    arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            if datum >= ci_date or not arrangement:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            if (datum >= ci_date) or rm_rate == None:

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

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

                if not fixed_rate:

                    if not it_exist:

                        if guest_pr:

                            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                            if queasy and queasy.logi3:
                                bill_date = res_line.ankunft

                            if new_contrate:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                            else:
                                rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                                if it_exist:
                                    rate_found = True

                                if not it_exist and bonus_array[curr_i - 1] :
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

                            if bonus_array[curr_i - 1] :
                                rm_rate =  to_decimal("0")
            output_list = Output_list()
            output_list_list.append(output_list)

            str = to_string(datum) + " " + translateExtended ("Roomrate", lvcarea, "") + " = " + trim(to_string(rm_rate, "->>>,>>>,>>9.99")) + " - " + trim(ratecode_qsy)
            tot_rate =  to_decimal(tot_rate) + to_decimal(rm_rate)
            daily_rate =  to_decimal(rm_rate)
            count_break =  to_decimal("0")

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

                            if res_line.ankunft == datum:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == datum:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(datum) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.is_charged == 0), first=True)

                            if not argt_list:
                                argt_list = Argt_list()
                                argt_list_list.append(argt_list)

                                argt_list.argtnr = argt_line.argtnr
                                argt_list.departement = argt_line.departement
                                argt_list.argt_artnr = argt_line.argt_artnr
                                argt_list.vt_percnt = argt_line.vt_percnt
                                argt_list.is_charged = 0
                                argt_list.period = 0

                            if argt_list.period < argt_line.intervall:

                                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                                if reslin_queasy:

                                    if reslin_queasy.date1 <= datum and reslin_queasy.date2 >= datum and (reslin_queasy.date1 + (argt_line.intervall - 1)) >= datum:
                                        add_it = True
                                        argt_list.period = argt_list.period + 1
                                    else:

                                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                                 (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.date1 <= datum) & (Reslin_queasy.date2 >= datum) & ((Reslin_queasy.date1 + (argt_line.intervall - 1)) >= datum)).first()

                                        if reslin_queasy:
                                            add_it = True
                                            argt_list.period = argt_list.period + 1
                                else:

                                    if (res_line.ankunft + (argt_line.intervall - 1)) >= datum:
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
                                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.date1 <= bill_date) & (Reslin_queasy.date2 >= bill_date)).order_by(Reslin_queasy._recid).all():
                                argt_defined = True

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                    zwkum = db_session.query(Zwkum).filter(
                                             (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                    if zwkum:
                                        argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                    else:
                                        argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)
                                argt_rate =  to_decimal(argt_rate) * to_decimal(qty)

                                if argt_rate != 0:
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.flag = 1
                                    c = to_string(qty) + " " + artikel.bezeich
                                    str = to_string(translateExtended (" Incl.", lvcarea, "") , "x(10)") + " " + to_string(c, "x(16)") + " = " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                                    count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if guest_pr and not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                            if reslin_queasy:

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == (contcode).lower()) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (Reslin_queasy.date1 <= bill_date) & (Reslin_queasy.date2 >= bill_date)).order_by(Reslin_queasy._recid).all():
                                    argt_defined = True

                                    if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                        zwkum = db_session.query(Zwkum).filter(
                                                 (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                        if zwkum:
                                            argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                        else:
                                            argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                    else:

                                        if reslin_queasy.deci1 != 0:
                                            argt_rate =  to_decimal(reslin_queasy.deci1)

                                        elif reslin_queasy.deci2 != 0:
                                            argt_rate =  to_decimal(reslin_queasy.deci2)

                                        elif reslin_queasy.deci3 != 0:
                                            argt_rate =  to_decimal(reslin_queasy.deci3)
                                    argt_rate =  to_decimal(argt_rate) * to_decimal(qty)

                                    if argt_rate != 0:
                                        output_list = Output_list()
                                        output_list_list.append(output_list)

                                        output_list.flag = 1
                                        c = to_string(qty) + " " + artikel.bezeich
                                        str = to_string(translateExtended (" Incl.", lvcarea, "") , "x(10)") + " " + to_string(c, "x(16)") + " = " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                                        count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if argt_rate2 > 0:
                            argt_rate2 =  to_decimal(argt_rate2) * to_decimal(qty)
                        else:

                            zwkum = db_session.query(Zwkum).filter(
                                     (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                            if zwkum:
                                argt_rate2 = ( to_decimal(rm_rate) * to_decimal((argt_rate2) / to_decimal(100))) * to_decimal(qty)
                            else:
                                argt_rate2 = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                        if argt_rate == 0:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = 1
                            c = to_string(qty) + " " + artikel.bezeich
                            str = to_string(translateExtended (" Incl.", lvcarea, "") , "x(10)") + " " + to_string(c, "x(16)") + " = " + trim(to_string(argt_rate2, "->>>,>>>,>>9.99"))
                            count_break =  to_decimal(count_break) + to_decimal(argt_rate2)


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

                        if res_line.ankunft == datum:
                            add_it = True

                    elif argt_line.fakt_modus == 3:

                        if (res_line.ankunft + 1) == datum:
                            add_it = True

                    elif argt_line.fakt_modus == 4 and get_day(datum) == 1:
                        add_it = True

                    elif argt_line.fakt_modus == 5 and get_day(datum + 1) == 1:
                        add_it = True

                    elif argt_line.fakt_modus == 6:

                        argt_list = query(argt_list_list, filters=(lambda argt_list: argt_list.argtnr == argt_line.argtnr and argt_list.departement == argt_line.departement and argt_list.argt_artnr == argt_line.argt_artnr and argt_list.vt_percnt == argt_line.vt_percnt and argt_list.is_charged == 1), first=True)

                        if not argt_list:
                            argt_list = Argt_list()
                            argt_list_list.append(argt_list)

                            argt_list.argtnr = argt_line.argtnr
                            argt_list.departement = argt_line.departement
                            argt_list.argt_artnr = argt_line.argt_artnr
                            argt_list.vt_percnt = argt_line.vt_percnt
                            argt_list.is_charged = 1
                            argt_list.period = 0

                        if argt_list.period < argt_line.intervall:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, res_line.abreise)],"date2": [(ge, res_line.ankunft)]})

                            if reslin_queasy:

                                if reslin_queasy.date1 <= bill_date and reslin_queasy.date2 >= bill_date and (reslin_queasy.date1 + (argt_line.intervall - 1)) >= bill_date:
                                    add_it = True
                                    argt_list.period = argt_list.period + 1
                                else:

                                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                                             (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.date1 <= bill_date) & (Reslin_queasy.date2 >= bill_date) & ((Reslin_queasy.date1 + (argt_line.intervall - 1)) >= bill_date)).first()

                                    if reslin_queasy:
                                        add_it = True
                                        argt_list.period = argt_list.period + 1
                            else:

                                if (res_line.ankunft + (argt_line.intervall - 1)) >= bill_date:
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

                                zwkum = db_session.query(Zwkum).filter(
                                         (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                if zwkum:
                                    argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                else:
                                    argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                            else:

                                if reslin_queasy.deci1 != 0:
                                    argt_rate =  to_decimal(reslin_queasy.deci1)

                                elif reslin_queasy.deci2 != 0:
                                    argt_rate =  to_decimal(reslin_queasy.deci2)

                                elif reslin_queasy.deci3 != 0:
                                    argt_rate =  to_decimal(reslin_queasy.deci3)
                            argt_rate =  to_decimal(argt_rate) * to_decimal(qty)

                            if argt_rate != 0:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                str = to_string("", "x(5)") + "Excl. " + to_string(artikel.bezeich, "x(16)") + " = " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                                tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate)
                                fixcost_rate =  to_decimal(fixcost_rate) + to_decimal(argt_rate)

                    if guest_pr and not argt_defined:

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("argt-line").lower()) & (Reslin_queasy.char1 == (contcode).lower()) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (bill_date >= Reslin_queasy.date1) & (bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
                                argt_defined = True

                                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :

                                    zwkum = db_session.query(Zwkum).filter(
                                             (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                                    if zwkum:
                                        argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100") * to_decimal(-1)
                                    else:
                                        argt_rate =  to_decimal(rm_rate) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                                else:

                                    if reslin_queasy.deci1 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci1)

                                    elif reslin_queasy.deci2 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci2)

                                    elif reslin_queasy.deci3 != 0:
                                        argt_rate =  to_decimal(reslin_queasy.deci3)
                                argt_rate =  to_decimal(argt_rate) * to_decimal(qty)

                                if argt_rate != 0:
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    str = to_string("", "x(5)") + "Excl. " + to_string(artikel.bezeich, "x(16)") + " = " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                                    tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate)
                                    fixcost_rate =  to_decimal(fixcost_rate) + to_decimal(argt_rate)

                    if argt_rate2 > 0:
                        argt_rate2 =  to_decimal(argt_rate2) * to_decimal(qty)
                    else:

                        zwkum = db_session.query(Zwkum).filter(
                                 (Zwkum.zknr == artikel.zwkum) & (Zwkum.departement == artikel.departement) & (matches(Zwkum.bezeich,"*DISCOUNT*"))).first()

                        if zwkum:
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal((argt_rate2) / to_decimal(100))) * to_decimal(qty)
                        else:
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal(- to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                    if argt_rate == 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        str = to_string("", "x(5)") + "Excl. " + to_string(artikel.bezeich, "x(16)") + " = " + trim(to_string(argt_rate2, "->>>,>>>,>>9.99"))
                        tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate2)
                        fixcost_rate =  to_decimal(fixcost_rate) + to_decimal(argt_rate2)

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                add_it = False
                argt_rate =  to_decimal("0")

                if fixleist.sequenz == 1:
                    add_it = True

                elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                    if res_line.ankunft == datum:
                        add_it = True

                elif fixleist.sequenz == 4 and get_day(datum) == 1:
                    add_it = True

                elif fixleist.sequenz == 5 and get_day(datum + 1) == 1:
                    add_it = True

                elif fixleist.sequenz == 6:

                    if fixleist.lfakt == None:
                        delta = 0
                    else:
                        delta = fixleist.lfakt - res_line.ankunft

                        if delta < 0:
                            delta = 0
                    start_date = res_line.ankunft + timedelta(days=delta)
                    tmpint = (res_line.abreise - start_date).days

                    if tmpint < fixleist.dekade:
                        start_date = res_line.ankunft
                    tmpint = fixleist.dekade - 1
                    tmpdate = start_date + timedelta(days=tmpint)

                    if datum <= tmpdate:
                        add_it = True

                    if datum < start_date:
                        add_it = False

                if add_it:

                    artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                    argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                if argt_rate != 0:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    str = to_string("", "x(8)") + " " + to_string(artikel.bezeich, "x(16)") + " = " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                    tot_rate =  to_decimal(tot_rate) + to_decimal(argt_rate)
                    fixcost_rate =  to_decimal(fixcost_rate) + to_decimal(argt_rate)

            if count_break != 0:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 2
                str = to_string(translateExtended (" Lodging", lvcarea, "") , "x(11)") + " = " + trim(to_string(daily_rate - count_break, "->>>,>>>,>>9.99"))
            str = str + " Total = " + trim(to_string(daily_rate + fixcost_rate, "->>>,>>>,>>9.99"))
        output_list = Output_list()
        output_list_list.append(output_list)

        str = " " + translateExtended ("Expected total revenue =", lvcarea, "") +\
                " " + trim(to_string(tot_rate, "->,>>>,>>>,>>9.99"))
        str1 = "expected"

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

    if arrangement:
        check_bonus()
    cal_revenue()

    return generate_output()