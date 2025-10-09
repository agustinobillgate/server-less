#using conversion tools version: 1.0.0.117

# ====================================================================
# Rulita, 09-10-2025
# Tiket ID : 7BB74B | recompile program
# Issue : - Fixing temptable name dateRes To dateres
#         - di .p ada conndition 
#           &IF SUBSTRING(PROVERSION, 1, 1) = "1" &THEN  /* OE */
#               DEFINE VARIABLE response        AS LONGCHAR NO-UNDO INIT "".
#           &ELSEIF SUBSTRING(PROVERSION, 1, 1) = "9" &THEN /* Progress v9 */
#               DEFINE VARIABLE response        AS CHAR NO-UNDO INIT "".
#           &ENDIF.
#         - di python variable response pake string ""
# ====================================================================


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.if_siteminder_read_mappingbl import if_siteminder_read_mappingbl
from functions.global_allotment_number import global_allotment_number
from functions.calc_servvat import calc_servvat
from functions.count_availability import count_availability
from functions.find_dyna_ratecodesm import find_dyna_ratecodesm
from functions.ratecode_rate import ratecode_rate
from functions.calc_dynaratessm import calc_dynaratessm
from models import Guest, Ratecode, Nation, Queasy, Guestseg, Reservation, Res_line, Htparam, Zimkateg, Artikel, Mc_guest, Fixleist, Arrangement, Waehrung, Reslin_queasy, Guest_pr, Pricecod, Resplan

res_info_data, Res_info = create_model("Res_info", {"res_time":string, "res_id":string, "ota_code":string, "no_room":int, "rate_code":string, "room_type":string, "ci_date":date, "co_date":date, "amount":string, "amountbeforetax":string, "taxes":string, "base_flag":bool, "curr":string, "adult":string, "child1":string, "child2":string, "remark":string, "eta":string, "given_name":string, "sure_name":string, "phone":string, "email":string, "address1":string, "address2":string, "city":string, "zip":string, "state":string, "country":string, "commission":string, "night":int, "amount_at":string, "curr_at":string, "argtnr":string, "uniq_id":string, "res_status":string, "deposit":Decimal, "membership":string, "card_info":string}, {"commission": ""})
detres_data, Detres = create_model("Detres", {"reslinnr":int, "amount":string, "amountbeforetax":string, "base_flag":bool, "adult":int, "child1":int, "child2":int, "room_type":string, "rate_code":string, "argtnr":string, "ci_date":date, "co_date":date, "night":int, "firstname":string, "lastname":string, "selected":bool, "uniq_id":string, "zikatnr":int, "gastnrmember":int})
t_fixleist_data, T_fixleist = create_model("T_fixleist", {"uniq_id":string, "bezeich":string, "servicerph":int, "qty":int, "amountaftertax":Decimal, "amountbeforetax":Decimal, "start_date":date, "end_date":date})

def store_ressmv2bl(res_info_data:[Res_info], detres_data:[Detres], t_fixleist_data:[T_fixleist], res_mode:string, dyna_code:string, becode:int, new_resno:int, chdelimeter:string, chdelimeter1:string, chdelimeter2:string, chdelimeter3:string, t_guest_nat:string, t_curr_name:string):

    prepare_cache ([Guest, Ratecode, Nation, Queasy, Guestseg, Htparam, Zimkateg, Artikel, Mc_guest, Fixleist, Arrangement, Waehrung, Reslin_queasy, Guest_pr, Pricecod, Resplan])

    error_str = ""
    done = False
    response:string = ""
    curr_date:date = None
    exist:bool = False
    expired:bool = False
    curr_error_str:string = ""
    sm_gastno:int = 0
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
    avalue:string = ""
    p:int = 0
    tahun:date = get_current_date()
    service_dept:int = 0
    service_artnr:int = 0
    tax_included:bool = False
    cat_flag:bool = False
    rmtype:string = ""
    double_currency:bool = False
    foreign_rate:bool = False
    ratecode_frate:Decimal = 1
    sm_frate:Decimal = 1
    bill_date:date = None
    upto_date:date = None
    zikatnr:int = 0
    n:int = 0
    max_reslinnr:int = 0
    amount:string = ""
    guest = ratecode = nation = queasy = guestseg = reservation = res_line = htparam = zimkateg = artikel = mc_guest = fixleist = arrangement = waehrung = reslin_queasy = guest_pr = pricecod = resplan = None

    room_avail_list = rate_list = rate_list2 = res_info = detres = t_fixleist = nation_list = rgast = bguest = bratecode = nationbuf = qsy6 = gseg = bres = bres_line = rqueasy = qsy = bqueasy = None

    room_avail_list_data, Room_avail_list = create_model("Room_avail_list", {"zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":int, "bezeich":string, "room":int, "troom":int, "datum":date}, {"sleeping": True})
    rate_list_data, Rate_list = create_model("Rate_list", {"datum":date, "currency":string, "rmrate":Decimal, "updateflag":bool, "occ_rooms":int, "rcode":string, "rcmap":string, "room_type":string})
    rate_list2_data, Rate_list2 = create_model_like(Rate_list)
    nation_list_data, Nation_list = create_model("Nation_list", {"nat_nr":int, "nat_abbr":string, "nat_desc":string})

    Rgast = create_buffer("Rgast",Guest)
    Bguest = create_buffer("Bguest",Guest)
    Bratecode = create_buffer("Bratecode",Ratecode)
    Nationbuf = create_buffer("Nationbuf",Nation)
    Qsy6 = create_buffer("Qsy6",Queasy)
    Gseg = create_buffer("Gseg",Guestseg)
    Bres = create_buffer("Bres",Reservation)
    Bres_line = create_buffer("Bres_line",Res_line)
    Rqueasy = create_buffer("Rqueasy",Queasy)
    Qsy = create_buffer("Qsy",Queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        return {"error_str": error_str, "done": done}

    def add_resline_acc(tgastnrmember:int):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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

        bufguest = get_cache (Guest, {"gastnr": [(eq, tgastnrmember)]})

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
        allotnr = get_output(global_allotment_number(sm_gastno, ota_gastnr, detres.ci_date, detres.co_date, rmtype))
        res_line = Res_line()
        db_session.add(res_line)

        res_line.resnr = new_resno
        res_line.reslinnr = detres.reslinnr
        res_line.gastnr = ota_gastnr
        res_line.gastnrmember = tgastnrmember
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
            res_line.zimmer_wunsch = "ebdisc;restricted;date," + to_string(get_year(curr_date)) + to_string(get_month(curr_date) , "99") + to_string(get_day(curr_date) , "99") + ";" + "voucher" + bookingid + ";" + "$CODE$" + res_statcode + ";"

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
        res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$OTACOM$" + res_info.remark + chdelimeter1 + "SM-TIME," + res_info.res_time + ";"

        for t_fixleist in query(t_fixleist_data, filters=(lambda t_fixleist: t_fixleist.start_date != None and t_fixleist.end_date != None)):

            if (t_fixleist.serviceRPH == 0 or t_fixleist.serviceRPH == detres.reslinnr) and t_fixleist.uniq_id == bookingid:
                fixleist = Fixleist()
                db_session.add(fixleist)

                fixleist.bezeich = t_fixleist.bezeich
                fixleist.number = t_fixleist.qty
                fixleist.sequenz = 6
                fixleist.artnr = service_artnr
                fixleist.departement = service_dept
                fixleist.resnr = new_resno
                fixleist.reslinnr = detres.reslinnr

                if foreign_rate or double_currency:
                    fixleist.betrag =  to_decimal(fixleist.betrag) * to_decimal((sm_frate) / to_decimal(ratecode_frate))

                if t_fixleist.start_date == None:
                    fixleist.lfakt = detres.ci_date
                    fixleist.dekade = (detres.co_date - detres.ci_date).days

                elif t_fixleist.start_date != None:
                    fixleist.lfakt = t_fixleist.start_date
                    fixleist.dekade = (t_fixleist.end_date - t_fixleist.start_date).days

                if fixleist.dekade == 0:
                    fixleist.dekade = 1
                fixleist.betrag =  to_decimal(t_fixleist.amountaftertax) / to_decimal(fixleist.dekade)
        rm_qty = res_line.zimmeranz
        pass
        create_resplan()
        create_reslog()
        error_str = error_str + "CUR" + chdelimeter1 + to_string(res_line.betriebsnr)
        pass


    def add_resline():

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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
        allotnr = get_output(global_allotment_number(sm_gastno, ota_gastnr, detres.ci_date, detres.co_date, rmtype))

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
            res_line.zimmer_wunsch = "ebdisc;restricted;date," + to_string(get_year(curr_date)) + to_string(get_month(curr_date) , "99") + to_string(get_day(curr_date) , "99") + ";" + "voucher" + bookingid + ";" + "$CODE$" + res_statcode + ";"

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
        res_line.zimmer_wunsch = res_line.zimmer_wunsch + "$OTACOM$" + res_info.remark + chdelimeter1 + "SM-TIME," + res_info.res_time + ";"

        for t_fixleist in query(t_fixleist_data, filters=(lambda t_fixleist: t_fixleist.start_date != None and t_fixleist.end_date != None)):

            if (t_fixleist.serviceRPH == 0 or t_fixleist.serviceRPH == detres.reslinnr) and t_fixleist.uniq_id == bookingid:
                fixleist = Fixleist()
                db_session.add(fixleist)

                fixleist.bezeich = t_fixleist.bezeich
                fixleist.number = t_fixleist.qty
                fixleist.sequenz = 6
                fixleist.artnr = service_artnr
                fixleist.departement = service_dept
                fixleist.resnr = new_resno
                fixleist.reslinnr = detres.reslinnr

                if foreign_rate or double_currency:
                    fixleist.betrag =  to_decimal(fixleist.betrag) * to_decimal((sm_frate) / to_decimal(ratecode_frate))

                if t_fixleist.start_date == None:
                    fixleist.lfakt = detres.ci_date
                    fixleist.dekade = (detres.co_date - detres.ci_date).days

                elif t_fixleist.start_date != None:
                    fixleist.lfakt = t_fixleist.start_date
                    fixleist.dekade = (t_fixleist.end_date - t_fixleist.start_date).days

                if fixleist.dekade == 0:
                    fixleist.dekade = 1
                fixleist.betrag =  to_decimal(t_fixleist.amountaftertax) / to_decimal(fixleist.dekade)
        rm_qty = res_line.zimmeranz
        pass
        create_resplan()
        create_reslog()
        error_str = error_str + "CUR" + chdelimeter1 + to_string(res_line.betriebsnr)
        pass


    def create_new_fixrate(resno:int, reslinno:int):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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
        currno_sm:int = 0
        check_arg:bool = False
        avail_room:int = 0
        avail_rmtype:int = 0

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
            room_price =  to_decimal("0")

            artikel = get_cache (Artikel, {"artnr": [(eq, arrangement.argt_artikelnr)],"departement": [(eq, 0)]})

            if artikel:
                serv, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, bill_date, artikel.service_code, artikel.mwst_code))

            if tax_included:

                if num_entries(detres.amount, ";") >= 1 and to_decimal(entry(n - 1, detres.amount, ";")) != 0:
                    room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , detres.amount , ";")))

                elif num_entries(detres.amountbeforetax, ";") >= 1 and to_decimal(entry(n - 1, detres.amountbeforetax, ";")) != 0:
                    room_price = to_decimal(round(to_decimal(entry(n - 1 , detres.amountbeforetax , ";")) * (1 + serv + vat) , 0))

                elif num_entries(detres.amount, ";") <= 1 and num_entries(detres.amountbeforetax, ";") <= 1:

                    if to_decimal(detres.amount) != 0:
                        room_price =  to_decimal(to_decimal(detres.amount))
                    else:
                        room_price = to_decimal(round(to_decimal(detres.amountbeforetax) * (1 + serv + vat) , 0))

                elif num_entries(detres.amount, ";") >= 1:
                    room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , detres.amount , ";")))

                elif num_entries(detres.amountbeforetax, ";") >= 1:
                    room_price = to_decimal(round(to_decimal(entry(n - 1 , detres.amountbeforetax , ";")) * (1 + serv + vat) , 0))
            else:

                if num_entries(detres.amountbeforetax, ";") >= 1 and to_decimal(entry(n - 1, detres.amountbeforetax, ";")) != 0:
                    room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , detres.amountbeforetax , ";")))

                elif num_entries(detres.amount, ";") >= 1 and to_decimal(entry(n - 1, detres.amount, ";")) != 0:
                    room_price = to_decimal(round(to_decimal(entry(n - 1 , detres.amount , ";")) / (1 + serv + vat) , 0))

                elif num_entries(detres.amount, ";") <= 1 and num_entries(detres.amountbeforetax, ";") <= 1:

                    if to_decimal(detres.amountbeforetax) != 0:
                        room_price =  to_decimal(to_decimal(detres.amountbeforetax))
                    else:
                        room_price = to_decimal(round(to_decimal(detres.amount) / (1 + serv + vat) , 0))

                elif num_entries(detres.amountbeforetax, ";") >= 1:
                    room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , detres.amountbeforetax , ";")))

                elif num_entries(detres.amount, ";") >= 1:
                    room_price = to_decimal(round(to_decimal(entry(n - 1 , detres.amount , ";")) / (1 + serv + vat) , 0))

            t_fixleist = query(t_fixleist_data, filters=(lambda t_fixleist: t_fixleist.serviceRPH == reslinno and t_fixleist.uniq_id == bookingid and (bill_date >= t_fixleist.start_date and bill_date <= t_fixleist.end_date)), first=True)

            if t_fixleist:

                if t_fixleist.amountaftertax == 0 and t_fixleist.amountbeforetax != 0:
                    t_fixleist.amountaftertax =  to_decimal(t_fixleist.amountbeforetax)

                if t_fixleist.amountbeforetax == 0 and t_fixleist.amountaftertax != 0:
                    t_fixleist.amountbeforetax =  to_decimal(t_fixleist.amountaftertax)

                if tax_included and not detres.base_flag:
                    room_price =  to_decimal(room_price) - to_decimal(t_fixleist.amountaftertax)

                elif not tax_included and not detres.base_flag:
                    room_price =  to_decimal(room_price) - to_decimal(t_fixleist.amountbeforetax)

            if globekey_rsv:

                rate_list = query(rate_list_data, filters=(lambda rate_list: rate_list.room_type == detres.room_type and rate_list.datum == detres.ci_date and rate_list.datum < detres.co_date), first=True)
                room_price =  to_decimal(rate_list.rmrate)
            ci_rate =  to_decimal(room_price)

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, res_info.curr)]})

            if not waehrung:

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, t_curr_name)]})

            if waehrung:
                currno_sm = waehrung.waehrungsnr

            rqueasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, detres.rate_code)]})

            if not rqueasy:
                detres.rate_code = dyna_code

            queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, detres.room_type)]})

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

                zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, detres.room_type)]})

                if zimkateg:
                    rmtype = detres.room_type
                    zikatnr = zimkateg.zikatnr

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

            if zimkateg:
                zikatno = zimkateg.zikatnr

            qsy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, bill_date)],"number1": [(eq, zikatnr)],"char1": [(eq, detres.rate_code)]})

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

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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

                if bill_date == detres.ci_date:
                    ci_rate =  to_decimal(reslin_queasy.deci1)


    def create_reslog():

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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

        nonlocal error_str, done, response, response, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_i, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
        nonlocal room_avail_list_data, rate_list_data, rate_list2_data, nation_list_data

        bill_date:date = None
        statcode:string = ""
        for bill_date in date_range(detres.ci_date,detres.co_date) :
            statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, detres.room_type, 1, 1, globekey_tot_amount, detres.rate_code, argtno))
            rate_list2_data = get_output(calc_dynaratessm(bill_date, bill_date, sm_gastno, detres.rate_code, zikatno, argtno, 1, 1))

            for rate_list2 in query(rate_list2_data):
                rate_list = Rate_list()
                rate_list_data.append(rate_list)

                buffer_copy(rate_list2, rate_list)

        for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.room_type == detres.room_type and rate_list.datum >= detres.ci_date and rate_list.datum < detres.co_date)):
            tot_rmrate_vhp =  to_decimal(tot_rmrate_vhp) + to_decimal(rate_list.rmrate)


    def chk_ascii(str1:string):

        nonlocal error_str, done, response, response, curr_date, exist, expired, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, avail_gdpr, curr_nat, do_it, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, city_str, curr_j, c_number, c_code, c_exp, c_info, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, str_date, m, yy, dd, tmp_given_name, tmp_email, tmp_sure_name, tmp_adress1, tmp_adress2, tmp_country, tmp_phone, tmp_city, tmp_zip, tgastnrmember, tot_guest, curri, str_tot_guest, avalue, p, tahun, service_dept, service_artnr, tax_included, cat_flag, rmtype, double_currency, foreign_rate, ratecode_frate, sm_frate, bill_date, upto_date, zikatnr, n, max_reslinnr, amount, guest, ratecode, nation, queasy, guestseg, reservation, res_line, htparam, zimkateg, artikel, mc_guest, fixleist, arrangement, waehrung, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal res_mode, dyna_code, becode, new_resno, chdelimeter, chdelimeter1, chdelimeter2, chdelimeter3, t_guest_nat, t_curr_name
        nonlocal rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy


        nonlocal room_avail_list, rate_list, rate_list2, res_info, detres, t_fixleist, nation_list, rgast, bguest, bratecode, nationbuf, qsy6, gseg, bres, bres_line, rqueasy, qsy, bqueasy
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

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if becode == 0:

        htparam = get_cache (Htparam, {"paramgruppe": [(eq, 40)],"paramnr": [(eq, 42)]})
        sm_gastno = htparam.finteger
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

        if queasy:
            sm_gastno = queasy.number2

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    tax_included = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

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
        for nationbuf.kurzbez, nationbuf._recid, nationbuf.nationnr, nationbuf.bezeich, qsy6.number1, qsy6.char3, qsy6.number2, qsy6._recid, qsy6.logi2, qsy6.logi1 in db_session.query(Nationbuf.kurzbez, Nationbuf._recid, Nationbuf.nationnr, Nationbuf.bezeich, Qsy6.number1, Qsy6.char3, Qsy6.number2, Qsy6._recid, Qsy6.logi2, Qsy6.logi1).join(Qsy6,(Qsy6.key == 6) & (Qsy6.number1 == Nationbuf.untergruppe) & (matches(Qsy6.char1,"*europe*"))).filter(
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

            if becode == 0:

                htparam = get_cache (Htparam, {"paramgruppe": [(eq, 40)],"paramnr": [(eq, 42)]})

                rgast = get_cache (Guest, {"gastnr": [(eq, htparam.finteger)]})
            else:

                queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, becode)]})

                if queasy:

                    rgast = get_cache (Guest, {"gastnr": [(eq, queasy.number2)]})

            if rgast:
                ota_gastnr = rgast.gastnr
        else:
            ota_gastnr = rgast.gastnr
        bookingid = res_info.uniq_id

        if res_info.ci_date < curr_date:
            done = True
            expired = True
            error_str = error_str + "expired, Reservation Check In Date is Less than Current Check In System Date"

            return generate_output()

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

            for detres in query(detres_data):

                queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, detres.room_type)]})

                if not queasy:

                    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, detres.room_type)]})

                    if not zimkateg:
                        error_str = error_str + chr_unicode(10) + detres.room_type + "No such Room Category"

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

        if not matches(res_info.sure_name,r"*" + r"$#" + r"*"):

            if res_info.email != "":

                guest = get_cache (Guest, {"email_adr": [(eq, res_info.email)],"name": [(eq, res_info.sure_name)],"vorname1": [(eq, res_info.given_name)]})
            else:

                guest = get_cache (Guest, {"name": [(eq, res_info.sure_name)],"vorname1": [(eq, res_info.given_name)],"adresse1": [(eq, res_info.address1)]})

            if not guest:

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

                if c_number != "":
                    guest.ausweis_nr2 = artikel.bezeich + "\\" + c_number + "\\" + c_exp + "|"

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
                    bguest.email_adr = res_info.email


                    pass
                    pass

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
        else:
            tot_guest = num_entries(res_info.sure_name, "$#")
            for curri in range(1,tot_guest + 1) :

                if res_info.given_name != "":
                    tmp_given_name = entry(curri - 1, res_info.given_name, "$#")

                if res_info.sure_name != "":
                    tmp_sure_name = entry(curri - 1, res_info.sure_name, "$#")

                if res_info.email != "" and num_entries(res_info.email, "$#") >= curri:
                    tmp_email = entry(curri - 1, res_info.email, "$#")
                else:
                    tmp_email = ""

                if res_info.address1 != "" and num_entries(res_info.address1, "$#") >= curri:
                    tmp_adress1 = entry(curri - 1, res_info.address1, "$#")
                else:
                    tmp_adress1 = ""

                if res_info.address2 != "" and num_entries(res_info.address2, "$#") >= curri:
                    tmp_adress2 = entry(curri - 1, res_info.address2, "$#")
                else:
                    tmp_adress2 = ""

                if res_info.country != "" and num_entries(res_info.country, "$#") >= curri:
                    tmp_country = entry(curri - 1, res_info.country, "$#")
                else:
                    tmp_country = ""

                if res_info.phone != "" and num_entries(res_info.phone, "$#") >= curri:
                    tmp_phone = entry(curri - 1, res_info.phone, "$#")
                else:
                    tmp_phone = ""

                if res_info.city != "" and num_entries(res_info.city, "$#") >= curri:
                    tmp_city = entry(curri - 1, res_info.city, "$#")
                else:
                    tmp_city = ""

                if res_info.zip != "" and num_entries(res_info.zip, "$#") >= curri:
                    tmp_zip = entry(curri - 1, res_info.zip, "$#")
                else:
                    tmp_zip = ""

                if substring(tmp_given_name, 0, 1) == ("#").lower() :
                    tmp_given_name = substring(tmp_given_name, 1, length(tmp_given_name))

                if substring(tmp_sure_name, 0, 1) == ("#").lower() :
                    tmp_sure_name = substring(tmp_sure_name, 1, length(tmp_sure_name))

                if substring(tmp_adress1, 0, 1) == ("#").lower() :
                    tmp_adress1 = substring(tmp_adress1, 1, length(tmp_adress1))

                if substring(tmp_adress2, 0, 1) == ("#").lower() :
                    tmp_adress2 = substring(tmp_adress2, 1, length(tmp_adress2))

                if substring(tmp_adress1, 0, 1) == ("#").lower() :
                    tmp_adress1 = substring(tmp_adress1, 1, length(tmp_adress1))

                if substring(tmp_adress2, 0, 1) == ("#").lower() :
                    tmp_adress2 = substring(tmp_adress2, 1, length(tmp_adress2))

                if tmp_email != "":

                    guest = db_session.query(Guest).filter(
                             ((Guest.vorname1 == (tmp_given_name).lower()) & (Guest.email_adr == (tmp_email).lower())) | ((Guest.name == (tmp_sure_name).lower()) & (Guest.vorname1 == (tmp_given_name).lower()) & (Guest.adresse1 == (tmp_adress1).lower()))).first()
                else:

                    guest = get_cache (Guest, {"name": [(eq, tmp_sure_name)],"vorname1": [(eq, tmp_given_name)],"adresse1": [(eq, tmp_adress1)]})

                if not guest:

                    nation = get_cache (Nation, {"bezeich": [(eq, tmp_country)]})

                    if nation:
                        t_guest_nat = nation.kurzbez
                    else:
                        t_guest_nat = get_output(if_siteminder_read_mappingbl(2, tmp_country))

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
                                error_str = error_str + chr_unicode(10) + "Unknown country not defined."
                                done = False

                                return generate_output()

                    if substring(tmp_given_name, 0, 1) == ("#").lower() :
                        tmp_given_name = substring(tmp_given_name, 1, length(tmp_given_name))

                    if substring(tmp_sure_name, 0, 1) == ("#").lower() :
                        tmp_sure_name = substring(tmp_sure_name, 1, length(tmp_sure_name))

                    if substring(tmp_adress1, 0, 1) == ("#").lower() :
                        tmp_adress1 = substring(tmp_adress1, 1, length(tmp_adress1))

                    if substring(tmp_adress2, 0, 1) == ("#").lower() :
                        tmp_adress2 = substring(tmp_adress2, 1, length(tmp_adress2))

                    if substring(tmp_city, 0, 1) == ("#").lower() :
                        tmp_city = substring(tmp_city, 1, length(tmp_city))

                    if substring(t_guest_nat, 0, 1) == ("#").lower() :
                        t_guest_nat = substring(t_guest_nat, 1, length(t_guest_nat))

                    if substring(tmp_zip, 0, 1) == ("#").lower() :
                        tmp_zip = substring(tmp_zip, 1, length(tmp_zip))

                    if substring(tmp_email, 0, 1) == ("#").lower() :
                        tmp_email = substring(tmp_email, 1, length(tmp_email))

                    if substring(tmp_phone, 0, 1) == ("#").lower() :
                        tmp_phone = substring(tmp_phone, 1, length(tmp_phone))

                    guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

                    if guest:
                        tgastnrmember = guest.gastnr + 1
                    guest = Guest()
                    db_session.add(guest)

                    guest.gastnr = tgastnrmember
                    guest.name = tmp_sure_name
                    guest.vorname1 = tmp_given_name
                    guest.adresse1 = tmp_adress1
                    guest.adresse2 = tmp_adress2
                    guest.wohnort = tmp_city
                    guest.land = t_guest_nat
                    guest.plz = tmp_zip
                    guest.email_adr = tmp_email
                    guest.telefon = tmp_phone
                    guest.nation1 = t_guest_nat

                    if curri == 1 and c_number != "":
                        guest.ausweis_nr2 = artikel.bezeich + "\\" + c_number + "\\" + c_exp + "|"

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, ota_gastnr)],"reihenfolge": [(eq, 1)]})

                    if guestseg:
                        rsegm = guestseg.segmentcode

                        gseg = get_cache (Guestseg, {"gastnr": [(eq, tgastnrmember)],"segmentcode": [(eq, rsegm)],"reihenfolge": [(eq, 1)]})

                        if not gseg:
                            gseg = Guestseg()
                            db_session.add(gseg)

                            gseg.gastnr = tgastnrmember
                            gseg.reihenfolge = 1
                            gseg.segmentcode = rsegm


                else:
                    tgastnrmember = guest.gastnr

                    bguest = get_cache (Guest, {"_recid": [(eq, guest._recid)]})

                    if bguest and bguest.ausweis_nr2 == "" and c_number != "":
                        pass
                        bguest.ausweis_nr2 = artikel.bezeich + "\\" + c_number + "\\" + c_exp + "|"
                        bguest.email_adr = res_info.email


                        pass
                        pass
                str_tot_guest = str_tot_guest + to_string(tgastnrmember) + ";"

            if res_info.membership != "":

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, tgastnrmember)]})

                if not mc_guest:
                    mc_guest = Mc_guest()
                    db_session.add(mc_guest)

                    mc_guest.gastnr = tgastnrmember
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
        bookingid = res_info.uniq_id
        pass

        if res_mode.lower()  == ("new").lower() :
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
                    reservation.depositgef =  to_decimal(res_info.deposit)

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

        if tot_guest == 1:

            for detres in query(detres_data):
                add_resline()

        elif tot_guest > 1:
            curri = 0

            for detres in query(detres_data):
                curri = curri + 1
                add_resline_acc(to_int(entry(curri - 1, str_tot_guest, ";")))
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
        i = i + 1

    return generate_output()