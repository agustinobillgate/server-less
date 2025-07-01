#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from functions.ratecode_seek import ratecode_seek
from models import Waehrung, Res_line, Htparam, Guest, Artikel, Guest_pr, Arrangement, Reslin_queasy, Queasy, Katpreis, Pricecod, Argt_line, Fixleist

def get_room_breakdown_phm(recid_resline:int, datum:date, curr_i:int, curr_date:date, banquet_dept:string, commision:string, payable:string):

    prepare_cache ([Waehrung, Res_line, Htparam, Artikel, Guest_pr, Arrangement, Reslin_queasy, Katpreis, Pricecod, Argt_line, Fixleist])

    lvcarea:string = "occ-fcast1"
    fnet_lodging = to_decimal("0.0")
    lnet_lodging = to_decimal("0.0")
    net_breakfast = to_decimal("0.0")
    net_lunch = to_decimal("0.0")
    net_dinner = to_decimal("0.0")
    net_others = to_decimal("0.0")
    tot_rmrev = to_decimal("0.0")
    nett_vat = to_decimal("0.0")
    nett_service = to_decimal("0.0")
    net_banquet = to_decimal("0.0")
    net_commision = to_decimal("0.0")
    net_payable = to_decimal("0.0")
    exrate:Decimal = to_decimal("0.0")
    frate:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    new_contrate:bool = False
    bonus_array:List[bool] = create_empty_list(999, False)
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    rm_vat:bool = False
    rm_serv:bool = False
    nett_rmrev:Decimal = to_decimal("0.0")
    j:int = 0
    ex_article:string = ""
    done:bool = False
    waehrung = res_line = htparam = guest = artikel = guest_pr = arrangement = reslin_queasy = queasy = katpreis = pricecod = argt_line = fixleist = None

    waehrung1 = None

    Waehrung1 = create_buffer("Waehrung1",Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, net_banquet, net_commision, net_payable, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, j, ex_article, done, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line, fixleist
        nonlocal recid_resline, datum, curr_i, curr_date, banquet_dept, commision, payable
        nonlocal waehrung1


        nonlocal waehrung1

        return {"fnet_lodging": fnet_lodging, "lnet_lodging": lnet_lodging, "net_breakfast": net_breakfast, "net_lunch": net_lunch, "net_dinner": net_dinner, "net_others": net_others, "tot_rmrev": tot_rmrev, "nett_vat": nett_vat, "nett_service": nett_service, "net_banquet": net_banquet, "net_commision": net_commision, "net_payable": net_payable}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, net_banquet, net_commision, net_payable, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, j, ex_article, done, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line, fixleist
        nonlocal recid_resline, datum, curr_i, curr_date, banquet_dept, commision, payable
        nonlocal waehrung1


        nonlocal waehrung1

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def calc_lodging2():

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, net_banquet, net_commision, net_payable, exrate, frate, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, j, ex_article, done, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line, fixleist
        nonlocal recid_resline, datum, curr_i, curr_date, banquet_dept, commision, payable
        nonlocal waehrung1


        nonlocal waehrung1

        qty:int = 0
        fixed_rate:bool = False
        it_exist:bool = False
        rmrate:Decimal = to_decimal("0.0")
        gpax:int = 0
        bill_date:date = None
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        restricted_disc:bool = False
        kback_flag:bool = False
        curr_zikatnr:int = 0
        w_day:int = 0
        rack_rate:bool = False
        vat:Decimal = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat_art:Decimal = to_decimal("0.0")
        service_art:Decimal = to_decimal("0.0")
        wrung = None
        qty1:int = 0
        take_it:bool = False
        post_it:bool = False
        bfast_art:int = 0
        fb_dept:int = 0
        lunch_art:int = 0
        dinner_art:int = 0
        lundin_art:int = 0
        contcode:string = ""
        ct:string = ""
        prcode:int = 0
        f_betrag:Decimal = to_decimal("0.0")
        argt_betrag:Decimal = to_decimal("0.0")
        fcost:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        nett_lamt:Decimal = to_decimal("0.0")
        gross_lamt:Decimal = to_decimal("0.0")
        nett_lserv:Decimal = to_decimal("0.0")
        nett_ltax:Decimal = to_decimal("0.0")
        nett_famt:Decimal = to_decimal("0.0")
        nett_fserv:Decimal = to_decimal("0.0")
        nett_ftax:Decimal = to_decimal("0.0")
        price_decimal:int = 0
        argtnr:string = ""
        rguest = None
        tot_fbreakfast:Decimal = to_decimal("0.0")
        tot_flunch:Decimal = to_decimal("0.0")
        tot_fdinner:Decimal = to_decimal("0.0")
        tot_fother:Decimal = to_decimal("0.0")
        tot_lbreakfast:Decimal = to_decimal("0.0")
        tot_llunch:Decimal = to_decimal("0.0")
        tot_ldinner:Decimal = to_decimal("0.0")
        tot_lother:Decimal = to_decimal("0.0")
        Wrung =  create_buffer("Wrung",Waehrung)
        Rguest =  create_buffer("Rguest",Guest)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
        bfast_art = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})
        fb_dept = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)],"departement": [(eq, fb_dept)]})

        if not artikel and bfast_art != 0:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
        lunch_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, lunch_art)],"departement": [(eq, fb_dept)]})

        if not artikel and lunch_art != 0:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
        dinner_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, dinner_art)],"departement": [(eq, fb_dept)]})

        if not artikel and dinner_art != 0:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})
        lundin_art = htparam.finteger

        artikel = get_cache (Artikel, {"zwkum": [(eq, lundin_art)],"departement": [(eq, fb_dept)]})

        if not artikel and lundin_art != 0:

            return
        qty1 = res_line.zimmeranz
        rmrate =  to_decimal(res_line.zipreis)
        bill_date = datum

        wrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if wrung:
            exrate =  to_decimal(wrung.ankauf) / to_decimal(wrung.einheit)
        else:
            exrate =  to_decimal("1")

        if res_line.resstatus == 6 and res_line.reserve_dec > 0:
            frate =  to_decimal(reserve_dec)
        else:
            frate =  to_decimal(exrate)

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
        service =  to_decimal("0")
        vat =  to_decimal("0")

        if artikel:
            service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

        if reslin_queasy:
            fixed_rate = True
            rmrate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.number3 != 0:
                gpax = reslin_queasy.number3

            if reslin_queasy.char1 != "":

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_queasy.char1)]})
            argtnr = arrangement.arrangement

        if not fixed_rate:

            if not it_exist:

                if guest_pr:

                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

                    if queasy and queasy.logi3:
                        bill_date = res_line.ankunft

                    if new_contrate:
                        rate_found, rmrate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, guest_pr.code, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, argtnr, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                    else:
                        rmrate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.code, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

                        if it_exist:
                            rate_found = True

                        if curr_i != 0:

                            if not it_exist and bonus_array[curr_i - 1] :
                                rmrate =  to_decimal("0")

                if not rate_found:
                    w_day = wd_array[get_weekday(bill_date) - 1]

                    if (bill_date == curr_date) or (bill_date == res_line.ankunft):
                        rmrate =  to_decimal(res_line.zipreis)

                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                        if not katpreis:

                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rmrate:
                            rack_rate = True

                    elif rack_rate:

                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

                        if not katpreis:

                            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                            rmrate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                    if curr_i != 0:

                        if bonus_array[curr_i - 1] :
                            rmrate =  to_decimal("0")
        tot_rmrev =  to_decimal(rmrate)


        contcode = ""

        rguest = db_session.query(Rguest).filter(
                 (Rguest.gastnr == res_line.gastnr)).first()

        if res_line.reserve_int != 0:

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, rguest.gastnr)]})

        if guest_pr:
            contcode = guest_pr.code
            ct = res_line.zimmer_wunsch

            if matches(ct,r"*$CODE$*"):
                ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                contcode = substring(ct, 0, get_index(ct, ";") - 1)

            if new_contrate:
                prcode = get_output(ratecode_seek(res_line.resnr, res_line.reslinnr, contcode, datum))
            else:

                pricecod = get_cache (Pricecod, {"code": [(eq, contcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, curr_zikatnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)]})

                if pricecod:
                    prcode = pricecod._recid
        gross_lamt =  to_decimal("0")

        if argtnr == "":
            argtnr = res_line.arrangement

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argtnr)]})

        argt_line_obj_list = {}
        argt_line = Argt_line()
        artikel = Artikel()
        for argt_line._recid, argt_line.betriebsnr, argt_line.betrag, argt_line.argtnr, argt_line.vt_percnt, artikel.departement, artikel.artnr, artikel.service_code, artikel.mwst_code, artikel.umsatzart, artikel._recid in db_session.query(Argt_line._recid, Argt_line.betriebsnr, Argt_line.betrag, Argt_line.argtnr, Argt_line.vt_percnt, Artikel.departement, Artikel.artnr, Artikel.service_code, Artikel.mwst_code, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                 (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
            if argt_line_obj_list.get(argt_line._recid):
                continue
            else:
                argt_line_obj_list[argt_line._recid] = True


            take_it, f_betrag, argt_betrag, qty = get_argtline_rate(datum, contcode, argt_line._recid)
            service_art =  to_decimal("0")
            vat_art =  to_decimal("0")
            service_art, vat_art = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            if take_it:
                nett_lamt = ( to_decimal((argt_betrag)) * to_decimal(qty1) )
                gross_lamt =  to_decimal(gross_lamt) + to_decimal(((argt_betrag)) * to_decimal(qty1) )
                nett_lamt =  to_decimal(nett_lamt) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )
                nett_famt = ( to_decimal((argt_betrag)) * to_decimal(frate)) * to_decimal(qty1)
                nett_famt =  to_decimal(nett_famt) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )


                done = False

                if commision != "":
                    for j in range(1,num_entries(commision, ";")  + 1) :
                        ex_article = entry(j - 1, commision, ";")

                        if artikel.artnr == to_int(entry(0, ex_article, "-")) and artikel.departement == to_int(entry(1, ex_article, "-")):
                            done = True
                            net_commision =  to_decimal(net_commision) + to_decimal(nett_lamt) * to_decimal(frate)

                if payable != "" and done == False:
                    for j in range(1,num_entries(payable, ";")  + 1) :
                        ex_article = entry(j - 1, payable, ";")

                        if artikel.artnr == to_int(entry(0, ex_article, "-")) and artikel.departement == to_int(entry(1, ex_article, "-")):
                            done = True
                            net_payable =  to_decimal(net_payable) + to_decimal(nett_lamt) * to_decimal(frate)

                if not done:

                    if banquet_dept != "" and artikel.departement == to_int(banquet_dept):
                        net_banquet =  to_decimal(net_banquet) + to_decimal(nett_lamt) * to_decimal(frate)

                    elif artikel.umsatzart == 3 or artikel.umsatzart >= 5:
                        tot_lbreakfast =  to_decimal(tot_lbreakfast) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fbreakfast =  to_decimal(tot_fbreakfast) + to_decimal(nett_famt)


                    else:
                        tot_lother =  to_decimal(tot_lother) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fother =  to_decimal(tot_fother) + to_decimal(nett_famt)

        for fixleist in db_session.query(Fixleist).filter(
                 (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
            post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)
            service_art =  to_decimal("0")
            vat_art =  to_decimal("0")

            if post_it:

                artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})

                if artikel:
                    service_art, vat_art = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))
                fcost =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)
                fcost =  to_decimal(fcost) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )


                done = False

                if commision != "":
                    for j in range(1,num_entries(commision, ";")  + 1) :
                        ex_article = entry(j - 1, commision, ";")

                        if artikel.artnr == to_int(entry(0, ex_article, "-")) and artikel.departement == to_int(entry(1, ex_article, "-")):
                            done = True
                            net_commision =  to_decimal(net_commision) + to_decimal(fcost) * to_decimal(frate)

                if payable != "" and done == False:
                    for j in range(1,num_entries(payable, ";")  + 1) :
                        ex_article = entry(j - 1, payable, ";")

                        if artikel.artnr == to_int(entry(0, ex_article, "-")) and artikel.departement == to_int(entry(1, ex_article, "-")):
                            done = True
                            net_payable =  to_decimal(net_payable) + to_decimal(fcost) * to_decimal(frate)

                if not done:

                    if banquet_dept != "" and artikel.departement == int (banquet_dept):
                        net_banquet =  to_decimal(net_banquet) + to_decimal(fcost) * to_decimal(frate)

                    elif artikel.umsatzart == 3 or artikel.umsatzart >= 5:
                        tot_lbreakfast =  to_decimal(tot_lbreakfast) + to_decimal(fcost) * to_decimal(frate)
                        tot_fbreakfast =  to_decimal(tot_fbreakfast) + to_decimal(fcost)


                    else:
                        tot_lother =  to_decimal(tot_lother) + to_decimal(fcost) * to_decimal(frate)
                        tot_fother =  to_decimal(tot_fother) + to_decimal(fcost)


        rmrate =  to_decimal(rmrate) * to_decimal(qty1)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        rm_vat = htparam.flogical

        if rm_vat:
            rmrate =  to_decimal(rmrate) - to_decimal(gross_lamt)
            nett_rmrev =  to_decimal(rmrate) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )
            nett_service =  to_decimal(nett_rmrev) * to_decimal(service)
            nett_vat =  to_decimal(nett_rmrev) * to_decimal(vat)


        else:
            rmrate =  to_decimal(rmrate) - to_decimal(nett_lamt)
            nett_rmrev =  to_decimal(rmrate)
            nett_service =  to_decimal(rmrate) * to_decimal(service)
            nett_vat =  to_decimal(rmrate) * to_decimal(vat)
            tot_rmrev =  to_decimal(rmrate) + to_decimal(nett_service) + to_decimal(nett_vat)


        net_breakfast =  to_decimal(tot_lbreakfast)
        net_lunch =  to_decimal(tot_llunch)
        net_dinner =  to_decimal(tot_ldinner)
        net_others =  to_decimal(tot_lother)

        if rmrate != 0:
            fnet_lodging, lnet_lodging = get_lodging(argtnr, rmrate, bill_date)

            if rm_vat:
                fnet_lodging =  to_decimal(fnet_lodging) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )
                lnet_lodging =  to_decimal(lnet_lodging) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )


        else:
            lnet_lodging =  to_decimal("0")
            fnet_lodging =  to_decimal("0")


    def get_argtline_rate(curr_date:date, contcode:string, argt_recid:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, net_banquet, net_commision, net_payable, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, j, ex_article, done, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line, fixleist
        nonlocal recid_resline, datum, curr_i, banquet_dept, commision, payable
        nonlocal waehrung1


        nonlocal waehrung1

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        argtline = get_cache (Argt_line, {"_recid": [(eq, argt_recid)]})

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = res_line.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = res_line.kind1

        elif argt_line.vt_percnt == 2:
            qty = res_line.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if res_line.ankunft == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (res_line.ankunft + 1) == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 4 and get_day(curr_date) == 1:
                add_it = True

            elif argtline.fakt_modus == 5 and get_day(curr_date + 1) == 1:
                add_it = True

            elif argtline.fakt_modus == 6:

                if (res_line.ankunft + (argtline.intervall - 1)) >= curr_date:
                    add_it = True

        if add_it:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number1": [(eq, argtline.departement)],"number2": [(eq, argtline.argtnr)],"number3": [(eq, argtline.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

            if reslin_queasy:
                argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                f_betrag =  to_decimal(argt_betrag)

                waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                    waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})
            f_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)
            argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, net_banquet, net_commision, net_payable, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, j, ex_article, done, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line, fixleist
        nonlocal recid_resline, datum, curr_i, banquet_dept, commision, payable
        nonlocal waehrung1


        nonlocal waehrung1

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return (post_it)


        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = (lfakt - res_line.ankunft).days

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + timedelta(days=delta)

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()


    def get_lodging(argtnr:string, zipreis:Decimal, bill_date:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, net_banquet, net_commision, net_payable, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, j, ex_article, done, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line, fixleist
        nonlocal recid_resline, datum, curr_i, curr_date, banquet_dept, commision, payable
        nonlocal waehrung1


        nonlocal waehrung1

        flodg_betrag = to_decimal("0.0")
        llodg_betrag = to_decimal("0.0")
        service:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        qty:int = 0
        argt_betrag:Decimal = to_decimal("0.0")
        fargt_betrag:Decimal = to_decimal("0.0")
        add_it:bool = False
        marknr:int = 0

        def generate_inner_output():
            return (flodg_betrag, llodg_betrag)


        if argtnr == "":
            argtnr = res_line.arrangement

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argtnr)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})
        service =  to_decimal("0")
        vat =  to_decimal("0")

        if artikel:

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.service_code)]})

            if htparam and htparam.fdecimal != 0:
                service =  to_decimal(htparam.fdecimal) / to_decimal("100")

            htparam = get_cache (Htparam, {"paramnr": [(eq, artikel.mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

            htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

            if htparam.flogical:
                vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
            vat =  to_decimal(round (vat , 2))
        flodg_betrag =  to_decimal(zipreis)
        llodg_betrag =  to_decimal(zipreis) * to_decimal(frate)
        llodg_betrag =  to_decimal(round (llodg_betrag , price_decimal))
        flodg_betrag =  to_decimal(round (flodg_betrag , price_decimal))

        return generate_inner_output()

    res_line = get_cache (Res_line, {"_recid": [(eq, recid_resline)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical
    calc_lodging2()

    return generate_output()