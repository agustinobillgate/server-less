from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from sqlalchemy import func
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
import re
from functions.ratecode_seek import ratecode_seek
from models import Waehrung, Res_line, Htparam, Guest, Artikel, Guest_pr, Arrangement, Reslin_queasy, Queasy, Katpreis, Pricecod, Argt_line

def get_room_breakdown(recid_resline:int, datum:date, curr_i:int, curr_date:date):
    lvcarea:str = "occ_fcast1"
    fnet_lodging = 0
    lnet_lodging = 0
    net_breakfast = 0
    net_lunch = 0
    net_dinner = 0
    net_others = 0
    tot_rmrev = 0
    nett_vat = 0
    nett_service = 0
    exrate:decimal = 0
    frate:decimal = 0
    price_decimal:int = 0
    new_contrate:bool = False
    bonus_array:[bool] = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    rm_vat:bool = False
    rm_serv:bool = False
    nett_rmrev:decimal = 0
    waehrung = res_line = htparam = guest = artikel = guest_pr = arrangement = reslin_queasy = queasy = katpreis = pricecod = argt_line = None

    waehrung1 = wrung = rguest = argtline = None

    Waehrung1 = Waehrung
    Wrung = Waehrung
    Rguest = Guest
    Argtline = Argt_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline
        return {"fnet_lodging": fnet_lodging, "lnet_lodging": lnet_lodging, "net_breakfast": net_breakfast, "net_lunch": net_lunch, "net_dinner": net_dinner, "net_others": net_others, "tot_rmrev": tot_rmrev, "nett_vat": nett_vat, "nett_service": nett_service}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        rate:decimal = 0

        if erwachs >= 1 and erwachs <= 4:
            rate = rate + katpreis.perspreis[erwachs - 1]
        rate = rate + kind1 * katpreis.kindpreis[0] + kind2 * katpreis.kindpreis[1]
        return rate

    def calc_lodging2():

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        qty:int = 0
        fixed_rate:bool = False
        it_exist:bool = False
        rmrate:decimal = 0
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
        vat:decimal = 0
        service:decimal = 0
        vat_art:decimal = 0
        service_art:decimal = 0
        qty1:int = 0
        take_it:bool = False
        post_it:bool = False
        bfast_art:int = 0
        fb_dept:int = 0
        lunch_art:int = 0
        dinner_art:int = 0
        lundin_art:int = 0
        contcode:str = ""
        ct:str = ""
        prcode:int = 0
        f_betrag:decimal = 0
        argt_betrag:decimal = 0
        fcost:decimal = 0
        fact:decimal = 0
        nett_lamt:decimal = 0
        gross_lamt:decimal = 0
        tnett_lamt:decimal = 0
        nett_lserv:decimal = 0
        nett_ltax:decimal = 0
        nett_famt:decimal = 0
        nett_fserv:decimal = 0
        nett_ftax:decimal = 0
        price_decimal:int = 0
        argtnr:str = ""
        tot_fbreakfast:decimal = 0
        tot_flunch:decimal = 0
        tot_fdinner:decimal = 0
        tot_fother:decimal = 0
        tot_lbreakfast:decimal = 0
        tot_llunch:decimal = 0
        tot_ldinner:decimal = 0
        tot_lother:decimal = 0
        Wrung = Waehrung
        Rguest = Guest

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 125)).first()
        bfast_art = finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 126)).first()
        fb_dept = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == bfast_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and bfast_art != 0:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 227)).first()
        lunch_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == lunch_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and lunch_art != 0:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 228)).first()
        dinner_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == dinner_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and dinner_art != 0:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 229)).first()
        lundin_art = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.zwkum == lundin_art) &  (Artikel.departement == fb_dept)).first()

        if not artikel and lundin_art != 0:

            return
        qty1 = res_line.zimmeranz
        rmrate = res_line.zipreis
        bill_date = datum

        wrung = db_session.query(Wrung).filter(
                (Wrung.waehrungsnr == res_line.betriebsnr)).first()

        if wrung:
            exrate = wrung.ankauf / wrung.einheit
        else:
            exrate = 1

        if res_line.resstatus == 6 and res_line.reserve_dec > 0:
            frate = reserve_dec
        else:
            frate = exrate

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == res_line.gastnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()
        service = 0
        vat = 0

        if artikel:
            service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

        if reslin_queasy:
            fixed_rate = True
            rmrate = reslin_queasy.deci1

            if reslin_queasy.number3 != 0:
                gpax = reslin_queasy.number3

            if reslin_queasy.char1 != "":

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == reslin_queasy.char1)).first()
            argtnr = arrangement
            rmrate, it_exist = usr_prog1(datum, rmrate)

        if not fixed_rate:
            rmrate, it_exist = usr_prog1(datum, rmrate)

            if not it_exist:

                if guest_pr:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 18) &  (Queasy.number1 == res_line.reserve_int)).first()

                    if queasy and queasy.logi3:
                        bill_date = res_line.ankunft

                    if new_contrate:
                        rate_found, rmrate, restricted_disc, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, guest_pr.CODE, None, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, argtnr, res_line.zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                    else:
                        rmrate, rate_found = get_output(pricecod_rate(res_line.resnr, res_line.reslinnr, guest_pr.CODE, bill_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))
                        rmrate, it_exist = usr_prog2(datum, rmrate)

                        if it_exist:
                            rate_found = True

                        if curr_i != 0:

                            if not it_exist and bonus_array[curr_i - 1] :
                                rmrate = 0

                if not rate_found:
                    w_day = wd_array[get_weekday(bill_date) - 1]

                    if (bill_date == curr_date) or (bill_date == res_line.ankunft):
                        rmrate = res_line.zipreis

                        katpreis = db_session.query(Katpreis).filter(
                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                        if not katpreis:

                            katpreis = db_session.query(Katpreis).filter(
                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rmrate:
                            rack_rate = True

                    elif rack_rate:

                        katpreis = db_session.query(Katpreis).filter(
                                (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == w_day)).first()

                        if not katpreis:

                            katpreis = db_session.query(Katpreis).filter(
                                    (Katpreis.zikat == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= bill_date) &  (Katpreis.endperiode >= bill_date) &  (Katpreis.betriebsnr == 0)).first()

                        if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) > 0:
                            rmrate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)

                    if curr_i != 0:

                        if bonus_array[curr_i - 1] :
                            rmrate = 0
        tot_rmrev = rmrate


        contcode = ""

        rguest = db_session.query(Rguest).filter(
                (Rguest.gastnr == res_line.gastnr)).first()

        if res_line.reserve_int != 0:

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == rguest.gastnr)).first()

        if guest_pr:
            contcode = guest_pr.CODE
            ct = res_line.zimmer_wunsch

            if re.match(".*\$CODE\$.*",ct):
                ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
                contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

            if new_contrate:
                prcode = get_output(ratecode_seek(res_line.resnr, res_line.reslinnr, contcode, datum))
            else:

                pricecod = db_session.query(Pricecod).filter(
                        (func.lower(Pricecod.code) == (contcode).lower()) &  (Pricecod.marknr == res_line.reserve_int) &  (Pricecod.argtnr == arrangement.argtnr) &  (Pricecod.zikatnr == curr_zikatnr) &  (Pricecod.datum >= Pricecod.startperiode) &  (Pricecod.datum <= Pricecod.endperiode)).first()

                if pricecod:
                    prcode = pricecod._recid
        gross_lamt = 0

        if argtnr == "":
            argtnr = res_line.arrangement

        arrangement = db_session.query(Arrangement).filter(
                (func.lower(Arrangement) == (argtnr).lower())).first()

        argt_line_obj_list = []
        for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) &  (Artikel.departement == Argt_line.departement)).filter(
                (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2) &  (Argt_line.kind1)).all():
            if argt_line._recid in argt_line_obj_list:
                continue
            else:
                argt_line_obj_list.append(argt_line._recid)


            take_it, f_betrag, argt_betrag, qty = get_argtline_rate(datum, contcode, argt_line._recid)
            service_art = 0
            vat_art = 0
            service_art, vat_art = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            if take_it:
                nett_lamt = ((argt_betrag) * qty1)
                gross_lamt = gross_lamt + ((argt_betrag) * qty1)
                nett_lamt = nett_lamt / (1 + service_art + vat_art)
                tnett_lamt = tnett_lamt + nett_lamt
                nett_famt = ((argt_betrag) * frate) * qty1
                nett_famt = nett_famt / (1 + service_art + vat_art)

                if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    tot_lbreakfast = tot_lbreakfast + nett_lamt * frate
                    tot_fbreakfast = tot_fbreakfast + nett_famt

                elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    tot_llunch = tot_llunch + nett_lamt * frate
                    tot_flunch = tot_flunch + nett_famt

                elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    tot_ldinner = tot_ldinner + nett_lamt * frate
                    tot_fdinner = tot_fdinner + nett_famt

                elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                    tot_llunch = tot_llunch + nett_lamt * frate
                    tot_flunch = tot_flunch + nett_famt


                else:
                    tot_lother = tot_lother + nett_lamt * frate
                    tot_fother = tot_fother + nett_famt


        rmrate = rmrate * qty1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 127)).first()
        rm_vat = htparam.flogical

        if rm_vat:
            rmrate = rmrate - gross_lamt
            nett_rmrev = rmrate / (1 + vat + service)
            nett_service = nett_rmrev * service
            nett_vat = nett_rmrev * vat


        else:
            rmrate = rmrate - tnett_lamt
            nett_rmrev = rmrate
            nett_service = rmrate * service
            nett_vat = rmrate * vat
            tot_rmrev = rmrate + nett_service + nett_vat


        net_breakfast = tot_lbreakfast
        net_lunch = tot_llunch
        net_dinner = tot_ldinner
        net_others = tot_lother

        if rmrate != 0:
            fnet_lodging, lnet_lodging = get_lodging(argtnr, rmrate, bill_date)

            if rm_vat:
                fnet_lodging = fnet_lodging / (1 + vat + service)
                lnet_lodging = lnet_lodging / (1 + vat + service)


        else:
            lnet_lodging = 0
            fnet_lodging = 0

    def get_argtline_rate(curr_date:date, contcode:str, argt_recid:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        add_it = False
        f_betrag = 0
        argt_betrag = 0
        qty = 0
        curr_zikatnr:int = 0

        def generate_inner_output():
            return add_it, f_betrag, argt_betrag, qty
        Argtline = Argt_line

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        argtline = db_session.query(Argtline).filter(
                (Argtline._recid == argt_recid)).first()

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

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr) &  (Reslin_queasy.number1 == argtline.departement) &  (Reslin_queasy.number2 == argtline.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:

                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != "0":
                    argt_betrag = res_line.zipreis * to_int(reslin_queasy.char2) / 100
                    f_betrag = argt_betrag
                else:
                    argt_betrag = reslin_queasy.deci1 * qty
                    f_betrag = argt_betrag

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung._recid == waehrung1._recid)).first()

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "argt_line") &  (func.lower(Reslin_queasy.char1) == (contcode).lower()) &  (Reslin_queasy.number1 == res_line.reserve_int) &  (Reslin_queasy.number2 == arrangement.argtnr) &  (Reslin_queasy.number3 == argtline.argt_artnr) &  (Reslin_queasy.resnr == argtline.departement) &  (Reslin_queasy.reslinnr == curr_zikatnr) &  (Reslin_queasy.curr_date >= Reslin_queasy.date1) &  (Reslin_queasy.curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag = reslin_queasy.deci1 * qty
                    f_betrag = argt_betrag

                    waehrung1 = db_session.query(Waehrung1).filter(
                            (Waehrung1.waehrungsnr == res_line.betriebsnr)).first()

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrung._recid == waehrung1._recid)).first()

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag = argt_line.betrag

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == argt_line.argtnr)).first()

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == arrangement.betriebsnr)).first()
            f_betrag = argt_betrag * qty

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag = argt_betrag * (waehrung.ankauf / waehrung.einheit) / frate

            if argt_betrag > 0:
                argt_betrag = argt_betrag * qty
            else:
                argt_betrag = (res_line.zipreis * (- argt_betrag / 100)) * qty

            if argt_betrag == 0:
                add_it = False


        return generate_inner_output()

    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return post_it

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
                delta = lfakt - res_line.ankunft

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + delta

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + (intervall - 1)):
                post_it = True

            if curr_date < start_date:
                post_it = False


        return generate_inner_output()

    def get_lodging(argtnr:str, zipreis:decimal, bill_date:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        flodg_betrag = 0
        llodg_betrag = 0
        service:decimal = 0
        vat:decimal = 0
        qty:int = 0
        argt_betrag:decimal = 0
        fargt_betrag:decimal = 0
        add_it:bool = False
        marknr:int = 0

        def generate_inner_output():
            return flodg_betrag, llodg_betrag

        if argtnr == "":
            argtnr = res_line.arrangement

        arrangement = db_session.query(Arrangement).filter(
                (func.lower(Arrangement) == (argtnr).lower())).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == arrangement.argt_artikelnr) &  (Artikel.departement == 0)).first()
        service = 0
        vat = 0

        if artikel:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.service_code)).first()

            if htparam and htparam.fdecimal != 0:
                service = htparam.fdecimal / 100

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == artikel.mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat = htparam.fdecimal / 100

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 479)).first()

            if htparam.flogical:
                vat = vat + vat * service
            vat = round (vat, 2)
        flodg_betrag = zipreis
        llodg_betrag = zipreis * frate
        llodg_betrag = round (llodg_betrag, price_decimal)
        flodg_betrag = round (flodg_betrag, price_decimal)


        return generate_inner_output()

    def usr_prog1(bill_date:date, roomrate:decimal):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        it_exist = False
        prog_str:str = ""
        i:int = 0

        def generate_inner_output():
            return it_exist

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "rate_prog") &  (Reslin_queasy.number1 == resnr) &  (Reslin_queasy.number2 == 0) &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.reslinnr == 1)).first()

        if reslin_queasy:
            prog_str = reslin_queasy.char3

        if prog_str != "":
            OUTPUT STREAM s1 TO ".\\__rate.p"
            for i in range(1,len(prog_str)  + 1) :
            OUTPUT STREAM s1 CLOSE
            compile value (".\\__rate.p")
            dos silent "del .\\__rate.p"

            if not compiler:ERROR:
                roomrate = value(".\\__rate.p") (0, res_line.resnr, res_line.reslinnr, bill_date, roomrate, False)
                it_exist = True


        return generate_inner_output()

    def usr_prog2(bill_date:date, roomrate:decimal):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, res_line, htparam, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal waehrung1, wrung, rguest, argtline


        nonlocal waehrung1, wrung, rguest, argtline

        it_exist = False
        prog_str:str = ""
        i:int = 0

        def generate_inner_output():
            return it_exist

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()

        if queasy:
            prog_str = queasy.char3

        if prog_str != "":
            OUTPUT STREAM s1 TO ".\\__rate.p"
            for i in range(1,len(prog_str)  + 1) :
            OUTPUT STREAM s1 CLOSE
            compile value (".\\__rate.p")
            dos silent "del .\\__rate.p"

            if not compiler:ERROR:
                roomrate = value(".\\__rate.p") (0, res_line.resnr, res_line.reslinnr, bill_date, roomrate, False)
                it_exist = True


        return generate_inner_output()


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == recid_resline)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical
    calc_lodging2()

    return generate_output()