#using conversion tools version: 1.0.0.61

from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servvat import calc_servvat
from sqlalchemy import func
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from functions.ratecode_seek import ratecode_seek
from models import Waehrung, Htparam, Res_line, Guest, Artikel, Guest_pr, Arrangement, Reslin_queasy, Queasy, Katpreis, Pricecod, Argt_line

def get_room_breakdown_big(recid_resline:int, datum:date, curr_i:int, curr_date:date):
    lvcarea:str = "occ-fcast1"
    fnet_lodging = to_decimal("0.0")
    lnet_lodging = to_decimal("0.0")
    net_breakfast = to_decimal("0.0")
    net_lunch = to_decimal("0.0")
    net_dinner = to_decimal("0.0")
    net_others = to_decimal("0.0")
    tot_rmrev = to_decimal("0.0")
    nett_vat = to_decimal("0.0")
    nett_service = to_decimal("0.0")
    exrate:decimal = to_decimal("0.0")
    frate:decimal = to_decimal("0.0")
    price_decimal:int = 0
    new_contrate:bool = False
    bonus_array:List[bool] = create_empty_list(999, False)
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    rm_vat:bool = False
    rm_serv:bool = False
    nett_rmrev:decimal = to_decimal("0.0")
    waehrung = htparam = res_line = guest = artikel = guest_pr = arrangement = reslin_queasy = queasy = katpreis = pricecod = argt_line = None

    waehrung1 = None

    Waehrung1 = create_buffer("Waehrung1",Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, htparam, res_line, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        return {"fnet_lodging": fnet_lodging, "lnet_lodging": lnet_lodging, "net_breakfast": net_breakfast, "net_lunch": net_lunch, "net_dinner": net_dinner, "net_others": net_others, "tot_rmrev": tot_rmrev, "nett_vat": nett_vat, "nett_service": nett_service}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, htparam, res_line, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        rate:decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def calc_lodging2():

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, htparam, res_line, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        qty:int = 0
        fixed_rate:bool = False
        it_exist:bool = False
        rmrate:decimal = to_decimal("0.0")
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
        vat:decimal = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat_art:decimal = to_decimal("0.0")
        service_art:decimal = to_decimal("0.0")
        wrung = None
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
        f_betrag:decimal = to_decimal("0.0")
        argt_betrag:decimal = to_decimal("0.0")
        fcost:decimal = to_decimal("0.0")
        fact:decimal = to_decimal("0.0")
        nett_lamt:decimal = to_decimal("0.0")
        gross_lamt:decimal = to_decimal("0.0")
        tnett_lamt:decimal = to_decimal("0.0")
        nett_lserv:decimal = to_decimal("0.0")
        nett_ltax:decimal = to_decimal("0.0")
        nett_famt:decimal = to_decimal("0.0")
        nett_fserv:decimal = to_decimal("0.0")
        nett_ftax:decimal = to_decimal("0.0")
        price_decimal:int = 0
        argtnr:int = 0
        rguest = None
        tot_fbreakfast:decimal = to_decimal("0.0")
        tot_flunch:decimal = to_decimal("0.0")
        tot_fdinner:decimal = to_decimal("0.0")
        tot_fother:decimal = to_decimal("0.0")
        tot_lbreakfast:decimal = to_decimal("0.0")
        tot_llunch:decimal = to_decimal("0.0")
        tot_ldinner:decimal = to_decimal("0.0")
        tot_lother:decimal = to_decimal("0.0")
        tmp_bezeich:str = ""
        Wrung =  create_buffer("Wrung",Waehrung)
        Rguest =  create_buffer("Rguest",Guest)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 125)).first()

        if htparam:
            bfast_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 126)).first()

        if htparam:
            fb_dept = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 227)).first()

        if htparam:
            lunch_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 228)).first()

        if htparam:
            dinner_art = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 229)).first()

        if htparam:
            lundin_art = htparam.finteger

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == bfast_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and bfast_art != 0:

            return

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == lunch_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and lunch_art != 0:

            return

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == dinner_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and dinner_art != 0:

            return

        artikel = db_session.query(Artikel).filter(
                 (Artikel.zwkum == lundin_art) & (Artikel.departement == fb_dept)).first()

        if not artikel and lundin_art != 0:

            return
        qty1 = res_line.zimmeranz
        rmrate =  to_decimal(res_line.zipreis)
        bill_date = datum

        wrung = db_session.query(Wrung).filter(
                 (Wrung.waehrungsnr == res_line.betriebsnr)).first()

        if wrung:
            exrate =  to_decimal(wrung.ankauf) / to_decimal(wrung.einheit)
        else:
            exrate =  to_decimal("1")

        if res_line.resstatus == 6 and res_line.reserve_dec > 0:
            frate =  to_decimal(res_line.reserve_dec)
        else:
            frate =  to_decimal(exrate)

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == res_line.gastnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        if arrangement:
            service =  to_decimal("0")
            vat =  to_decimal("0")

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()

            if artikel:
                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

            if reslin_queasy:
                fixed_rate = True
                rmrate =  to_decimal(reslin_queasy.deci1)

                if reslin_queasy.number3 != 0:
                    gpax = reslin_queasy.number3

                if reslin_queasy.char1 != "":

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.arrangement == reslin_queasy.char1)).first()

                    if arrangement:
                        argtnr = arrangement.argtnr

            if not fixed_rate:

                if not it_exist:

                    if guest_pr:

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 18) & (Queasy.number1 == res_line.reserve_int)).first()

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

                            katpreis = db_session.query(Katpreis).filter(
                                     (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                            if not katpreis:

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

                            if katpreis and get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2) == rmrate:
                                rack_rate = True

                        elif rack_rate:

                            katpreis = db_session.query(Katpreis).filter(
                                     (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == w_day)).first()

                            if not katpreis:

                                katpreis = db_session.query(Katpreis).filter(
                                         (Katpreis.zikatnr == curr_zikatnr) & (Katpreis.argtnr == arrangement.argtnr) & (Katpreis.startperiode <= bill_date) & (Katpreis.endperiode >= bill_date) & (Katpreis.betriebsnr == 0)).first()

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

                guest_pr = db_session.query(Guest_pr).filter(
                         (Guest_pr.gastnr == rguest.gastnr)).first()

            if guest_pr:
                contcode = guest_pr.code
                ct = res_line.zimmer_wunsch

                if matches(ct,r"*$CODE$*"):
                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                    contcode = substring(ct, 0, get_index(ct, ";") - 1)

                if new_contrate:
                    prcode = get_output(ratecode_seek(res_line.resnr, res_line.reslinnr, contcode, datum))
                else:

                    pricecod = db_session.query(Pricecod).filter(
                             (func.lower(Pricecod.code) == (contcode).lower()) & (Pricecod.marknr == res_line.reserve_int) & (Pricecod.argtnr == arrangement.argtnr) & (Pricecod.zikatnr == curr_zikatnr) & (datum >= Pricecod.startperiode) & (datum <= Pricecod.endperiode)).first()

                    if pricecod:
                        prcode = pricecod._recid
        gross_lamt =  to_decimal("0")

        if argtnr == 0:
            tmp_bezeich = res_line.arrangement

        arrangement = db_session.query(Arrangement).filter(
                 (func.lower(Arrangement.arrangement) == (tmp_bezeich).lower())).first()

        if arrangement:
            argtnr = arrangement.argtnr
        else:
            argtnr = 0

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.argtnr == argtnr)).first()

        if arrangement:

            argt_line_obj_list = []
            for argt_line, artikel in db_session.query(Argt_line, Artikel).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                     (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                if argt_line._recid in argt_line_obj_list:
                    continue
                else:
                    argt_line_obj_list.append(argt_line._recid)


                take_it, f_betrag, argt_betrag, qty = get_argtline_rate(datum, contcode, argt_line._recid)
                service_art =  to_decimal("0")
                vat_art =  to_decimal("0")
                service_art, vat_art = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

                if take_it:
                    nett_lamt = ( to_decimal((argt_betrag)) * to_decimal(qty1) )
                    gross_lamt =  to_decimal(gross_lamt) + to_decimal(((argt_betrag)) * to_decimal(qty1) )
                    nett_lamt =  to_decimal(nett_lamt) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )
                    tnett_lamt =  to_decimal(tnett_lamt) + to_decimal(nett_lamt)
                    nett_famt = ( to_decimal((argt_betrag)) * to_decimal(frate)) * to_decimal(qty1)
                    nett_famt =  to_decimal(nett_famt) / to_decimal((1) + to_decimal(service_art) + to_decimal(vat_art) )

                    if artikel.zwkum == bfast_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_lbreakfast =  to_decimal(tot_lbreakfast) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fbreakfast =  to_decimal(tot_fbreakfast) + to_decimal(nett_famt)

                    elif artikel.zwkum == lunch_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_llunch =  to_decimal(tot_llunch) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_flunch =  to_decimal(tot_flunch) + to_decimal(nett_famt)

                    elif artikel.zwkum == dinner_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_ldinner =  to_decimal(tot_ldinner) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fdinner =  to_decimal(tot_fdinner) + to_decimal(nett_famt)

                    elif artikel.zwkum == lundin_art and (artikel.umsatzart == 3 or artikel.umsatzart >= 5):
                        tot_llunch =  to_decimal(tot_llunch) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_flunch =  to_decimal(tot_flunch) + to_decimal(nett_famt)


                    else:
                        tot_lother =  to_decimal(tot_lother) + to_decimal(nett_lamt) * to_decimal(frate)
                        tot_fother =  to_decimal(tot_fother) + to_decimal(nett_famt)


        rmrate =  to_decimal(rmrate) * to_decimal(qty1)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 127)).first()
        rm_vat = htparam.flogical

        if rm_vat:
            rmrate =  to_decimal(rmrate) - to_decimal(gross_lamt)
            nett_rmrev =  to_decimal(rmrate) / to_decimal((1) + to_decimal(vat) + to_decimal(service) )
            nett_service =  to_decimal(nett_rmrev) * to_decimal(service)
            nett_vat =  to_decimal(nett_rmrev) * to_decimal(vat)


        else:
            rmrate =  to_decimal(rmrate) - to_decimal(tnett_lamt)
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


    def get_argtline_rate(curr_date:date, contcode:str, argt_recid:int):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, htparam, res_line, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal recid_resline, datum, curr_i, waehrung1


        nonlocal waehrung1

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        tmp_betrag:decimal = to_decimal("0.0")
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

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
                     (func.lower(Reslin_queasy.key) == ("fargt-line").lower()) & (Reslin_queasy.char1 == "") & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.number1 == argtline.departement) & (Reslin_queasy.number2 == argtline.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

            if reslin_queasy:

                if reslin_queasy.char2.lower()  != "" and reslin_queasy.char2.lower()  != ("0").lower() :
                    argt_betrag =  to_decimal(res_line.zipreis) * to_decimal(to_int(reslin_queasy.char2)) / to_decimal("100")
                    f_betrag =  to_decimal(argt_betrag)
                else:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("argt-line").lower()) & (func.lower(Reslin_queasy.char1) == (contcode).lower()) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.number3 == argtline.argt_artnr) & (Reslin_queasy.resnr == argtline.departement) & (Reslin_queasy.reslinnr == curr_zikatnr) & (curr_date >= Reslin_queasy.date1) & (curr_date <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                    waehrung1 = db_session.query(Waehrung1).filter(
                             (Waehrung1.waehrungsnr == res_line.betriebsnr)).first()

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.argtnr == argt_line.argtnr)).first()

            waehrung = db_session.query(Waehrung).filter(
                     (Waehrung.waehrungsnr == arrangement.betriebsnr)).first()
            f_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)

            if argt_betrag > 0:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)
            else:
                tmp_betrag =  -1 * to_decimal(argt_betrag)
                argt_betrag = ( to_decimal(res_line.zipreis) * to_decimal((tmp_betrag) / to_decimal(100))) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, htparam, res_line, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal recid_resline, datum, curr_i, waehrung1


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


    def get_lodging(argtnr:int, zipreis:decimal, bill_date:date):

        nonlocal lvcarea, fnet_lodging, lnet_lodging, net_breakfast, net_lunch, net_dinner, net_others, tot_rmrev, nett_vat, nett_service, exrate, frate, price_decimal, new_contrate, bonus_array, wd_array, rm_vat, rm_serv, nett_rmrev, waehrung, htparam, res_line, guest, artikel, guest_pr, arrangement, reslin_queasy, queasy, katpreis, pricecod, argt_line
        nonlocal recid_resline, datum, curr_i, curr_date
        nonlocal waehrung1


        nonlocal waehrung1

        flodg_betrag = to_decimal("0.0")
        llodg_betrag = to_decimal("0.0")
        service:decimal = to_decimal("0.0")
        vat:decimal = to_decimal("0.0")
        qty:int = 0
        argt_betrag:decimal = to_decimal("0.0")
        fargt_betrag:decimal = to_decimal("0.0")
        add_it:bool = False
        marknr:int = 0
        tmp_bez:str = ""

        def generate_inner_output():
            return (flodg_betrag, llodg_betrag)


        if argtnr == 0:
            tmp_bez = res_line.arrangement

        arrangement = db_session.query(Arrangement).filter(
                 (func.lower(Arrangement.arrangement) == (tmp_bez).lower())).first()

        if arrangement:
            argtnr = arrangement.argtnr
        else:
            argtnr = 0

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.argtnr == argtnr)).first()

        if arrangement:
            service =  to_decimal("0")
            vat =  to_decimal("0")

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artnr == arrangement.argt_artikelnr) & (Artikel.departement == 0)).first()

            if artikel:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == artikel.service_code)).first()

                if htparam and htparam.fdecimal != 0:
                    service =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == artikel.mwst_code)).first()

                if htparam and htparam.fdecimal != 0:
                    vat =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 479)).first()

                if htparam.flogical:
                    vat =  to_decimal(vat) + to_decimal(vat) * to_decimal(service)
                vat =  to_decimal(round (vat , 2))
        flodg_betrag =  to_decimal(zipreis)
        llodg_betrag =  to_decimal(zipreis) * to_decimal(frate)
        llodg_betrag =  to_decimal(round (llodg_betrag , price_decimal))
        flodg_betrag =  to_decimal(round (flodg_betrag , price_decimal))

        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()

    if htparam:
        price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam:

        if htparam.feldtyp == 4:
            new_contrate = htparam.flogical

    res_line = db_session.query(Res_line).filter(
             (Res_line._recid == recid_resline)).first()

    if res_line:
        calc_lodging2()

    return generate_output()