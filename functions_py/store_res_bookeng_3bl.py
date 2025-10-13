#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 09-10-2025
# Tiket ID : 8CF423 | Recompile program
# Issue : Fixing lowercase detres
# =======================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.global_allotment_number import global_allotment_number
from functions.intevent_1 import intevent_1
from functions.calc_servvat import calc_servvat
from functions.count_availability import count_availability
from functions.find_dyna_ratecodesm import find_dyna_ratecodesm
from functions.ratecode_rate import ratecode_rate
from functions.calc_dynaratessm import calc_dynaratessm
from models import Guest, Ratecode, Guestseg, Nation, Queasy, Reservation, Res_line, Htparam, Zimkateg, Artikel, Mc_guest, Arrangement, Waehrung, Reslin_queasy, Guest_pr, Pricecod, Resplan

res_info_data, Res_info = create_model("Res_info", {"res_time":string, "res_id":string, "ota_code":string, "no_room":int, "rate_code":string, "room_type":string, "ci_date":date, "co_date":date, "amount":string, "curr":string, "adult":string, "child1":string, "child2":string, "remark":string, "eta":string, "given_name":string, "sure_name":string, "phone":string, "email":string, "address1":string, "address2":string, "city":string, "zip":string, "state":string, "country":string, "commission":string, "night":int, "amount_at":string, "curr_at":string, "argtnr":string, "uniq_id":string, "card_info":string})
detres_data, Detres = create_model("Detres", {"reslinnr":int, "amount":string, "adult":int, "child1":int, "child2":int, "room_type":string, "rate_code":string, "ci_date":date, "co_date":date, "argtnr":string, "zikatnr":int, "firstname":string, "lastname":string, "selected":bool})

def store_res_bookeng_3bl(res_info_data:[Res_info], detres_data:[Detres], res_mode:string, dyna_code:string, becode:int, new_resno:int, chdelimeter:string, chdelimeter1:string, chdelimeter2:string, chdelimeter3:string, t_guest_nat:string, t_curr_name:string):

    prepare_cache ([Guest, Ratecode, Guestseg, Nation, Queasy, Htparam, Zimkateg, Artikel, Arrangement, Waehrung, Reslin_queasy, Guest_pr, Pricecod, Resplan])

    error_str = ""
    done = False
    # response:string = ""
    response:string = ""
    curr_date:date = None
    exist:bool = False
    expired:bool = False
    curr_error_str:string = ""
    cm_gastno:int = 0
    inp_resno:int = 0
    ota_gastnr:int = 0
    rsegcode:int = 0
    resart:int = 0
    gastnrmember:int = 1
    rsegm:int = 0
    resstatus:int = 1
    i:int = 1
    markno:int = 0
    argtno:int = 0
    zikatno:int = 0
    currno:int = 0
    rm_qty:int = 0
    cm_name:string = ""
    card_name:string = ""
    card_no:string = ""
    argt:string = ""
    ratecode1:string = ""
    guest_nat:string = ""
    eta_char:string = ""
    hh:string = ""
    mm:string = ""
    bookingid:string = ""
    avail_gdpr:bool = False
    curr_nat:string = ""
    do_it:bool = False
    card_exist:bool = False
    new_contrate:bool = False
    restricted_disc:bool = False
    use_it:bool = False
    ci_rate:Decimal = to_decimal("0.0")
    ci_rate1:Decimal = to_decimal("0.0")
    room_price:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    city_str:string = ""
    curr_i:int = 0
    globekey_rsv:bool = False
    globekey_tot_amount:Decimal = to_decimal("0.0")
    tot_rmrate_vhp:Decimal = to_decimal("0.0")
    asc_str:string = ""
    rmtype:string = ""
    tmp_given_name:string = ""
    tmp_email:string = ""
    tmp_sure_name:string = ""
    tmp_adress1:string = ""
    tmp_adress2:string = ""
    tmp_country:string = ""
    tmp_phone:string = ""
    tmp_city:string = ""
    tmp_zip:string = ""
    tgastnrmember:int = 0
    tot_guest:int = 1
    curri:int = 0
    str_tot_guest:string = ""
    c_number:string = ""
    c_code:string = ""
    c_exp:string = ""
    c_info:string = ""
    avail_room:int = 0
    avail_rmtype:int = 0
    counter:int = 0
    m:int = 0
    yy:int = 0
    dd:int = 0
    date_str:string = ""
    bill_date:date = None
    upto_date:date = None
    zikatnr:int = 0
    cat_flag:bool = False
    n:int = 0
    j:int = 0
    tax_included:bool = False
    default_country:string = "INA"
    guest = ratecode = guestseg = nation = queasy = reservation = res_line = htparam = zimkateg = artikel = mc_guest = arrangement = waehrung = reslin_queasy = guest_pr = pricecod = resplan = None

    detres = room_avail_list = rate_list = rate_list2 = res_info = nation_list = rgast = bratecode = bguestseg = nationbuf = qsy6 = bres = bres_line = rqueasy = qsy = bqueasy = None

    room_avail_list_data, Room_avail_list = create_model("Room_avail_list", {"zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":int, "bezeich":string, "room":int, "troom":int, "datum":date}, {"sleeping": True})
    rate_list_data, Rate_list = create_model("Rate_list", {"datum":date, "currency":string, "rmrate":Decimal, "updateflag":bool, "occ_rooms":int, "rcode":string, "rcmap":string, "room_type":string})
    rate_list2_data, Rate_list2 = create_model_like(Rate_list)
    nation_list_data, Nation_list = create_model("Nation_list", {"nat_nr":int, "nat_abbr":string, "nat_desc":string})

    Rgast = create_buffer("Rgast",Guest)
    Bratecode = create_buffer("Bratecode",Ratecode)
    Bguestseg = create_buffer("Bguestseg",Guestseg)
    Nationbuf = create_buffer("Nationbuf",Nation)
    Qsy6 = create_buffer("Qsy6",Queasy)
    Bres = create_buffer("Bres",Reservation)
    Bres_line = create_buffer("Bres_line",Res_line)
    Rqueasy = create_buffer("Rqueasy",Queasy)
    Qsy = create_buffer("Qsy",Queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        return {"error_str": error_str, "done": done}

    def add_resline():

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        new_reslinno:int = 1
        allotnr:int = 0
        statcode:string = ""
        res_statcode:string = ""
        bufguest = None
        guestbuff = None
        mcguestbuf = None
        Bufguest =  create_buffer("Bufguest",Guest)
        Guestbuff =  create_buffer("Guestbuff",Guest)
        Mcguestbuf =  create_buffer("Mcguestbuf",Mc_guest)

        if new_contrate:
            statcode, res_statcode = create_new_fixrate(new_resno, detres.reslinnr)
        else:
            create_fixed_rate(new_resno, detres.reslinnr)

        if res_info.eta != "":
            hh = entry(0, res_info.eta, ":")
            mm = entry(1, res_info.eta, ":")
            eta_char = hh + mm
        else:
            eta_char = "0000"
        allotnr = get_output(global_allotment_number(cm_gastno, ota_gastnr, detres.ci_date, detres.co_date, rmtype))

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

        if zimkateg:
            zikatno = zimkateg.zikatnr

        bufguest = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})
        res_line = Res_line()
        db_session.add(res_line)

        res_line.resnr = new_resno
        res_line.reslinnr = detres.reslinnr
        res_line.gastnr = ota_gastnr
        res_line.gastnrmember = gastnrmember
        res_line.gastnrpay = ota_gastnr
        res_line.ankunft = detres.ci_date
        res_line.abreise = detres.co_date
        res_line.anztage = detres.co_date - detres.ci_date
        res_line.flight_nr = " " + to_string(eta_char, "x(5)") +\
                " "
        res_line.name = bufguest.name + ", " + bufguest.vorname1 +\
                ", " + bufguest.anrede1
        res_line.arrangement = argt
        res_line.resstatus = resstatus
        res_line.erwachs = detres.adult
        res_line.kind1 = detres.child1
        res_line.kind2 = detres.child2
        res_line.betriebsnr = currno
        res_line.bemerk = res_info.remark + chdelimeter1 +\
                "TIME," + res_info.res_time
        res_line.zimmeranz = 1
        res_line.zikatnr = zikatno
        res_line.zipreis =  to_decimal(ci_rate1)
        res_line.was_status = 1
        res_line.reserve_char = to_string(get_year(get_current_date()) - 2000, "99") + "/" +\
                to_string(get_month(get_current_date()) , "99") + "/" +\
                to_string(get_day(get_current_date()) , "99") +\
                to_string(get_current_time_in_seconds(), "hh:mm") +\
                "**"
        res_line.reserve_int = markno

        if resstatus == 1:
            res_line.kontignr = allotnr

        if new_contrate:
            res_line.zimmer_wunsch = "ebdisc;restricted;date," + to_string(get_year(curr_date)) + to_string(get_month(curr_date) , "99") + to_string(get_day(curr_date) , "99") + ";" + "voucher" + bookingid + ";" + "$CODE$" + res_statcode + ";" + "$OrigCode$" + detres.rate_code + ";"

        if avail_gdpr:

            guestbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guestbuff:

                mcguestbuf = db_session.query(Mcguestbuf).filter(
                         (Mcguestbuf.gastnr == res_line.gastnrmember)).first()

                if mcguestbuf:
                    do_it = False

                if guestbuff.land != " ":
                    curr_nat = guestbuff.land

                elif guestbuff.nation1 != " ":
                    curr_nat = guestbuff.nation1

                nation_list = query(nation_list_data, filters=(lambda nation_list: nation_list.nat_abbr.lower()  == (curr_nat).lower()), first=True)

                if nation_list:
                    do_it = True
                else:
                    do_it = False

                if do_it:

                    if not matches(res_line.zimmer_wunsch,r"*GDPR*"):
                        res_line.zimmer_wunsch = res_line.zimmer_wunsch + "GDPRyes;"
        rm_qty = res_line.zimmeranz
        pass
        get_output(intevent_1(12, "", "Priscilla", new_resno, detres.reslinnr))
        create_resplan()
        create_reslog()
        error_str = error_str + "CUR" + chdelimeter1 + to_string(res_line.betriebsnr)
        pass


    def create_new_fixrate(resno:int, reslinno:int):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        statcode = ""
        res_statcode = ""
        rate_found:bool = False
        rmrate:Decimal = to_decimal("0.0")
        kback_flag:bool = False
        n:int = 0
        ratecode_curr:string = ""
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        ratecode_frate:Decimal = 1
        sm_frate:Decimal = 1
        currno_sm:int = 0
        check_arg:bool = False

        def generate_inner_output():
            return (statcode, res_statcode)


        if detres.ci_date == detres.co_date:
            upto_date = detres.co_date
        else:
            upto_date = detres.co_date - timedelta(days=1)

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, detres.argtnr)]})

        if arrangement:
            argtno = arrangement.argtnr
        for bill_date in date_range(detres.ci_date,upto_date) :
            n = n + 1
            currno = 0
            markno = 0

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

            if artikel:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            if num_entries(detres.amount, "-") >= 1:
                room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , detres.amount , "-")))
            else:
                room_price =  to_decimal(to_decimal(detres.amount))
            ci_rate =  to_decimal(room_price)

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, res_info.curr)]})

            if not waehrung:

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, t_curr_name)]})

            if waehrung:
                currno_sm = waehrung.waehrungsnr

            rqueasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, detres.rate_code)]})

            if not rqueasy:
                detres.rate_code = dyna_code

            if cat_flag:

                queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, detres.room_type)]})

                if queasy:
                    room_avail_list_data = get_output(count_availability(bill_date))
                    avail_room = 0
                    avail_rmtype = 0

                    for room_avail_list in query(room_avail_list_data, filters=(lambda room_avail_list: room_avail_list.i_typ == queasy.number1), sort_by=[("room",False)]):

                        if room_avail_list.room >= avail_room:
                            avail_room = room_avail_list.room
                            avail_rmtype = room_avail_list.zikatnr

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, avail_rmtype)]})

                    if not zimkateg:

                        zimkateg = get_cache (Zimkateg, {"typ": [(eq, queasy.number1)]})
                    rmtype = zimkateg.kurzbez

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, queasy.number1)],"char1": [(eq, detres.rate_code)]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            pass
                            bqueasy.logi2 = True
                            pass
                            pass

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, queasy.number1)],"char1": [(eq, "")]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            pass
                            bqueasy.logi2 = True
                            pass
                            pass
            else:

                zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, detres.room_type)]})

                if zimkateg:
                    rmtype = zimkateg.kurzbez
                else:
                    rmtype = detres.room_type

                qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zimkateg.zikatnr)],"char1": [(eq, detres.rate_code)]})

                if qsy and qsy.logi1 == False and qsy.logi2 == False:

                    bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                    if bqueasy:
                        pass
                        bqueasy.logi2 = True
                        pass
                        pass

                qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zimkateg.zikatnr)],"char1": [(eq, "")]})

                if qsy and qsy.logi1 == False and qsy.logi2 == False:

                    bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                    if bqueasy:
                        pass
                        bqueasy.logi2 = True
                        pass
                        pass
            statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, rmtype, detres.adult, detres.child1, room_price, detres.rate_code, argtno))

            if n == 1:
                res_statcode = statcode

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, markno)]})

            if queasy and queasy.char3 != "":

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})

                if waehrung:
                    currno = waehrung.waehrungsnr

            if currno_sm != currno and currno != 0:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, currno)],"betriebsnr": [(eq, 0)]})

                if waehrung:
                    ratecode_frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, res_info.curr)],"betriebsnr": [(eq, 0)]})

                if waehrung:
                    sm_frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                ci_rate =  to_decimal(ci_rate) * to_decimal((sm_frate) / to_decimal(ratecode_frate))
                ci_rate = to_decimal(round(ci_rate , price_decimal))

                rqueasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, detres.rate_code)]})

                if not rqueasy:
                    detres.rate_code = dyna_code
                statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, rmtype, detres.adult, detres.child1, ci_rate, detres.rate_code, argtno))

                if n == 1:
                    res_statcode = statcode

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

            if zimkateg:
                zikatno = zimkateg.zikatnr

            if argtno == 0:

                ratecode = get_cache (Ratecode, {"code": [(eq, detres.rate_code)],"zikatnr": [(eq, zikatno)]})

                if not ratecode:
                    error_str = error_str + "Arrangement Not Found " + detres.rate_code + " " + to_string(zikatno)

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 151)]})

                    if htparam.fchar != "":

                        arrangement = get_cache (Arrangement, {"arrangement": [(eq, htparam.fchar)]})

                        if arrangement:
                            argt = arrangement.arrangement
                        else:
                            check_arg = True
                    else:
                        check_arg = True

                    if check_arg:

                        arrangement = get_cache (Arrangement, {"segmentcode": [(eq, 0)]})
                        argt = arrangement.arrangement

            elif markno == 0:
                error_str = error_str + "Market Segment Not Found."

            if currno == 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

                if htparam:

                    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

                    if not waehrung:

                        waehrung = db_session.query(Waehrung).first()
                    currno = waehrung.waehrungsnr

            if argtno != 0:

                arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

                if arrangement:
                    argt = arrangement.arrangement
            rate_found, rmrate, restricted_disc, kback_flag = get_output(ratecode_rate(True, True, resno, reslinno, ("!" + statcode), curr_date, bill_date, detres.ci_date, detres.co_date, markno, argtno, zikatno, detres.adult, detres.child1, detres.child2, 0, currno))
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "arrangement"
            reslin_queasy.resnr = resno
            reslin_queasy.reslinnr = reslinno
            reslin_queasy.date1 = bill_date
            reslin_queasy.date2 = bill_date
            reslin_queasy.deci1 =  to_decimal(ci_rate)
            reslin_queasy.char1 = argt
            reslin_queasy.char2 = statcode


            pass

            if bill_date == detres.ci_date:
                ci_rate1 =  to_decimal(ci_rate)

        return generate_inner_output()


    def create_fixed_rate(resno:int, reslinno:int):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        bill_date:date = None

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, ota_gastnr)]})

        if not guest_pr:
            error_str = error_str + "Guest PR not available for gastnr" + to_string(ota_gastnr) + "."

            return

        ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)]})

        if ratecode:
            markno = ratecode.marknr
            argtno = ratecode.argtnr

        if argtno == 0:
            error_str = error_str + "Arrangement not available"

            return
        else:

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

            if arrangement:
                argt = arrangement.arrangement
        for bill_date in date_range(detres.ci_date,detres.co_date) :

            pricecod = get_cache (Pricecod, {"code": [(eq, guest_pr.code)],"marknr": [(eq, markno)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, zikatno)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)]})

            if pricecod:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = resno
                reslin_queasy.reslinnr = reslinno
                reslin_queasy.date1 = bill_date
                reslin_queasy.date2 = bill_date
                reslin_queasy.deci1 =  to_decimal(pricecod.perspreis[detres.adult - 1] +\
                        pricecod.kindpreis[0]) * to_decimal(detres.child1)
                reslin_queasy.char1 = argt


                pass
                
                # Rulita | Missing detres.ci_date
                if bill_date == detres.ci_date:
                    ci_rate =  to_decimal(reslin_queasy.deci1)


    def create_reslog():

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        guest1 = None
        cid:string = " "
        cdate:string = " "
        Guest1 =  create_buffer("Guest1",Guest)
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = res_line.resnr
        reslin_queasy.reslinnr = res_line.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()
        reslin_queasy.char3 = to_string(res_line.ankunft) + ";" +\
                to_string(res_line.ankunft) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.zimmeranz, ">>9") + ";" +\
                to_string(res_line.zimmeranz, ">>9") + ";" +\
                to_string(res_line.erwachs, ">9") + ";" +\
                to_string(res_line.erwachs, ">9") + ";" +\
                to_string(res_line.kind1, ">9") + ";" +\
                to_string(res_line.kind1, ">9") + ";" +\
                to_string(res_line.gratis, ">9") + ";" +\
                to_string(res_line.gratis, ">9") + ";" +\
                to_string(res_line.zikatnr, ">>9") + ";" +\
                to_string(res_line.zikatnr, ">>9") + ";" +\
                to_string(res_line.zinr, "x(4)") + ";" +\
                to_string(res_line.zinr, "x(4)") + ";" +\
                to_string(res_line.arrangement, "x(5)") + ";" +\
                to_string(res_line.arrangement, "x(5)") + ";" +\
                to_string(res_line.zipreis, ">,>>>,>>9.99") + ";" +\
                to_string(res_line.zipreis, ">,>>>,>>9.99") + ";" +\
                to_string("**", "x(2)") + ";" +\
                to_string("**", "x(2)") + ";" +\
                to_string(get_current_date()) + ";" +\
                to_string(get_current_date()) + ";" +\
                to_string(res_line.name, "x(16)") + ";" +\
                to_string("New Reservation", "x(16)") + ";" +\
                to_string("YES", "x(3)") + ";" +\
                to_string("YES", "x(3)")


        pass
        pass


    def create_resplan():

        nonlocal error_str, done, response, response, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        curr_date:date = None

        if res_line.ankunft == res_line.abreise:
            upto_date = res_line.abreise
        else:
            upto_date = res_line.abreise - timedelta(days=1)
        for curr_date in date_range(res_line.ankunft,upto_date) :

            resplan = get_cache (Resplan, {"zikatnr": [(eq, res_line.zikatnr)],"datum": [(eq, curr_date)]})

            if resplan:
                pass
                resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + res_line.zimmeranz
                pass
                pass
            else:
                resplan = Resplan()
                db_session.add(resplan)

                resplan.datum = curr_date
                resplan.zikatnr = res_line.zikatnr
                resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + res_line.zimmeranz


    def calc_commisions(room_price:Decimal):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        ccommission:string = "0"
        dcommission:Decimal = 0
        decs:Decimal = 0
        points:string = ""

        def generate_inner_output():
            return (room_price)

        ccommission = res_info.commission

        if matches(ccommission,r"*%*"):
            ccommission = trim(replace_str(ccommission, "%", ""))

        if matches(ccommission,r"*,*"):
            decs =  to_decimal(to_decimal(entry(0 , ccommission , ",")) )
            points = entry(1, ccommission, ",")

        elif matches(ccommission,r"*.*") and num_entries(ccommission, ".") >= 2:
            decs =  to_decimal(to_decimal(entry(0 , ccommission , ".")) )
            points = entry(1, ccommission, ".")


        else:
            decs =  to_decimal(to_decimal(ccommission) )
            points = "0"


        dcommission = decs + (to_decimal(substring(points, 0, 1)) / 10) + (to_decimal(substring(points, 1, 1)) / 100) + (to_decimal(substring(points, 2, 1)) / 1000)
        room_price = to_decimal(round(room_price * (1 + (dcommission / 100)) , 2))

        return generate_inner_output()


    def check_vhp_rsv():

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        bill_date:date = None
        statcode:string = ""
        for bill_date in date_range(res_info.ci_date,res_info.co_date) :
            statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, detres.room_type, 1, 1, globekey_tot_amount, detres.rate_code, argtno))
            rate_list2_data = get_output(calc_dynaratessm(bill_date, bill_date, cm_gastno, detres.rate_code, zikatno, argtno, 1, 1))

            for rate_list2 in query(rate_list2_data):
                rate_list = Rate_list()
                rate_list_data.append(rate_list)

                buffer_copy(rate_list2, rate_list)

        for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.room_type == detres.room_type and rate_list.datum >= detres.ci_date and rate_list.datum < detres.co_date)):
            tot_rmrate_vhp =  to_decimal(tot_rmrate_vhp) + to_decimal(rate_list.rmrate)


    def chk_ascii(str1:string):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, cm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, cm_name, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, rmtype, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, c_number, c_code, c_exp, c_info, avail_room, avail_rmtype, counter, m, yy, dd, date_str, bill_date, upto_date, zikatnr, cat_flag, n, j, tax_included, default_country, guest, ratecode, guestseg, nation, queasy, reservation, res_line, htparam, zimkateg, artikel, mc_guest, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal detres, room_avail_list, rate_list, rate_list2, res_info, nation_list, rgast, bratecode, bguestseg, nationbuf, qsy6, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        str2 = ""
        curr_i:int = 0

        def generate_inner_output():
            return (str2)

        str2 = ""
        for curr_i in range(1,length(str1)  + 1) :

            if asc(substring(str1, curr_i - 1, 1)) == 10:
                str2 = str2 + "-"

            elif asc(substring(str1, curr_i - 1, 1)) < 32:
                str2 = str2 + "-"

            elif asc(substring(str1, curr_i - 1, 1)) == 233 or asc(substring(str1, curr_i, 1)) == 232:
                str2 = str2 + "e"

            elif asc(substring(str1, curr_i - 1, 1)) == 252 or asc(substring(str1, curr_i, 1)) == 250:
                str2 = str2 + "u"

            elif asc(substring(str1, curr_i - 1, 1)) == 209:
                str2 = str2 + "n"

            elif asc(substring(str1, curr_i - 1, 1)) == 225 or asc(substring(str1, curr_i, 1)) == 228:
                str2 = str2 + "a"

            elif asc(substring(str1, curr_i - 1, 1)) == 160:
                str2 = str2 + " "

            elif asc(substring(str1, curr_i - 1, 1)) == 243:
                str2 = str2 + "o"

            elif asc(substring(str1, curr_i - 1, 1)) == 241:
                str2 = str2 + "n"

            elif asc(substring(str1, curr_i - 1, 1)) > 127 or asc(substring(str1, curr_i, 1)) < 32:
                str2 = str2 + "-"
            else:
                str2 = str2 + substring(str1, curr_i - 1, 1)

        return generate_inner_output()

    # if substring(proversion(), 0, 1) == ("1").lower() :
    #     &elseif substring(proversion(), 0, 1) = "9" THEN

    if becode == 0:

        htparam = get_cache (Htparam, {"paramgruppe": [(eq, 40)],"paramnr": [(eq, 42)]})
        cm_gastno = htparam.finteger
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

        if queasy:
            cm_gastno = queasy.number2
            cm_name = queasy.char1

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 67)]})

    if htparam:
        rsegcode = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 69)]})

    if htparam:
        resart = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})

    if htparam:
        tax_included = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    if htparam:
        default_country = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 953)]})

    if htparam:

        if htparam.flogical  and not htparam.bezeichnung.lower()  == ("Not Used").lower() :
            resstatus = 5
        else:
            resstatus = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 346)]})

    if htparam:
        avail_gdpr = htparam.flogical

    if avail_gdpr:

        nationbuf_obj_list = {}
        nationbuf = Nation()
        qsy6 = Queasy()
        for nationbuf.kurzbez, nationbuf._recid, nationbuf.nationnr, nationbuf.bezeich, qsy6.number1, qsy6.char3, qsy6.number2, qsy6.char1, qsy6._recid, qsy6.logi2, qsy6.logi1 in db_session.query(Nationbuf.kurzbez, Nationbuf._recid, Nationbuf.nationnr, Nationbuf.bezeich, Qsy6.number1, Qsy6.char3, Qsy6.number2, Qsy6.char1, Qsy6._recid, Qsy6.logi2, Qsy6.logi1).join(Qsy6,(Qsy6.key == 6) & (Qsy6.number1 == Nationbuf.untergruppe) & (matches(Qsy6.char1,"*europe*"))).filter(
                 (Nationbuf.natcode == 0)).order_by(Nationbuf.kurzbez).all():
            if nationbuf_obj_list.get(nationbuf._recid):
                continue
            else:
                nationbuf_obj_list[nationbuf._recid] = True


            nation_list = Nation_list()
            nation_list_data.append(nation_list)

            nation_list.nat_nr = nationbuf.nationnr
            nation_list.nat_abbr = nationbuf.kurzbez
            nation_list.nat_desc = entry(0, nationbuf.bezeich, ";")

    res_info = query(res_info_data, first=True)

    if res_info:

        guest = db_session.query(Guest).filter(
                 (matches(trim(entry(0, Guest.steuernr, "-")),trim(res_info.ota_code)))).first()

        if guest and num_entries(guest.steuernr, "-") == 2:
            res_info.commission = entry(1, guest.steuernr, "-")
        else:
            res_info.commission = "0"
        asc_str = chk_ascii(res_info.sure_name)
        res_info.sure_name = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.city)
        res_info.city = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.given_name)
        res_info.given_name = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.address1)
        res_info.address1 = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.address2)
        res_info.address2 = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.city)
        res_info.city = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.remark)
        res_info.remark = asc_str
        asc_str = ""
        asc_str = chk_ascii(res_info.email)
        res_info.email = asc_str
        asc_str = ""
        pass

    res_info = query(res_info_data, first=True)

    if res_info:

        rgast = db_session.query(Rgast).filter(
                 (matches(trim(entry(0, Rgast.steuernr, "|")),trim(res_info.ota_code)))).first()

        if not rgast:
            error_str = error_str + "Reservation TA File not found for : " + trim(res_info.ota_code) + ". "

            rgast = get_cache (Guest, {"gastnr": [(eq, cm_gastno)]})

            if rgast:
                ota_gastnr = rgast.gastnr
        else:
            ota_gastnr = rgast.gastnr
        bookingid = res_info.uniq_id

        if res_info.ci_date < curr_date:
            done = True
            expired = True
            error_str = error_str + "expired, Reservation Check In Date is Less than Current Check In System Date"

        if expired:

            return generate_output()

        if res_mode.lower()  == ("new").lower() :

            reservation = get_cache (Reservation, {"vesrdepot": [(eq, bookingid)],"gastnr": [(eq, ota_gastnr)]})

            res_line = db_session.query(Res_line).filter(
                     (Res_line.gastnr == ota_gastnr) & (matches(Res_line.zimmer_wunsch,"*voucher" + bookingid + "*"))).first()

            if reservation or res_line:
                error_str = error_str + chr_unicode(10) + "Reservation " + res_info.uniq_id + " already exist."


                exist = True
                done = True

                return generate_output()

            if exist:

                return generate_output()
            for j in range(1,num_entries(res_info.room_type, ";") - 1 + 1) :

                if cat_flag:

                    queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, entry(j - 1, res_info.room_type, ";"))]})

                    if not queasy:
                        error_str = error_str + chr_unicode(10) + res_info.room_type + "No such Room Category"

                        return generate_output()
                else:

                    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, entry(j - 1, res_info.room_type, ";"))]})

                    if not zimkateg:
                        error_str = error_str + chr_unicode(10) + res_info.room_type + "No such Room Category"

                        return generate_output()
                for i in range(1,to_int(entry(j - 1, res_info.res_id, ";"))  + 1) :
                    counter = counter + 1
                    detres = Detres()
                    detres_data.append(detres)

                    detres.reslinnr = counter
                    detres.rate_code = entry(j - 1, res_info.rate_code, ";")
                    detres.adult = to_int(entry(j - 1, res_info.adult, ";"))
                    detres.amount = entry(j - 1, res_info.amount, ";")
                    detres.room_type = entry(j - 1, res_info.room_type, ";")

                    if res_info.child1 != "":
                        detres.child1 = to_int(entry(j - 1, res_info.child1, ";"))

                    if res_info.amount_at == "":
                        detres.ci_date = res_info.ci_date
                    else:
                        date_str = entry(j - 1, res_info.amount_at, ";")

                        if matches(date_str,r"*" + chr_unicode(45) + r"*"):
                            yy = to_int(entry(0, date_str, "-"))
                            m = to_int(entry(1, date_str, "-"))
                            dd = to_int(entry(2, date_str, "-"))

                        elif matches(date_str,r"*" + chr_unicode(47) + r"*"):
                            yy = to_int(entry(0, date_str, "/"))
                            m = to_int(entry(1, date_str, "/"))
                            dd = to_int(entry(2, date_str, "/"))


                        else:
                            error_str = error_str + chr_unicode(10) + to_string(res_info.amount_at) + ", " + date_str + "C/i date format is invalid"

                            return generate_output()
                        detres.ci_date = date_mdy(m, dd, yy)

                    if res_info.curr_at == "":
                        detres.co_date = res_info.co_date
                    else:
                        date_str = entry(j - 1, res_info.curr_at, ";")

                        if matches(date_str,r"*" + chr_unicode(45) + r"*"):
                            yy = to_int(entry(0, date_str, "-"))
                            m = to_int(entry(1, date_str, "-"))
                            dd = to_int(entry(2, date_str, "-"))

                        elif matches(date_str,r"*" + chr_unicode(47) + r"*"):
                            yy = to_int(entry(0, date_str, "/"))
                            m = to_int(entry(1, date_str, "/"))
                            dd = to_int(entry(2, date_str, "/"))


                        else:
                            error_str = error_str + chr_unicode(10) + to_string(res_info.curr_at) + ", " + date_str + "C/O date format is invalid"

                            return generate_output()
                        detres.co_date = date_mdy(m, dd, yy)

                    if matches(res_info.argtnr,r"*" + r";" + r"*"):

                        if num_entries(res_info.room_type, ";") == num_entries(res_info.argtnr, ";"):
                            detres.argtnr = entry(j - 1, res_info.argtnr, ";")
                        else:
                            detres.argtnr = entry(num_entries(res_info.argtnr, ";") - 1 - 1, res_info.argtnr, ";")
                    else:
                        detres.argtnr = res_info.argtnr
        pass

        if res_info.email != "":

            guest = db_session.query(Guest).filter(
                     ((Guest.vorname1 == res_info.given_name) & (Guest.email_adr == res_info.email) & (Guest.name == res_info.sure_name)) | ((Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name) & (Guest.adresse1 == res_info.address1))).first()
        else:

            guest = get_cache (Guest, {"name": [(eq, res_info.sure_name)],"vorname1": [(eq, res_info.given_name)],"adresse1": [(eq, res_info.address1)]})

        if not guest:

            if res_info.country == "" or res_info.country == " ":
                res_info.country = default_country

            nation = get_cache (Nation, {"bezeich": [(eq, res_info.country)]})

            if nation:
                t_guest_nat = nation.kurzbez
            else:

                nation = get_cache (Nation, {"kurzbez": [(eq, res_info.country)]})

                if nation:
                    t_guest_nat = nation.kurzbez
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, t_guest_nat)]})

                    if nation:
                        t_guest_nat = nation.kurzbez
                    else:

                        nation = db_session.query(Nation).filter(
                                 (matches(Nation.bezeich,"*Unknown*"))).first()

                        if nation:
                            t_guest_nat = nation.kurzbez
                        else:
                            error_str = error_str + chr_unicode(10) + "Unknown country not defined."
                            done = False

                            return generate_output()

            guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

            if guest:
                gastnrmember = guest.gastnr + 1
            guest = Guest()
            db_session.add(guest)

            guest.gastnr = gastnrmember
            guest.name = res_info.sure_name
            guest.vorname1 = res_info.given_name
            guest.adresse1 = res_info.address1
            guest.adresse2 = res_info.address2
            guest.wohnort = res_info.city
            guest.land = t_guest_nat
            guest.plz = res_info.zip
            guest.email_adr = res_info.email
            guest.telefon = res_info.phone
            guest.nation1 = t_guest_nat

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, ota_gastnr)],"reihenfolge": [(eq, 1)]})

            if guestseg:
                rsegm = guestseg.segmentcode

                bguestseg = get_cache (Guestseg, {"gastnr": [(eq, gastnrmember)],"segmentcode": [(eq, rsegm)],"reihenfolge": [(eq, 1)]})

                if not bguestseg:
                    guestseg = Guestseg()
                    db_session.add(guestseg)

                    guestseg.gastnr = gastnrmember
                    guestseg.reihenfolge = 1
                    guestseg.segmentcode = rsegm


        else:
            gastnrmember = guest.gastnr
        pass
        for i in range(1,num_entries(res_info.card_info, ";")  + 1) :
            c_info = entry(i - 1, res_info.card_info, ";")

            if c_info != "" and num_entries(c_info, ":") > 1:

                if entry(0, c_info, ":") == ("number").lower() :
                    c_number = entry(1, c_info, ":")

                elif entry(0, c_info, ":") == ("exp").lower() :
                    c_exp = entry(1, c_info, ":")

                elif entry(0, c_info, ":") == ("code").lower() :
                    c_code = entry(1, c_info, ":")

        if c_number != "":

            artikel = db_session.query(Artikel).filter(
                     (Artikel.artart == 7) & (matches(Artikel.bezeich,"*" + cm_name + "*"))).first()

            if not artikel:

                if c_code.lower()  == ("VI").lower() :

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artart == 7) & (matches(Artikel.bezeich,"*visa*"))).first()

                elif c_code.lower()  == ("MC").lower() :

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artart == 7) & (matches(Artikel.bezeich,"*master*"))).first()

                if not artikel:

                    artikel = get_cache (Artikel, {"artart": [(eq, 7)]})

            if c_exp != "" and length(c_exp) == 4:
                c_exp = substring(c_exp, 0, 2) + "20" + substring(c_exp, 2)
            guest.ausweis_nr2 = artikel.bezeich + "\\" + c_number + "\\" + c_exp + "|"
        pass
        bookingid = res_info.uniq_id
        pass

        if res_mode.lower()  == ("new").lower() :

            reservation = get_cache (Reservation, {"vesrdepot": [(eq, bookingid)]})

            res_line = db_session.query(Res_line).filter(
                     (matches(Res_line.zimmer_wunsch,"*voucher" + bookingid + "*"))).first()

            if reservation or res_line:
                error_str = error_str + chr_unicode(10) + "Reservation " + res_info.uniq_id + " already exist."
                done = False

                return generate_output()

            elif not reservation:
                exist = False
                new_resno = 0

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, rgast.gastnr)],"reihenfolge": [(eq, 1)]})

                if not guestseg:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, rgast.gastnr)]})

                for reservation in db_session.query(Reservation).order_by(Reservation.resnr.desc()).all():
                    new_resno = reservation.resnr + 1


                    break

                bres = db_session.query(Bres).filter(
                         (Bres.resnr == new_resno)).first()

                bres_line = db_session.query(Bres_line).filter(
                         (Bres_line.resnr == new_resno)).first()
                exist = None != bres or None != bres_line
                while exist:
                    new_resno = new_resno + 1

                    bres = db_session.query(Bres).filter(
                             (Bres.resnr == new_resno)).first()

                    bres_line = db_session.query(Bres_line).filter(
                             (Bres_line.resnr == new_resno)).first()
                    exist = None != bres or None != bres_line

                if not exist:

                    reservation = get_cache (Reservation, {"resnr": [(eq, new_resno)]})

                    if not reservation:
                        reservation = Reservation()
                        db_session.add(reservation)

                        reservation.resnr = new_resno
                        reservation.gastnr = ota_gastnr
                        reservation.gastnrherk = ota_gastnr
                        reservation.herkunft = rgast.name
                        reservation.name = rgast.name
                        reservation.useridanlage = "**"
                        reservation.vesrdepot = bookingid
                        reservation.bemerk = res_info.remark
                        reservation.ankzeit = 0
                        reservation.point_resnr = 0

                        if guestseg:
                            reservation.segmentcode = guestseg.segmentcode
                        else:
                            reservation.segmentcode = rsegcode

                        if rgast.segment3 != 0:
                            reservation.resart = rgast.segment3
                        else:
                            reservation.resart = resart
                    else:
                        error_str = error_str + chr_unicode(10) + "Reservation already exist with resnr: " + to_string(reservation.resnr) + "; VN: " + to_string(reservation.vesrdepot)

        elif res_mode.lower()  == ("Insert").lower() :

            reservation = get_cache (Reservation, {"resnr": [(eq, new_resno)]})

        for detres in query(detres_data):
            add_resline()
        done = True
        curr_error_str = "OC" + chdelimeter1 + res_info.ota_code + chdelimeter2 +\
                "RC" + chdelimeter1 + res_info.rate_code + chdelimeter2 +\
                "RT" + chdelimeter1 + res_info.room_type + chdelimeter2 +\
                "CI" + chdelimeter1 + to_string(res_info.ci_date, "99/99/9999") + chdelimeter2 +\
                "CO" + chdelimeter1 + to_string(res_info.co_date, "99/99/9999") + chdelimeter2 +\
                "AM" + chdelimeter1 + res_info.amount + chdelimeter2 +\
                "NR" + chdelimeter1 + to_string(res_info.no_room) + chdelimeter2 +\
                "AD" + chdelimeter1 + to_string(res_info.adult) + chdelimeter2 +\
                "CH1" + chdelimeter1 + to_string(res_info.child1) + chdelimeter2 +\
                "CH2" + chdelimeter1 + to_string(res_info.child2) + chdelimeter2 +\
                "GN" + chdelimeter1 + res_info.sure_name + "," + res_info.given_name + chdelimeter2 +\
                error_str


        error_str = error_str + curr_error_str

    return generate_output()