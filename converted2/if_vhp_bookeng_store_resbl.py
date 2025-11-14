#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.if_siteminder_read_mappingbl import if_siteminder_read_mappingbl
from functions.global_allotment_number import global_allotment_number
from functions.intevent_1 import intevent_1
from functions.calc_servvat import calc_servvat
from functions.count_availability import count_availability
from functions.find_dyna_ratecodesm_1bl import find_dyna_ratecodesm_1bl
from functions.ratecode_rate import ratecode_rate
from models import Guest, Ratecode, Nation, Queasy, Guestseg, Reservation, Res_line, Htparam, Zimkateg, Artikel, Mc_guest, Fixleist, Arrangement, Waehrung, Reslin_queasy, Guest_pr, Pricecod, Resplan, Argt_line

res_info_data, Res_info = create_model("Res_info", {"res_time":string, "res_id":string, "ota_code":string, "commission":string, "curr":string, "adult":string, "child1":string, "child2":string, "remark":string, "eta":string, "given_name":string, "sure_name":string, "phone":string, "email":string, "address1":string, "address2":string, "city":string, "zip":string, "state":string, "country":string, "uniq_id":string, "res_status":string, "deposit":Decimal, "membership":string, "card_info":string, "gastnrmember":int})
room_list_data, Room_list = create_model("Room_list", {"reslinnr":int, "res_id":string, "ci_date":string, "co_date":string, "amount":string, "room_type":string, "rate_code":string, "number":int, "adult":int, "child1":int, "child2":int, "service":string, "gastnr":string, "comment":string, "argtnr":string, "ankunft":date, "abreise":date, "zikatnr":int})
service_list_data, Service_list = create_model("Service_list", {"ci_date":string, "co_date":string, "res_id":string, "amountaftertax":Decimal, "amountbeforetax":Decimal, "tamountaftertax":Decimal, "tamountbeforetax":Decimal, "bezeich":string, "rph":string, "id":string, "curr":string, "qty":int})
guest_list_data, Guest_list = create_model("Guest_list", {"res_id":string, "given_name":string, "sure_name":string, "phone":string, "email":string, "address1":string, "address2":string, "city":string, "zip":string, "state":string, "country":string, "gastnr":string, "gastnrmember":int})

def if_vhp_bookeng_store_resbl(res_info_data:[Res_info], room_list_data:[Room_list], service_list_data:[Service_list], guest_list_data:[Guest_list], res_mode:string, dyna_code:string, becode:int, new_resno:int, chdelimeter:string, chdelimeter1:string, chdelimeter2:string, chdelimeter3:string, t_guest_nat:string, t_curr_name:string):

    prepare_cache ([Guest, Ratecode, Nation, Queasy, Guestseg, Htparam, Zimkateg, Artikel, Mc_guest, Fixleist, Arrangement, Waehrung, Reslin_queasy, Guest_pr, Pricecod, Resplan, Argt_line])

    error_str = ""
    done = False
    room_occ:int = 0
    curr_date:date = None
    exist:bool = False
    curr_error_str:string = ""
    cm_gastno:int = 0
    cm_name:string = ""
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
    rmtype:string = ""
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
    loop_i:int = 0
    curr_j:int = 0
    c_number:string = ""
    c_code:string = ""
    c_exp:string = ""
    c_info:string = ""
    globekey_rsv:bool = False
    globekey_tot_amount:Decimal = to_decimal("0.0")
    tot_rmrate_vhp:Decimal = to_decimal("0.0")
    asc_str:string = ""
    str_date:string = ""
    m:int = 0
    yy:int = 0
    dd:int = 0
    n:int = 0
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
    ota_name:string = ""
    ota_seg:int = 0
    avalue:string = ""
    p:int = 0
    tahun:date = get_current_date()
    service_dept:int = 0
    service_artnr:int = 0
    tax_included:bool = False
    double_currency:bool = False
    foreign_rate:bool = False
    ratecode_frate:Decimal = 1
    sm_frate:Decimal = 1
    bill_date:date = None
    upto_date:date = None
    zikatnr:int = 0
    commission_str:string = ""
    commission_dec:Decimal = to_decimal("0.0")
    dcommission:bool = False
    markup_str:string = ""
    markup_dec:Decimal = to_decimal("0.0")
    artnr_comm:int = 0
    default_country:string = ""
    guest = ratecode = nation = queasy = guestseg = reservation = res_line = htparam = zimkateg = artikel = mc_guest = fixleist = arrangement = waehrung = reslin_queasy = guest_pr = pricecod = resplan = argt_line = None

    res_info = room_avail_list = service_list = room_list = guest_list = nation_list = rgast = bguest = bratecode = nationbuf = qsy6 = qsy = rqueasy = bqueasy = gseg = bres = bres_line = None

    room_avail_list_data, Room_avail_list = create_model("Room_avail_list", {"zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":int, "bezeich":string, "room":int, "troom":int, "datum":date}, {"sleeping": True})
    nation_list_data, Nation_list = create_model("Nation_list", {"nat_nr":int, "nat_abbr":string, "nat_desc":string})

    Rgast = create_buffer("Rgast",Guest)
    Bguest = create_buffer("Bguest",Guest)
    Bratecode = create_buffer("Bratecode",Ratecode)
    Nationbuf = create_buffer("Nationbuf",Nation)
    Qsy6 = create_buffer("Qsy6",Queasy)
    Qsy = create_buffer("Qsy",Queasy)
    Rqueasy = create_buffer("Rqueasy",Queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Gseg = create_buffer("Gseg",Guestseg)
    Bres = create_buffer("Bres",Reservation)
    Bres_line = create_buffer("Bres_line",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

        return {"error_str": error_str, "done": done}

    def add_resline(new_reslinno:int):

        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

        allotnr:int = 0
        statcode:string = ""
        res_statcode:string = ""
        start_date:date = None
        end_date:date = None
        bufguest = None
        guestbuff = None
        mcguestbuf = None
        Bufguest =  create_buffer("Bufguest",Guest)
        Guestbuff =  create_buffer("Guestbuff",Guest)
        Mcguestbuf =  create_buffer("Mcguestbuf",Mc_guest)

        if new_contrate:
            statcode, res_statcode = create_new_fixrate(new_resno, room_list.reslinnr)
            else:
                create_fixed_rate(new_resno, room_list.reslinnr)

        if res_info.eta != "":
            hh = entry(0, res_info.eta, ":")
            mm = entry(1, res_info.eta, ":")
            eta_char = hh + mm
            else:
                eta_char = "0000"
        allotnr = get_output(global_allotment_number(cm_gastno, ota_gastnr, room_list.ankunft, room_list.abreise, rmtype))

        res_line = get_cache (Res_line, {"resnr": [(eq, new_resno)],"reslinnr": [(eq, new_reslinno)]})

        if not res_line:
            res_line = Res_line()
            db_session.add(res_line)

            res_line.resnr = new_resno
            res_line.reslinnr = new_reslinno
            res_line.gastnr = ota_gastnr
            res_line.gastnrpay = ota_gastnr
            res_line.ankunft = room_list.ankunft
            res_line.abreise = room_list.abreise
            res_line.flight_nr = " " + to_string(eta_char, "x(5)") +\
                    " "
            res_line.arrangement = argt
            res_line.resstatus = resstatus
            res_line.erwachs = room_list.adult
            res_line.kind1 = room_list.child1
            res_line.kind2 = room_list.child2
            res_line.betriebsnr = currno
            res_line.bemerk = room_list.comment + chdelimeter1
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

            guest_list = query(guest_list_data, filters=(lambda guest_list: guest_list.gastnr == room_list.gastnr), first=True)

            if guest_list:

                bufguest = get_cache (Guest, {"gastnr": [(eq, guest_list.gastnrmember)]})

                if bufguest:
                    res_line.gastnrmember = bufguest.gastnr
                    res_line.name = bufguest.name + ", " + bufguest.vorname1 + ", " + bufguest.anrede1


                    error_str = error_str + chr_unicode(10) + " Assign Guest Room: " + bufguest.name + "(" + to_string(bufguest.gastnr) + ")"
            else:

                bufguest = get_cache (Guest, {"gastnr": [(eq, res_info.gastnrmember)]})

                if bufguest:
                    res_line.gastnrmember = bufguest.gastnr
                    res_line.name = bufguest.name + ", " + bufguest.vorname1 + ", " + bufguest.anrede1


                    error_str = error_str + chr_unicode(10) + "Assign Guest Room: " + bufguest.name + "(" + to_string(bufguest.gastnr) + ")"

            if room_list.comment == "":
                res_line.bemerk = ""

            if room_list.ankunft == room_list.abreise:
                res_line.anztage = 1
            else:
                res_line.anztage = (room_list.abreise - room_list.ankunft).days

            if res_line.resstatus == 1:
                res_line.kontignr = allotnr

            if new_contrate:
                res_line.zimmer_wunsch = "ebdisc;restricted;date," + to_string(get_year(curr_date)) + to_string(get_month(curr_date) , "99") + to_string(get_day(curr_date) , "99") + ";" + "voucher" + bookingid + ";" + "$CODE$" + res_statcode + ";" + "$OrigCode$" + room_list.rate_code + ";"

            if avail_gdpr:

                guestbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guestbuff:

                    mcguestbuf = get_cache (Mc_guest, {"gastnr": [(eq, res_line.gastnrmember)]})

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
            res_info.remark = replace_str(res_info.remark, ";", ",")
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$OTACOM$" + res_info.remark + chdelimeter1 + "SM-TIME," + res_info.res_time + ";" + "$PAID$" + res_info.commission + ";" + "$PRCODE$" + res_info.address2 + ";"

            if num_entries(room_list.service, "-") != 0:
                for i in range(1,num_entries(room_list.service, "-") - 1 + 1) :

                    service_list = query(service_list_data, filters=(lambda service_list: service_list.rph == entry(i - 1, room_list.service, "-")), first=True)

                    if service_list:

                        if service_list.ci_date != "":
                            start_date = date_mdy(to_int(entry(1, service_list.ci_date, "-")) , to_int(entry(2, service_list.ci_date, "-")) , to_int(entry(0, service_list.ci_date, "-")))

                        if service_list.co_date != "":
                            end_date = date_mdy(to_int(entry(1, service_list.co_date, "-")) , to_int(entry(2, service_list.co_date, "-")) , to_int(entry(0, service_list.co_date, "-")))
                        fixleist = Fixleist()
                        db_session.add(fixleist)

                        fixleist.bezeich = service_list.bezeich
                        fixleist.number = service_list.qty
                        fixleist.sequenz = 6
                        fixleist.betrag =  to_decimal(service_list.amountaftertax)
                        fixleist.artnr = service_artnr
                        fixleist.departement = service_dept
                        fixleist.resnr = new_resno
                        fixleist.reslinnr = room_list.reslinnr

                        if foreign_rate or double_currency:
                            fixleist.betrag =  to_decimal(fixleist.betrag) * to_decimal((sm_frate) / to_decimal(ratecode_frate))

                        if start_date == None:
                            fixleist.lfakt = room_list.ankunft
                            fixleist.dekade = (room_list.abreise - room_list.ankunft).days

                        elif start_date != None:
                            fixleist.lfakt = start_date
                            fixleist.dekade = (end_date - start_date).days

                        if fixleist.dekade == 0:
                            fixleist.dekade = 1
            rm_qty = res_line.zimmeranz
            pass

            if res_mode.lower()  == ("new").lower() :
                get_output(intevent_1(12, "", "Priscilla", res_line.resnr, res_line.reslinnr))

            elif res_mode.lower()  == ("insert").lower() :
                get_output(intevent_1(11, "", "Priscilla", res_line.resnr, res_line.reslinnr))
            create_resplan()
            create_reslog()
            error_str = error_str + "CUR" + chdelimeter1 + to_string(res_line.betriebsnr)
            pass
            else:
                error_str = error_str + chr_unicode(10) + "Resline already exist with resnr: " + to_string(res_line.resnr) + ";reslinnr: " + to_string(res_line.reslinnr) + ";loop: " + to_string(loop_i)


    def create_new_fixrate(resno:int, reslinno:int):

        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

        statcode = ""
        res_statcode = ""
        rate_found:bool = False
        rmrate:Decimal = to_decimal("0.0")
        kback_flag:bool = False
        n:int = 0
        ratecode_curr:string = ""
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        currno_sm:int = 0
        check_arg:bool = False
        avail_room:int = 0
        avail_rmtype:int = 0
        i:int = 0

        def generate_inner_output():
            return (statcode, res_statcode)


        if room_list.ankunft == room_list.abreise:
            upto_date = room_list.abreise
            else:
                upto_date = room_list.abreise - timedelta(days=1)

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, room_list.argtnr)]})

        if arrangement:
            argtno = arrangement.argtnr
        for bill_date in date_range(room_list.ankunft,upto_date) :
            n = n + 1
            currno = 0
            markno = 0

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

            if artikel:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            if tax_included:

                if num_entries(room_list.amount, "-") - 1 > 1:
                    room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , room_list.amount , "-")))
                else:
                    room_price =  to_decimal(to_decimal(entry(0 , room_list.amount , "-")))
            else:

                if num_entries(room_list.amount, "-") - 1 > 1:
                    room_price = to_decimal(round(to_decimal(entry(n - 1 , room_list.amount , "-")) / (1 + serv + vat) , 0))
                else:
                    room_price = to_decimal(round(to_decimal(entry(0 , room_list.amount , "-")) / (1 + serv + vat) , 0))
            ci_rate =  to_decimal(room_price)

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, res_info.curr)],"betriebsnr": [(eq, 0)]})

            if not waehrung:
                t_curr_name = get_output(if_siteminder_read_mappingbl(1, res_info.curr))

                if t_curr_name != "":

                    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, t_curr_name)],"betriebsnr": [(eq, 0)]})

            if waehrung:
                currno_sm = waehrung.waehrungsnr

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, room_list.room_type)]})

            if queasy:
                zikatnr = queasy.number1
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
            else:

                zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, room_list.room_type)]})

                if zimkateg:
                    rmtype = room_list.room_type
                    zikatnr = zimkateg.zikatnr

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

            if zimkateg:
                zikatno = zimkateg.zikatnr

            qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, room_list.rate_code)]})

            if qsy and qsy.logi1 == False and qsy.logi2 == False:

                bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                if bqueasy:
                    pass
                    bqueasy.logi2 = True
                    pass
                    pass

            qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, "")]})

            if qsy and qsy.logi1 == False and qsy.logi2 == False:

                bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                if bqueasy:
                    pass
                    bqueasy.logi2 = True
                    pass
                    pass
            statcode, argtno, markno, currno, room_occ = get_output(find_dyna_ratecodesm_1bl(ota_gastnr, bill_date, rmtype, room_list.adult, room_list.child1, room_price, room_list.rate_code, argtno))

            if n == 1:
                res_statcode = statcode

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, markno)]})

            if queasy and queasy.char3 != "":

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})

                if waehrung:
                    currno = waehrung.waehrungsnr

            if currno_sm != 0 and currno != 0 and currno_sm != currno:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, currno)],"betriebsnr": [(eq, 0)]})

                if waehrung:
                    ratecode_frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, res_info.curr)],"betriebsnr": [(eq, 0)]})

                if waehrung:
                    sm_frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                ci_rate =  to_decimal(ci_rate) * to_decimal((sm_frate) / to_decimal(ratecode_frate))
                ci_rate = to_decimal(round(ci_rate , price_decimal))

                rqueasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, room_list.rate_code)]})

                if not rqueasy:
                    room_list.rate_code = dyna_code
                statcode, argtno, markno, currno, room_occ = get_output(find_dyna_ratecodesm_1bl(ota_gastnr, bill_date, rmtype, room_list.adult, room_list.child1, ci_rate, room_list.rate_code, argtno))

                if n == 1:
                    res_statcode = statcode

            if argtno == 0:

                ratecode = get_cache (Ratecode, {"code": [(eq, room_list.rate_code)],"zikatnr": [(eq, zikatno)]})

                if not ratecode:
                    error_str = error_str + "Arrangement Not Found " + room_list.rate_code + " " + to_string(zikatno)

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 151)]})

                    if htparam.fchar != "":

                        arrangement = get_cache (Arrangement, {"arrangement": [(eq, htparam.fchar)]})

                        if arrangement:
                            argt = arrangement.arrangement
                            argtno = arrangement.argtnr


                        else:
                            check_arg = True
                    else:
                        check_arg = True

                    if check_arg:

                        arrangement = get_cache (Arrangement, {"segmentcode": [(eq, 0)]})

                        if arrangement:
                            argt = arrangement.arrangement
                            argtno = arrangement.argtnr


            else:

                arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

                if arrangement:
                    argt = arrangement.arrangement

            if markno == 0:
                error_str = error_str + "Market Segment Not Found."

            if currno == 0:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

                if htparam:

                    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

                    if not waehrung:

                        waehrung = db_session.query(Waehrung).first()
                    currno = waehrung.waehrungsnr
            rate_found, rmrate, restricted_disc, kback_flag = get_output(ratecode_rate(True, True, resno, reslinno, ("!" + statcode), curr_date, bill_date, room_list.ankunft, room_list.abreise, markno, argtno, zikatno, room_list.adult, room_list.child1, room_list.child2, 0, currno))

            if artnr_comm != 0:

                if dcommission:
                    calc_commissions(bill_date, resno, reslinno, argtno, room_price)
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


            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "occ-room"
            reslin_queasy.resnr = resno
            reslin_queasy.reslinnr = reslinno
            reslin_queasy.date1 = bill_date
            reslin_queasy.date2 = bill_date
            reslin_queasy.deci1 =  to_decimal(ci_rate)
            reslin_queasy.char1 = argt
            reslin_queasy.char2 = statcode
            reslin_queasy.number1 = room_occ


            pass

            if bill_date == room_list.ankunft:
                ci_rate1 =  to_decimal(ci_rate)

        return generate_inner_output()


    def create_fixed_rate(resno:int, reslinno:int):

        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

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

        if room_list.ankunft == room_list.abreise:
            upto_date = room_list.abreise
            else:
                upto_date = room_list.abreise - timedelta(days=1)
        for bill_date in date_range(room_list.ankunft,upto_date) :

            pricecod = get_cache (Pricecod, {"code": [(eq, guest_pr.code)],"marknr": [(eq, markno)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, zikatno)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)]})

            if pricecod:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = resno
                reslin_queasy.reslinnr = reslinno
                reslin_queasy.date1 = bill_date
                reslin_queasy.date2 = bill_date
                reslin_queasy.deci1 =  to_decimal(pricecod.perspreis[room_list.adult - 1] +\
                        pricecod.kindpreis[0]) * to_decimal(room_list.child1)
                reslin_queasy.char1 = argt


                pass

                if bill_date == room_list.ankunft:
                    ci_rate =  to_decimal(reslin_queasy.deci1)


    def create_reslog():

        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

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

        nonlocal error_str, done, room_occ, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

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


    def chk_ascii(str1:string):

        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

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

            elif asc(substring(str1, curr_i - 1, 1)) == 192 or asc(substring(str1, curr_i, 1)) == 193 or asc(substring(str1, curr_i, 1)) == 194 or asc(substring(str1, curr_i, 1)) == 195 or asc(substring(str1, curr_i, 1)) == 196 or asc(substring(str1, curr_i, 1)) == 197:
                str2 = str2 + "A"

            elif asc(substring(str1, curr_i - 1, 1)) == 224 or asc(substring(str1, curr_i, 1)) == 225 or asc(substring(str1, curr_i, 1)) == 226 or asc(substring(str1, curr_i, 1)) == 227 or asc(substring(str1, curr_i, 1)) == 228 or asc(substring(str1, curr_i, 1)) == 229:
                str2 = str2 + "a"

            elif asc(substring(str1, curr_i - 1, 1)) == 200 or asc(substring(str1, curr_i, 1)) == 201 or asc(substring(str1, curr_i, 1)) == 202 or asc(substring(str1, curr_i, 1)) == 203:
                str2 = str2 + "E"

            elif asc(substring(str1, curr_i - 1, 1)) == 232 or asc(substring(str1, curr_i, 1)) == 233 or asc(substring(str1, curr_i, 1)) == 234 or asc(substring(str1, curr_i, 1)) == 235:
                str2 = str2 + "e"

            elif asc(substring(str1, curr_i - 1, 1)) == 204 or asc(substring(str1, curr_i, 1)) == 205 or asc(substring(str1, curr_i, 1)) == 206 or asc(substring(str1, curr_i, 1)) == 207:
                str2 = str2 + "i"

            elif asc(substring(str1, curr_i - 1, 1)) == 236 or asc(substring(str1, curr_i, 1)) == 237 or asc(substring(str1, curr_i, 1)) == 238 or asc(substring(str1, curr_i, 1)) == 239:
                str2 = str2 + "i"

            elif asc(substring(str1, curr_i - 1, 1)) == 210 or asc(substring(str1, curr_i, 1)) == 211 or asc(substring(str1, curr_i, 1)) == 212 or asc(substring(str1, curr_i, 1)) == 213 or asc(substring(str1, curr_i, 1)) == 214:
                str2 = str2 + "O"

            elif asc(substring(str1, curr_i - 1, 1)) == 242 or asc(substring(str1, curr_i, 1)) == 243 or asc(substring(str1, curr_i, 1)) == 244 or asc(substring(str1, curr_i, 1)) == 245 or asc(substring(str1, curr_i, 1)) == 246:
                str2 = str2 + "o"

            elif asc(substring(str1, curr_i - 1, 1)) == 217 or asc(substring(str1, curr_i, 1)) == 218 or asc(substring(str1, curr_i, 1)) == 219 or asc(substring(str1, curr_i, 1)) == 220:
                str2 = str2 + "U"

            elif asc(substring(str1, curr_i - 1, 1)) == 249 or asc(substring(str1, curr_i, 1)) == 250 or asc(substring(str1, curr_i, 1)) == 251 or asc(substring(str1, curr_i, 1)) == 252:
                str2 = str2 + "u"

            elif asc(substring(str1, curr_i - 1, 1)) == 209:
                str2 = str2 + "n"

            elif asc(substring(str1, curr_i - 1, 1)) == 241:
                str2 = str2 + "n"

            elif asc(substring(str1, curr_i - 1, 1)) == 160:
                str2 = str2 + " "

            elif asc(substring(str1, curr_i - 1, 1)) > 127 or asc(substring(str1, curr_i, 1)) < 32:
                str2 = str2 + "-"
            else:
                str2 = str2 + substring(str1, curr_i - 1, 1)

        return generate_inner_output()


    def calc_commissions(stay_date:date, rsv_resno:int, rsv_reslinno:int, rsv_argtno:int, rsv_rate:Decimal):

        nonlocal error_str, done, room_occ, curr_date, exist, curr_error_str, cm_gastno, cm_name, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, rmtype, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, loop_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, n, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, ota_name, ota_seg, avalue, p, tahun, service_dept, service_artnr, tax_included, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, commission_str, commission_dec, dcommission, markup_str, markup_dec, artnr_comm, default_country, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan, argt_line
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line


        nonlocal res_info, room_avail_list, service_list, room_list, guest_list, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, qsy, rqueasy, bqueasy, gseg, bres, bres_line
        nonlocal room_avail_list_data, nation_list_data

        commission_amount:Decimal = to_decimal("0.0")
        commission_amount = to_decimal(round(((commission_dec / 100) * rsv_rate) , 0))

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, rsv_argtno)],"argt_artnr": [(eq, artnr_comm)]})

        if argt_line:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "fargt-line"
            reslin_queasy.number1 = argt_line.departement
            reslin_queasy.number2 = rsv_argtno
            reslin_queasy.number3 = argt_line.argt_artnr
            reslin_queasy.resnr = rsv_resno
            reslin_queasy.reslinnr = rsv_reslinno
            reslin_queasy.deci1 =  to_decimal(commission_amount)
            reslin_queasy.deci2 =  to_decimal("0")
            reslin_queasy.deci3 =  to_decimal("0")
            reslin_queasy.date1 = stay_date
            reslin_queasy.date2 = stay_date


            pass

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

    if queasy:
        cm_gastno = queasy.number2
        cm_name = queasy.char1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 67)]})
    rsegcode = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 69)]})
    resart = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 30)]})
    service_artnr = htparam.finteger
    service_dept = 0

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    tax_included = htparam.flogical

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

    for guest_list in query(guest_list_data):
        asc_str = chk_ascii(guest_list.sure_name)
        guest_list.sure_name = asc_str
        asc_str = ""
        asc_str = chk_ascii(guest_list.city)
        res_info.city = asc_str
        asc_str = ""
        asc_str = chk_ascii(guest_list.given_name)
        guest_list.given_name = asc_str
        asc_str = ""
        asc_str = chk_ascii(guest_list.address1)
        guest_list.address1 = asc_str
        asc_str = ""
        asc_str = chk_ascii(guest_list.address2)
        guest_list.address2 = asc_str
        asc_str = ""
        asc_str = chk_ascii(guest_list.city)
        guest_list.city = asc_str
        asc_str = ""
        asc_str = chk_ascii(guest_list.email)
        guest_list.email = asc_str
        asc_str = ""

    res_info = query(res_info_data, first=True)

    if res_info:

        rgast = db_session.query(Rgast).filter(
                 (trim(entry(0, Rgast.steuernr, "|")) == trim(res_info.ota_code))).first()

        if not rgast:
            error_str = error_str + "Reservation TA File not found for : " + trim(res_info.ota_code) + ". "

            rgast = get_cache (Guest, {"gastnr": [(eq, cm_gastno)]})

            if rgast:
                ota_gastnr = rgast.gastnr
        else:
            ota_gastnr = rgast.gastnr
        bookingid = res_info.res_id
        ota_name = rgast.name
        ota_seg = rgast.segment3

        if trim(res_info.ota_code) == ("SERVR").lower() :
            resstatus = 5

        guest = get_cache (Guest, {"gastnr": [(eq, ota_gastnr)]})

        if guest:

            if num_entries(guest.steuernr, "|") > 5:

                if entry(1, guest.steuernr, "|") != "" or entry(1, guest.steuernr, "|") != None:
                    commission_str = entry(1, guest.steuernr, "|")
                    commission_str = replace_str(commission_str, "-", "")
                    commission_str = replace_str(commission_str, "%", "")
                    commission_str = replace_str(commission_str, ",", ".")
                    commission_dec =  to_decimal(to_decimal(commission_str) )

                if entry(6, guest.steuernr, "|") != "" or entry(6, guest.steuernr, "|") != None:
                    markup_str = entry(6, guest.steuernr, "|")
                    markup_str = replace_str(commission_str, "-", "")
                    markup_str = replace_str(commission_str, "%", "")
                    markup_str = replace_str(commission_str, ",", ".")
                    markup_dec =  to_decimal(to_decimal(commission_str) )

                if entry(7, guest.steuernr, "|") != "" or entry(7, guest.steuernr, "|") != None:
                    dcommission = logical(entry(7, guest.steuernr, "|"))

                if entry(8, guest.steuernr, "|") != "" or entry(8, guest.steuernr, "|") != None:
                    artnr_comm = to_int(entry(8, guest.steuernr, "|"))

            elif num_entries(guest.steuernr, "|") == 5:

                if entry(1, guest.steuernr, "|") != "" or entry(1, guest.steuernr, "|") != None:
                    commission_str = entry(1, guest.steuernr, "|")
                    commission_str = replace_str(commission_str, "-", "")
                    commission_str = replace_str(commission_str, "%", "")
                    commission_str = replace_str(commission_str, ",", ".")
                    commission_dec =  to_decimal(to_decimal(commission_str) )

                if entry(2, guest.steuernr, "|") != "" or entry(2, guest.steuernr, "|") != None:
                    markup_str = entry(2, guest.steuernr, "|")
                    markup_str = replace_str(commission_str, "-", "")
                    markup_str = replace_str(commission_str, "%", "")
                    markup_str = replace_str(commission_str, ",", ".")
                    markup_dec =  to_decimal(to_decimal(commission_str) )

                if entry(3, guest.steuernr, "|") != "" or entry(3, guest.steuernr, "|") != None:
                    dcommission = logical(entry(3, guest.steuernr, "|"))

                if entry(4, guest.steuernr, "|") != "" or entry(4, guest.steuernr, "|") != None:
                    artnr_comm = to_int(entry(4, guest.steuernr, "|"))

        if res_mode.lower()  == ("new").lower() :

            for room_list in query(room_list_data):

                rqueasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, room_list.rate_code)]})

                if not rqueasy:
                    room_list.rate_code = dyna_code

                queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, room_list.room_type)]})

                if not queasy:

                    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, room_list.room_type)]})

                    if not zimkateg:
                        error_str = error_str + chr_unicode(10) + room_list.room_type + "No such Room Category"

                        return generate_output()

            reservation = get_cache (Reservation, {"vesrdepot": [(eq, bookingid)],"gastnr": [(eq, ota_gastnr)]})

            if not reservation:

                res_line = db_session.query(Res_line).filter(
                         (Res_line.gastnr == ota_gastnr) & (matches(Res_line.zimmer_wunsch,"*voucher" + bookingid + "*")) & not_ (Res_line.resstatus == 9)).first()

            if res_line or reservation:
                error_str = error_str + chr_unicode(10) + "Reservation " + res_info.uniq_id + " already exist."


                exist = True
                done = True

                room_list = query(room_list_data, filters=(lambda room_list: room_list.res_id == bookingid), first=True)

                if room_list.ankunft == room_list.abreise:
                    upto_date = room_list.abreise
                else:
                    upto_date = room_list.abreise - timedelta(days=1)
                for bill_date in date_range(room_list.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, room_list.room_type)]})

                    if queasy:
                        zikatnr = queasy.number1
                    else:

                        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, room_list.room_type)]})

                        if zimkateg:
                            zikatnr = zimkateg.zikatnr

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, room_list.rate_code)]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            pass
                            bqueasy.logi2 = True
                            pass
                            pass

                    qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, "")]})

                    if qsy and qsy.logi1 == False and qsy.logi2 == False:

                        bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                        if bqueasy:
                            pass
                            bqueasy.logi2 = True
                            pass
                            pass

                if exist:

                    return generate_output()
        pass

        if res_info.card_info != "":
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

                if c_code.lower()  == ("VI").lower() :

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artart == 7) & (matches(Artikel.bezeich,"*visa*"))).first()

                elif c_code.lower()  == ("MC").lower() :

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artart == 7) & (matches(Artikel.bezeich,"*master*"))).first()

                elif c_code.lower()  == ("AX").lower() :

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artart == 7) & (matches(Artikel.bezeich,"*american*"))).first()

                elif c_code.lower()  == ("JC").lower() :

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artart == 7) & (matches(Artikel.bezeich,"*japanese*"))).first()

                if not artikel:

                    artikel = get_cache (Artikel, {"artart": [(eq, 7)]})

                if c_exp != "":
                    c_exp = substring(c_exp, 0, 2) + "20" + substring(c_exp, 2, 2)

        if not num_entries(res_info.email, "@") == 2:
            res_info.email = ""

        elif not length(entry(0, res_info.email, "@")) >= 2 and not length(entry(1, res_info.email, "@")) >= 2:
            res_info.email = ""
        res_info.phone = replace_str(res_info.phone, " ", "")
        res_info.phone = replace_str(res_info.phone, "-", "")

        if substring(res_info.phone, 0, 3) == "+62":
            res_info.phone = replace_str(res_info.phone, "+62", "0")

        elif substring(res_info.phone, 0, 2) == ("62").lower() :
            res_info.phone = replace_str(res_info.phone, substring(res_info.phone, 0, 2) , "0")

        if res_info.phone.lower()  != "" and res_info.phone.lower()  != ("n/A").lower() :

            guest = db_session.query(Guest).filter(
                         (matches((Guest.telefon,'*' + substring(res_info.phone, 1))) | (matches(Guest.mobil_telefon,'*' + substring(res_info.phone, 1)))) & (Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name)).first()
        else:

            if res_info.email.lower()  != "" and res_info.email.lower()  != ("n/A").lower() :

                guest = db_session.query(Guest).filter(
                             ((Guest.email_adr == res_info.email) | (Guest.email_adr == ("n/A").lower()) | (Guest.email_adr == "")) & (Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name)).first()
            else:

                guest = get_cache (Guest, {"name": [(eq, res_info.sure_name)],"vorname1": [(eq, res_info.given_name)],"adresse1": [(eq, res_info.address1)]})

        if not guest:

            if res_info.country != "":
                t_guest_nat = ""

                nation = get_cache (Nation, {"bezeich": [(eq, res_info.country)]})

                if nation:
                    t_guest_nat = nation.kurzbez
                else:
                    t_guest_nat = get_output(if_siteminder_read_mappingbl(2, res_info.country))

                    if t_guest_nat != "":

                        nation = get_cache (Nation, {"kurzbez": [(eq, t_guest_nat)]})

                        if nation:
                            t_guest_nat = nation.kurzbez
                    else:

                        nation = db_session.query(Nation).filter(
                                     (matches(Nation.bezeich,"*Unknown*"))).first()

                        if nation:
                            t_guest_nat = nation.kurzbez
                        else:
                            t_guest_nat = ""
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})
                default_country = htparam.fchar

                if default_country != "" or default_country != None:
                    t_guest_nat = default_country


                else:

                    nation = db_session.query(Nation).filter(
                                 (matches(Nation.bezeich,"*Unknown*"))).first()

                    if nation:
                        t_guest_nat = nation.kurzbez
                    else:
                        t_guest_nat = ""
            exist = False
            gastnrmember = 0

            for guest in db_session.query(Guest).order_by(Guest.gastnr.desc()).all():
                gastnrmember = guest.gastnr + 1


                break

            rgast = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})
            exist = None != rgast
            while exist :
                gastnrmember = gastnrmember + 1

                rgast = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})
                exist = None != rgast

            if not exist:

                bguest = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})

                if not bguest:
                    bguest = Guest()
                    db_session.add(bguest)

                    bguest.gastnr = gastnrmember
                    bguest.name = res_info.sure_name
                    bguest.vorname1 = res_info.given_name
                    bguest.adresse1 = res_info.address1
                    bguest.wohnort = res_info.city
                    bguest.land = t_guest_nat
                    bguest.plz = res_info.zip
                    bguest.email_adr = res_info.email
                    bguest.telefon = res_info.phone
                    bguest.nation1 = t_guest_nat

                    if c_number != "":
                        bguest.ausweis_nr2 = artikel.bezeich + "\\" + c_number + "\\" + c_exp + "|"

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, ota_gastnr)],"reihenfolge": [(eq, 1)]})

                    if guestseg:
                        rsegm = guestseg.segmentcode

                        gseg = get_cache (Guestseg, {"gastnr": [(eq, gastnrmember)],"segmentcode": [(eq, rsegm)],"reihenfolge": [(eq, 1)]})

                        if not gseg:
                            gseg = Guestseg()
                            db_session.add(gseg)

                            gseg.gastnr = gastnrmember
                            gseg.reihenfolge = 1
                            gseg.segmentcode = rsegm


        else:
            gastnrmember = guest.gastnr

            bguest = get_cache (Guest, {"_recid": [(eq, guest._recid)]})

            if bguest and bguest.ausweis_nr2 == "" and c_number != "":
                pass
                bguest.ausweis_nr2 = artikel.bezeich + "\\" + c_number + "\\" + c_exp + "|"
                pass
                pass
        res_info.gastnrmember = gastnrmember

        if res_info.membership != "":

            mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastnrmember)]})

            if not mc_guest:
                mc_guest = Mc_guest()
                db_session.add(mc_guest)

                mc_guest.gastnr = gastnrmember
                mc_guest.created_date = get_current_date()
                mc_guest.activeflag = False
                mc_guest.fdate = get_current_date()
                mc_guest.tdate = tahun + timedelta(days=32850)


                for p in range(1,num_entries(res_info.membership, "-")  + 1) :
                    avalue = entry(p - 1, res_info.membership, "-")

                    if matches(avalue,r"*membershipid*"):
                        mc_guest.cardnum = entry(1, avalue, ":")

                    if matches(avalue,r"*membershipprogram*"):
                        mc_guest.bemerk = entry(1, avalue, ":")

        for guest_list in query(guest_list_data):

            if not num_entries(guest_list.email, "@") == 2:
                guest_list.email = ""

            elif not length(entry(0, guest_list.email, "@")) >= 2 and not length(entry(1, guest_list.email, "@")) >= 2:
                guest_list.email = ""
            guest_list.phone = replace_str(guest_list.phone, " ", "")
            guest_list.phone = replace_str(guest_list.phone, "-", "")

            if substring(guest_list.phone, 0, 3) == "+62":
                guest_list.phone = replace_str(guest_list.phone, "+62", "0")

            elif substring(guest_list.phone, 0, 2) == ("62").lower() :
                guest_list.phone = replace_str(guest_list.phone, substring(guest_list.phone, 0, 2) , "0")

            if guest_list.phone.lower()  != "" and guest_list.phone.lower()  != ("n/A").lower() :

                guest = db_session.query(Guest).filter(
                         (matches((Guest.telefon,'*' + substring(guest_list.phone, 1))) | (matches(Guest.mobil_telefon,'*' + substring(guest_list.phone, 1)))) & (Guest.name == guest_list.sure_name) & (Guest.vorname1 == guest_list.given_name)).first()
            else:

                if guest_list.email.lower()  != "" and guest_list.email.lower()  != ("n/A").lower() :

                    guest = db_session.query(Guest).filter(
                             ((Guest.email_adr == guest_list.email) | (Guest.email_adr == ("n/A").lower()) | (Guest.email_adr == "")) & (Guest.name == guest_list.sure_name) & (Guest.vorname1 == guest_list.given_name)).first()
                else:

                    guest = get_cache (Guest, {"name": [(eq, guest_list.sure_name)],"vorname1": [(eq, guest_list.given_name)],"adresse1": [(eq, guest_list.address1)]})

            if not guest:

                if guest_list.country != "":
                    t_guest_nat = ""

                    nation = get_cache (Nation, {"bezeich": [(eq, guest_list.country)]})

                    if nation:
                        t_guest_nat = nation.kurzbez
                    else:
                        t_guest_nat = get_output(if_siteminder_read_mappingbl(2, guest_list.country))

                        if t_guest_nat != "":

                            nation = get_cache (Nation, {"kurzbez": [(eq, t_guest_nat)]})

                            if nation:
                                t_guest_nat = nation.kurzbez
                        else:
                            error_str = error_str + chr_unicode(10) + "Guest country not mapping yet = " + guest_list.country
                            t_guest_nat = ""


                else:
                    error_str = error_str + chr_unicode(10) + "Guest country not defined."
                    t_guest_nat = ""


                exist = False
                gastnrmember = 0

                for guest in db_session.query(Guest).order_by(Guest.gastnr.desc()).all():
                    gastnrmember = guest.gastnr + 1


                    break

                rgast = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})
                exist = None != rgast
                while exist :
                    gastnrmember = gastnrmember + 1

                    rgast = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})
                    exist = None != rgast

                if not exist:

                    bguest = get_cache (Guest, {"gastnr": [(eq, gastnrmember)]})

                    if not bguest:
                        bguest = Guest()
                        db_session.add(bguest)

                        bguest.gastnr = gastnrmember
                        bguest.name = guest_list.sure_name
                        bguest.vorname1 = guest_list.given_name
                        bguest.adresse1 = guest_list.address1
                        bguest.wohnort = guest_list.city
                        bguest.land = t_guest_nat
                        bguest.plz = guest_list.zip
                        bguest.email_adr = guest_list.email
                        bguest.telefon = guest_list.phone
                        bguest.nation1 = t_guest_nat

                        guestseg = get_cache (Guestseg, {"gastnr": [(eq, ota_gastnr)],"reihenfolge": [(eq, 1)]})

                        if guestseg:
                            rsegm = guestseg.segmentcode

                            gseg = get_cache (Guestseg, {"gastnr": [(eq, gastnrmember)],"segmentcode": [(eq, rsegm)],"reihenfolge": [(eq, 1)]})

                            if not gseg:
                                gseg = Guestseg()
                                db_session.add(gseg)

                                gseg.gastnr = gastnrmember
                                gseg.reihenfolge = 1
                                gseg.segmentcode = rsegm


            else:
                gastnrmember = guest.gastnr
            guest_list.gastnrmember = gastnrmember


        bookingid = res_info.res_id
        pass

        if res_mode.lower()  == ("new").lower() :

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, ota_gastnr)],"reihenfolge": [(eq, 1)]})

            if not guestseg:

                guestseg = get_cache (Guestseg, {"gastnr": [(eq, ota_gastnr)]})
            exist = False
            new_resno = 0

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
                    reservation.herkunft = ota_name
                    reservation.name = ota_name
                    reservation.useridanlage = "**"
                    reservation.vesrdepot = bookingid
                    reservation.bemerk = res_info.remark
                    reservation.ankzeit = 0
                    reservation.point_resnr = 0

                    if guestseg:
                        reservation.segmentcode = guestseg.segmentcode
                    else:
                        reservation.segmentcode = rsegcode

                    if ota_seg != 0:
                        reservation.resart = ota_seg
                    else:
                        reservation.resart = resart
                else:
                    error_str = error_str + chr_unicode(10) + "Reservation already exist with resnr: " + to_string(reservation.resnr) + "; VN: " + to_string(reservation.vesrdepot)

        elif res_mode.lower()  == ("Insert").lower() :

            reservation = get_cache (Reservation, {"resnr": [(eq, new_resno)]})
        pass
        loop_i = 0

        for room_list in query(room_list_data):
            loop_i = loop_i + 1

            if res_mode.lower()  == ("new").lower() :
                room_list.reslinnr = loop_i
            add_resline(room_list.reslinnr)
        done = True
        error_str = error_str + curr_error_str

        if matches(error_str,r"*resnr*"):
            done = False
        i = i + 1

    return generate_output()