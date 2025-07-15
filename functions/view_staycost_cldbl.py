from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from models import Reservation, Htparam, Res_line, Arrangement, Guest_pr, Waehrung, Genstat, Reslin_queasy, Queasy, Katpreis, Argt_line, Artikel, Fixleist

def view_staycost_cldbl(pvilanguage:int, resnr:int, reslinnr:int, contcode:str, repeat_charge:bool):
    output_list_list = []
    ci_date:date = None
    new_contrate:bool = False
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    bonus_array:List[bool] = create_empty_list(999, False)
    periode:date = None
    loopi:date = None
    curr_diff:decimal = to_decimal("0.0")
    lvcarea:str = "view-staycost"
    reservation = htparam = res_line = arrangement = guest_pr = waehrung = genstat = reslin_queasy = queasy = katpreis = argt_line = artikel = fixleist = None

    output_list = periode_list = output_list1 = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":str, "str1":str})
    periode_list_list, Periode_list = create_model("Periode_list", {"counter":int, "periode1":date, "periode2":date, "diff_day":int, "amt_periode":decimal, "tamount":decimal})
    output_list1_list, Output_list1 = create_model("Output_list1", {"datum":date, "rate":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list
        return {"output-list": output_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

        rate:decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def check_bonus():

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

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

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

        datum:date = None
        co_date:date = None
        argt_rate:decimal = to_decimal("0.0")
        argt_rate2:decimal = to_decimal("0.0")
        rm_rate:decimal = to_decimal("0.0")
        daily_rate:decimal = to_decimal("0.0")
        tot_rate:decimal = to_decimal("0.0")
        add_it:bool = False
        c:str = ""
        fixed_rate:bool = False
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        qty:int = 0
        it_exist:bool = False
        exrate1:decimal = 1
        ex2:decimal = 1
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
        ratecode_qsy:str = ""
        count_break:decimal = to_decimal("0.0")
        fixcost_rate:decimal = to_decimal("0.0")
        w1 = None
        W1 =  create_buffer("W1",Waehrung)
        n = 0

        if re.match(r".*DATE,.*",res_line.zimmer_wunsch, re.IGNORECASE):
            n = 1 + get_index(res_line.zimmer_wunsch, "Date,")

        if n > 0:
            c = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
            created_date = date_mdy(to_int(substring(c, 4, 2)) , to_int(substring(c, 6, 2)) , to_int(substring(c, 0, 4)))
        else:
            created_date = reservation.resdat
        ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
        kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

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

                genstat = db_session.query(Genstat).filter(
                         (Genstat.datum == datum) & (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr)).first()

                if genstat:
                    rm_rate =  to_decimal(genstat.zipreis)
                    pax = genstat.erwachs

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == genstat.resnr) & (Reslin_queasy.reslinnr == genstat.res_int[0]) & (Reslin_queasy.datum >= Reslin_queasy.date1) & (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                    if reslin_queasy:

                        if reslin_queasy.char2 != "":
                            ratecode_qsy = reslin_queasy.char2
                        else:
                            ratecode_qsy = "Undefined"

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.arrangement == genstat.argt)).first()

            if datum >= ci_date or not arrangement:

                arrangement = db_session.query(Arrangement).filter(
                         (Arrangement.arrangement == res_line.arrangement)).first()

            if (datum >= ci_date) or rm_rate == None:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.datum >= Reslin_queasy.date1) & (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

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

                        arrangement = db_session.query(Arrangement).filter(
                                 (Arrangement.arrangement == reslin_queasy.char1)).first()
                    rm_rate, it_exist = usr_prog1(datum, rm_rate)

                if not fixed_rate:
                    rm_rate, it_exist = usr_prog1(datum, rm_rate)

                    if not it_exist:

                        if guest_pr:

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 18) & (Queasy.number1 == res_line.reserve_int)).first()

                            if queasy and queasy.logi3:
                                bill_date = res_line.ankunft

                            if new_contrate:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                            else:
                                rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                if it_exist:
                                    rate_found = True

                                if not it_exist and bonus_array[curr_i - 1] :
                                    rm_rate =  to_decimal("0")

                        if not rate_found:
                            w_day = wd_array[get_weekday(bill_date) - 1]

                            if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                rm_rate =  to_decimal(res_line.zipreis)

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                                if not katpreis:

                                    katpreis = db_session.query(Katpreis).filter(
                                             (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                                if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                    rack_rate = True

                            elif rack_rate:

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                                if not katpreis:

                                    katpreis = db_session.query(Katpreis).filter(
                                             (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                                if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                    rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                            if bonus_array[curr_i - 1] :
                                rm_rate =  to_decimal("0")
            output_list = Output_list()
            output_list_list.append(output_list)

            str = to_string(datum) + " " + translateExtended ("roomrate", lvcarea, "") + " = " + trim(to_string(rm_rate, "->>>,>>>,>>9.99")) + " - " + trim(ratecode_qsy)
            tot_rate =  to_decimal(tot_rate) + to_decimal(rm_rate)
            daily_rate =  to_decimal(rm_rate)
            count_break =  to_decimal("0")

            if rm_rate != 0:

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & (not Argt_line.kind2)).order_by(Argt_line._recid).all():
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

                            if (res_line.ankunft + (argt_line.intervall - 1)) >= datum:
                                add_it = True

                    if add_it:

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == argt_line.argt_artnr) & (Artikel.departement == argt_line.departement)).first()
                        argt_rate =  to_decimal("0")
                        argt_rate2 =  to_decimal(argt_line.betrag)
                        argt_defined = False

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                 (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

                        if reslin_queasy:

                            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                     (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.number1 == argt_line.departement) & (Reslin_queasy.number2 == argt_line.argtnr) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
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
                                    argt_rate = ( to_decimal(rm_rate) * to_decimal(() - to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

                                if argt_rate != 0:
                                    output_list = Output_list()
                                    output_list_list.append(output_list)

                                    output_list.flag = 1
                                    c = to_string(qty) + " " + artikel.bezeich
                                    str = to_string(translateExtended (" Incl.", lvcarea, "") , "x(10)") + " " + to_string(c, "x(16)") + " = " + trim(to_string(argt_rate, "->>>,>>>,>>9.99"))
                                    count_break =  to_decimal(count_break) + to_decimal(argt_rate)

                        if guest_pr and not argt_defined:

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                     (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).first()

                            if reslin_queasy:

                                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                                         (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == argt_line.argt_artnr) & (Reslin_queasy.resnr == argt_line.departement) & (Reslin_queasy.bill_date >= Reslin_queasy.date1) & (Reslin_queasy.bill_date <= Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
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
                                        argt_rate = ( to_decimal(rm_rate) * to_decimal(() - to_decimal(argt_rate) / to_decimal(100))) * to_decimal(qty)

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
                            argt_rate2 = ( to_decimal(rm_rate) * to_decimal(() - to_decimal(argt_rate2) / to_decimal(100))) * to_decimal(qty)

                        if argt_rate == 0:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = 1
                            c = to_string(qty) + " " + artikel.bezeich
                            str = to_string(translateExtended (" Incl.", lvcarea, "") , "x(10)") + " " + to_string(c, "x(16)") + " = " + trim(to_string(argt_rate2, "->>>,>>>,>>9.99"))
                            count_break =  to_decimal(count_break) + to_decimal(argt_rate2)


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

                    if (res_line.abreise - start_date) < fixleist.dekade:
                        start_date = res_line.ankunft

                    if datum <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                        add_it = True

                    if datum < start_date:
                        add_it = False

                if add_it:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == fixleist.artnr) & (Artikel.departement == fixleist.departement)).first()
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


    def usr_prog1(bill_date:date, roomrate:decimal):

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

        it_exist = False
        prog_str:str = ""
        i:int = 0

        def generate_inner_output():
            return (roomrate, it_exist)


        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (func.lower(Reslin_queasy.key) == ("rate-prog").lower()) & (Reslin_queasy.number1 == resnr) & (Reslin_queasy.number2 == 0) & (Reslin_queasy.char1 == "") & (Reslin_queasy.reslinnr == 1)).first()

        if reslin_queasy:
            prog_str = reslin_queasy.char3

        if prog_str != "":
            pass

        return generate_inner_output()


    def usr_prog2(bill_date:date, roomrate:decimal):

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

        it_exist = False
        prog_str:str = ""
        i:int = 0

        def generate_inner_output():
            return (roomrate, it_exist)


        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (func.lower(Queasy.char1) == (contcode).lower())).first()

        if queasy:
            prog_str = queasy.char3

        if prog_str != "":
            pass

        return generate_inner_output()


    def calc_periode():

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

        periode_rsv1:date = None
        periode_rsv2:date = None
        counter:int = 0

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 301) & (Queasy.number1 == res_line.resnr) & (Queasy.logi1 == repeat_charge)).first()

        if queasy:
            periode_rsv1 = res_line.ankunft
            periode_rsv2 = res_line.abreise

            if get_month(periode_rsv1) + 1 > 12:
                periode = date_mdy(1, get_day(periode_rsv1) , get_year(periode_rsv1) + timedelta(days=1) - 1)


            else:
                periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1, get_day(periode_rsv1) , get_year(periode_rsv1)) - 1)


            for loopi in date_range(periode_rsv1,periode_rsv2 - 1) :

                if loopi > periode:
                    periode_rsv1 = loopi

                    if get_month(periode_rsv1) + 1 > 12:
                        periode = date_mdy(1, get_day(periode_rsv1) , get_year(periode_rsv1) + timedelta(days=1) - 1)


                    else:
                        periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1, get_day(periode_rsv1) , get_year(periode_rsv1)) - 1)

                if loopi <= periode:

                    periode_list = query(periode_list_list, filters=(lambda periode_list: periode_list.periode1 == periode_rsv1), first=True)

                    if not periode_list:
                        periode_list = Periode_list()
                        periode_list_list.append(periode_list)

                        periode_list.periode1 = periode_rsv1
                        counter = counter + 1
                        periode_list.counter = counter


                    periode_list.periode2 = loopi

            for periode_list in query(periode_list_list):
                periode_list.diff_day = periode_list.periode2 - periode_list.periode1 + 1

                if periode_list.diff_day >= 30:
                    periode_list.amt_periode =  to_decimal(queasy.deci1) / to_decimal(periode_list.diff_day)
                    periode_list.tamount =  to_decimal(periode_list.amt_periode) * to_decimal(periode_list.diff_day)
                    curr_diff =  to_decimal(periode_list.diff_day)


                else:
                    periode_list.amt_periode = ( to_decimal(queasy.deci1) * to_decimal(12)) / to_decimal("365")
                    periode_list.tamount =  to_decimal(periode_list.amt_periode) * to_decimal(periode_list.diff_day)


    def cal_revenue1():

        nonlocal output_list_list, ci_date, new_contrate, wd_array, bonus_array, periode, loopi, curr_diff, lvcarea, reservation, htparam, res_line, arrangement, guest_pr, waehrung, genstat, reslin_queasy, queasy, katpreis, argt_line, artikel, fixleist
        nonlocal pvilanguage, resnr, reslinnr, contcode, repeat_charge


        nonlocal output_list, periode_list, output_list1
        nonlocal output_list_list, periode_list_list, output_list1_list

        datum:date = None
        co_date:date = None
        argt_rate:decimal = to_decimal("0.0")
        argt_rate2:decimal = to_decimal("0.0")
        rm_rate:decimal = to_decimal("0.0")
        daily_rate:decimal = to_decimal("0.0")
        tot_rate:decimal = to_decimal("0.0")
        add_it:bool = False
        c:str = ""
        fixed_rate:bool = False
        argt_defined:bool = False
        delta:int = 0
        start_date:date = None
        qty:int = 0
        it_exist:bool = False
        exrate1:decimal = 1
        ex2:decimal = 1
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
        ratecode_qsy:str = ""
        count_break:decimal = to_decimal("0.0")
        fixcost_rate:decimal = to_decimal("0.0")
        counter:int = 0
        w1 = None
        W1 =  create_buffer("W1",Waehrung)
        n = 0

        if re.match(r".*DATE,.*",res_line.zimmer_wunsch, re.IGNORECASE):
            n = 1 + get_index(res_line.zimmer_wunsch, "Date,")

        if n > 0:
            c = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
            created_date = date_mdy(to_int(substring(c, 4, 2)) , to_int(substring(c, 6, 2)) , to_int(substring(c, 0, 4)))
        else:
            created_date = reservation.resdat
        ebdisc_flag = re.match(".*ebdisc.*",res_line.zimmer_wunsch)
        kbdisc_flag = re.match(".*kbdisc.*",res_line.zimmer_wunsch)

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

            if datum < ci_date:

                genstat = db_session.query(Genstat).filter(
                         (Genstat.datum == datum) & (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr)).first()

                if genstat:

                    periode_list = query(periode_list_list, filters=(lambda periode_list: periode_list.genstat.datum >= periode_list.periode1 and genstat.datum <= periode_list.periode2), first=True)

                    if periode_list:

                        output_list1 = query(output_list1_list, filters=(lambda output_list1: output_list1.datum == periode_list.periode1), first=True)

                        if not output_list1:
                            output_list1 = Output_list1()
                            output_list1_list.append(output_list1)

                            output_list1.datum = periode_list.periode1
                        output_list1.rate =  to_decimal(output_list1.rate) + to_decimal(genstat.zipreis)

            if datum >= ci_date:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.datum >= Reslin_queasy.date1) & (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

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

                        arrangement = db_session.query(Arrangement).filter(
                                 (Arrangement.arrangement == reslin_queasy.char1)).first()
                    rm_rate, it_exist = usr_prog1(datum, rm_rate)

                if not fixed_rate:
                    rm_rate, it_exist = usr_prog1(datum, rm_rate)

                    if not it_exist:

                        if guest_pr:

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 18) & (Queasy.number1 == res_line.reserve_int)).first()

                            if queasy and queasy.logi3:
                                bill_date = res_line.ankunft

                            if new_contrate:
                                rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                            else:
                                rm_rate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                                rm_rate, it_exist = usr_prog2(datum, rm_rate)

                                if it_exist:
                                    rate_found = True

                                if not it_exist and bonus_array[curr_i - 1] :
                                    rm_rate =  to_decimal("0")

                        if not rate_found:
                            w_day = wd_array[get_weekday(bill_date) - 1]

                            if (bill_date == ci_date) or (bill_date == res_line.ankunft):
                                rm_rate =  to_decimal(res_line.zipreis)

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                                if not katpreis:

                                    katpreis = db_session.query(Katpreis).filter(
                                             (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                                if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rm_rate:
                                    rack_rate = True

                            elif rack_rate:

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                                if not katpreis:

                                    katpreis = db_session.query(Katpreis).filter(
                                             (Katpreis.zikat == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                                if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                                    rm_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                            if bonus_array[curr_i - 1] :
                                rm_rate =  to_decimal("0")

                periode_list = query(periode_list_list, filters=(lambda periode_list: periode_list.datum >= periode_list.periode1 and datum <= periode_list.periode2), first=True)

                if periode_list:

                    output_list1 = query(output_list1_list, filters=(lambda output_list1: output_list1.datum == periode_list.periode1), first=True)

                    if not output_list1:
                        output_list1 = Output_list1()
                        output_list1_list.append(output_list1)

                        output_list1.datum = periode_list.periode1
                    output_list1.rate =  to_decimal(output_list1.rate) + to_decimal(rm_rate)


        tot_rate =  to_decimal("0")

        for output_list1 in query(output_list1_list, sort_by=[("datum",False)]):
            output_list = Output_list()
            output_list_list.append(output_list)

            counter = counter + 1
            output_list.flag = counter
            output_list.str = to_string(output_list1.datum) + " " + translateExtended ("roomrate", lvcarea, "") +\
                    " = " + trim(to_string(output_list1.rate, "->>>,>>>,>>9.99"))
            tot_rate =  to_decimal(tot_rate) + to_decimal(output_list1.rate)


        output_list = Output_list()
        output_list_list.append(output_list)

        counter = counter + 1
        output_list.flag = counter
        output_list.str = " " + translateExtended ("Expected total revenue =", lvcarea, "") +\
                " " + trim(to_string(tot_rate, "->,>>>,>>>,>>9.99"))


    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr == resnr)).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

    arrangement = db_session.query(Arrangement).filter(
             (Arrangement.arrangement == res_line.arrangement)).first()

    guest_pr = db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == res_line.gastnr)).first()
    check_bonus()

    if repeat_charge :
        calc_periode()
        cal_revenue1()
    else:
        cal_revenue()

    return generate_output()