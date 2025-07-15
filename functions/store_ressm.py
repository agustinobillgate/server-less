from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.mapping import mapping
from functions.global_allotment_number import global_allotment_number
from functions.find_dyna_ratecodesm import find_dyna_ratecodesm
from functions.ratecode_rate import ratecode_rate
from functions.calc_dynaratessm import calc_dynaratessm
from models import Guest, Ratecode, Htparam, Zimkateg, Reservation, Res_line, Nation, Guestseg, Arrangement, Waehrung, Queasy, Reslin_queasy, Guest_pr, Pricecod, Resplan

res_info_list, Res_info = create_model("Res_info", {"res_time":str, "res_id":str, "ota_code":str, "no_room":int, "rate_code":str, "room_type":str, "ci_date":date, "co_date":date, "amount":str, "curr":str, "adult":str, "child1":str, "child2":str, "remark":str, "eta":str, "given_name":str, "sure_name":str, "phone":str, "email":str, "address1":str, "address2":str, "city":str, "zip":str, "state":str, "country":str, "commission":str, "night":int, "amount_at":str, "curr_at":str, "argtnr":str})

def store_ressm(res_info_list:[Res_info]):
    error_str = ""
    done = False
    variable = None
    variable = None
    variable = None
    variable = None
    variable = None
    variable = None
    response:str = ""
    response:str = ""
    curr_date:date = None
    exist:bool = False
    curr_error_str:str = ""
    sm_gastno:int = 0
    inp_resno:int = 0
    ota_gastnr:int = 0
    rsegcode:int = 0
    resart:int = 0
    gastnrmember:int = 1
    rsegm:int = 0
    resstatus:int = 1
    i:int = 1
    new_resno:int = 1
    markno:int = 0
    argtno:int = 0
    zikatno:int = 0
    currno:int = 0
    rm_qty:int = 0
    card_name:str = ""
    card_no:str = ""
    argt:str = ""
    ratecode1:str = ""
    guest_nat:str = ""
    eta_char:str = ""
    hh:str = ""
    mm:str = ""
    bookingid:str = ""
    card_exist:bool = False
    new_contrate:bool = False
    restricted_disc:bool = False
    use_it:bool = False
    ci_rate:decimal = to_decimal("0.0")
    ci_rate1:decimal = to_decimal("0.0")
    room_price:decimal = to_decimal("0.0")
    price_decimal:int = 0
    globekey_rsv:bool = False
    globekey_tot_amount:decimal = to_decimal("0.0")
    tot_rmrate_vhp:decimal = to_decimal("0.0")
    asc_str:str = ""
    n:int = 0
    qty:int = 0
    j:int = 1
    k:int = 1
    guest = ratecode = htparam = zimkateg = reservation = res_line = nation = guestseg = arrangement = waehrung = queasy = reslin_queasy = guest_pr = pricecod = resplan = None

    rate_list = rate_list2 = res_info = rgast = bratecode = detres = None

    rate_list_list, Rate_list = create_model("Rate_list", {"datum":date, "currency":str, "rmrate":decimal, "updateflag":bool, "occ_rooms":int, "rcode":str, "rcmap":str, "room_type":str})
    rate_list2_list, Rate_list2 = create_model_like(Rate_list)
    detres_list, Detres = create_model("Detres", {"reslinnr":int, "amount":str, "adult":int, "child1":int, "child2":int})

    Rgast = create_buffer("Rgast",Guest)
    Bratecode = create_buffer("Bratecode",Ratecode)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        return {"error_str": error_str, "done": done}

    def add_resline():

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        new_reslinno:int = 1
        allotnr:int = 0
        statcode:str = ""

        if new_contrate:
            statcode = create_new_fixrate(new_resno, detRes.reslinnr)
        else:
            create_fixed_rate(new_resno, detRes.reslinnr)

        if res_info.eta != "":
            hh = entry(0, res_info.eta, ":")
            mm = entry(1, res_info.eta, ":")
            eta_char = hh + mm
        else:
            eta_char = "0000"
        allotnr = get_output(global_allotment_number(sm_gastno, ota_gastnr, res_info.ci_date, res_info.co_date, res_info.room_type))
        res_line = Res_line()
        db_session.add(res_line)

        res_line.resnr = new_resno
        res_line.reslinnr = detRes.reslinnr
        res_line.gastnr = ota_gastnr
        res_line.gastnrmember = gastnrmember
        res_line.gastnrpay = gastnrmember
        res_line.ankunft = res_info.ci_date
        res_line.abreise = res_info.co_date
        res_line.anztage = res_info.co_date -
        res_info.ci_date
        res_line.flight_nr = " " + to_string(eta_char, "x(5)") +\
                " "
        res_line.name = guest.name + ", " + guest.vorname1 +\
                ", " + guest.anrede1
        res_line.arrangement = argt
        res_line.resstatus = resstatus
        res_line.erwachs = detRes.adult
        res_line.kind1 = detRes.child1
        res_line.kind2 = detRes.child2
        res_line.betriebsnr = currno
        res_line.bemerk = res_info.remark + chDelimeter1 +\
                "SM-TIME," + res_info.res_time
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
            res_line.zimmer_wunsch = "ebdisc;restricted;date," + to_string(get_year(curr_date)) + to_string(get_month(curr_date) , "99") + to_string(get_day(curr_date) , "99") + ";" + "voucher" + bookingid + ";" + "$CODE$" + statcode + ";"
        rm_qty = res_line.zimmeranz
        create_resplan()
        create_reslog()
        error_str = error_str + "CUR" + chDelimeter1 + to_string(res_line.betriebsnr)
        pass


    def create_new_fixrate(resno:int, reslinno:int):

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        statcode = ""
        bill_date:date = None
        upto_date:date = None
        rate_found:bool = False
        rmrate:decimal = to_decimal("0.0")
        kback_flag:bool = False
        n:int = 0
        curr_name:str = ""
        ratecode_curr:str = ""
        ratecode_frate:decimal = 1
        sm_frate:decimal = 1
        currno_sm:int = 0
        bres = None
        bres_line = None

        def generate_inner_output():
            return (statcode)

        Bres =  create_buffer("Bres",Reservation)
        Bres_line =  create_buffer("Bres_line",Res_line)

        if res_info.ci_date == res_info.co_date:
            upto_date = res_info.co_date
        else:
            upto_date = res_info.co_date - timedelta(days=1)

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_info.argtnr)).first()

        if arrangement:
            argtno = arrangement.argtnr
        for bill_date in date_range(res_info.ci_date,upto_date) :
            n = n + 1
            currno = 0
            markno = 0

            if num_entries(detRes.amount, ";") >= 1:
                room_price =  to_decimal(to_decimal(entry(n) - to_decimal(1 , detRes.amount , ";")))
            else:
                room_price =  to_decimal(to_decimal(detRes.amount))

            if globekey_rsv:

                rate_list = query(rate_list_list, filters=(lambda rate_list: rate_list.room_type == res_info.room_type and rate_list.datum == res_info.ci_date and rate_list.datum < res_info.co_date), first=True)
                room_price =  to_decimal(rate_list.rmrate)
            ci_rate =  to_decimal(room_price)

            if res_info.curr != "":

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.wabkurz == res_info.curr)).first()

                if not waehrung:
                    curr_name = get_output(mapping(2, curr_map, res_info.curr))

                    waehrung = db_session.query(Waehrung).filter(
                             (func.lower(Waehrung.wabkurz) == (curr_name).lower())).first()

                if waehrung:
                    currno_sm = waehrung.waehrungsnr
            statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, res_info.room_type, detRes.adult, detRes.child1, room_price, res_info.rate_code, argtno))

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 18) & (Queasy.number1 == markno)).first()

            if queasy and queasy.char3 != "":

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.wabkurz == queasy.char3)).first()

                if waehrung:
                    currno = waehrung.waehrungsnr

            if currno_sm != currno:

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == currno) & (Waehrung.betriebsnr == 0)).first()

                if waehrung:
                    ratecode_frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.wabkurz == res_info.curr) & (Waehrung.betriebsnr == 0)).first()

                if waehrung:
                    sm_frate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                ci_rate =  to_decimal(ci_rate) * to_decimal((sm_frate) / to_decimal(ratecode_frate))
                ci_rate = to_decimal(round(ci_rate , price_decimal))
                statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, res_info.room_type, detRes.adult, detRes.child1, ci_rate, res_info.rate_code, argtno))

            if argtno == 0:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == res_info.rate_code) & (Ratecode.zikatNr == zikatno)).first()

                if not ratecode:
                    error_str = error_str + "Arrangement Not Found " + res_info.rate_code + " " + to_string(zikatno)

                    arrangement = db_session.query(Arrangement).first()

                    if arrangement:
                        argt = arrangement.arrangement

            elif markno == 0:
                error_str = error_str + "Market Segment Not Found."

            if currno == 0:
                error_str = error_str + "Currency Not Found : " + to_string(res_info.curr)

                waehrung = db_session.query(Waehrung).first()

                if waehrung:
                    currno = waehrung.waehrungsnr

            if argtno != 0:

                arrangement = db_session.query(Arrangement).filter(
                         (Arrangement.argtnr == argtno)).first()

                if arrangement:
                    argt = arrangement.arrangement
            rate_found, rmrate, restricted_disc, kback_flag = get_output(ratecode_rate(True, True, resno, reslinno, ("!" + statcode), curr_date, bill_date, res_info.ci_date, res_info.co_date, markno, argtno, zikatno, detRes.adult, detRes.child1, detRes.child2, 0, currno))
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

            if bill_date == res_info.ci_date:
                ci_rate1 =  to_decimal(ci_rate)

        return generate_inner_output()


    def create_fixed_rate(resno:int, reslinno:int):

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        bill_date:date = None

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == ota_gastnr)).first()

        if not guest_pr:

            return

        ratecode = db_session.query(Ratecode).filter(
                 (Ratecode.code == guest_pr.code)).first()

        if ratecode:
            markno = ratecode.marknr
            argtno = ratecode.argtnr

        if argtno == 0:

            return
        else:

            arrangement = db_session.query(Arrangement).filter(
                     (Arrangement.argtnr == argtno)).first()

            if arrangement:
                argt = arrangement.arrangement
        for bill_date in date_range(res_info.ci_date,res_info.co_date) :

            pricecod = db_session.query(Pricecod).filter(
                     (Pricecod.code == guest_pr.code) & (Pricecod.marknr == markno) & (Pricecod.argtnr == arrangement.argtnr) & (Pricecod.zikatnr == zikatno) & (Pricecod.startperiode <= bill_date) & (Pricecod.endperiode >= bill_date)).first()

            if pricecod:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = resno
                reslin_queasy.reslinnr = reslinno
                reslin_queasy.date1 = bill_date
                reslin_queasy.date2 = bill_date
                reslin_queasy.deci1 =  to_decimal(pricecod.perspreis[detRes.adult - 1] +\
                        pricecod.kindpreis[0]) * to_decimal(detRes.child1)
                reslin_queasy.char1 = argt

                if bill_date == ci_date:
                    ci_rate =  to_decimal(reslin_queasy.deci1)


    def create_reslog():

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        guest1 = None
        cid:str = " "
        cdate:str = " "
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


    def create_resplan():

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        curr_date:date = None
        for curr_date in date_range(res_line.ankunft,(res_line.abreise - 1)) :

            resplan = db_session.query(Resplan).filter(
                     (Resplan.zikatnr == res_line.zikatnr) & (Resplan.datum == curr_date)).first()

            if not resplan:
                resplan = Resplan()
                db_session.add(resplan)

                resplan.datum = curr_date


                resplan.zikatnr = res_line.zikatnr
            resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] + res_line.zimmeranz
            pass


    def calc_commisions(room_price:decimal):

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        ccommission:str = "0"
        dcommission:decimal = 0
        decs:decimal = 0
        points:str = ""

        def generate_inner_output():
            return (room_price)

        ccommission = res_info.commission

        if re.match(r".*%.*",ccommission, re.IGNORECASE):
            ccommission = trim(replace_str(ccommission, "%", ""))

        if re.match(r".*,.*",ccommission, re.IGNORECASE):
            decs =  to_decimal(to_decimal(entry(0 , ccommission , ",")) )
            points = entry(1, ccommission, ",")

        elif re.match(r".*..*",ccommission, re.IGNORECASE) and num_entries(ccommission, ".") >= 2:
            decs =  to_decimal(to_decimal(entry(0 , ccommission , ".")) )
            points = entry(1, ccommission, ".")


        else:
            decs =  to_decimal(to_decimal(ccommission) )
            points = "0"


        dcommission = decs + (to_decimal(substring(points, 0, 1)) / 10) + (to_decimal(substring(points, 1, 1)) / 100) + (to_decimal(substring(points, 2, 1)) / 1000)
        room_price = to_decimal(round(room_price * (1 + (dcommission / 100)) , 2))

        return generate_inner_output()


    def check_vhp_rsv():

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        bill_date:date = None
        statcode:str = ""
        for bill_date in date_range(res_info.ci_date,res_info.co_date) :
            statcode, argtno, markno, currno = get_output(find_dyna_ratecodesm(ota_gastnr, bill_date, res_info.room_type, 1, 1, globekey_tot_amount, res_info.rate_code, argtno))
            rate_list2_list = get_output(calc_dynaratessm(bill_date, bill_date, sm_gastno, res_info.rate_code, zikatno, argtno, 1, 1))

            for rate_list2 in query(rate_list2_list):
                rate_list = Rate_list()
                rate_list_list.append(rate_list)

                buffer_copy(rate_list2, rate_list)

        for rate_list in query(rate_list_list, filters=(lambda rate_list: rate_list.room_type == res_info.room_type and rate_list.datum >= res_info.ci_date and rate_list.datum < res_info.co_date)):
            tot_rmrate_vhp =  to_decimal(tot_rmrate_vhp) + to_decimal(rate_list.rmrate)


    def chk_ascii(str1:str):

        nonlocal error_str, done, variable, variable, variable, variable, variable, variable, response, response, curr_date, exist, curr_error_str, sm_gastno, inp_resno, ota_gastnr, rsegcode, resart, gastnrmember, rsegm, resstatus, i, new_resno, markno, argtno, zikatno, currno, rm_qty, card_name, card_no, argt, ratecode1, guest_nat, eta_char, hh, mm, bookingid, card_exist, new_contrate, restricted_disc, use_it, ci_rate, ci_rate1, room_price, price_decimal, globekey_rsv, globekey_tot_amount, tot_rmrate_vhp, asc_str, n, qty, j, k, guest, ratecode, htparam, zimkateg, reservation, res_line, nation, guestseg, arrangement, waehrung, queasy, reslin_queasy, guest_pr, pricecod, resplan
        nonlocal rgast, bratecode


        nonlocal rate_list, rate_list2, res_info, rgast, bratecode, detres
        nonlocal rate_list_list, rate_list2_list, detres_list

        str2 = ""
        curr_i:int = 0

        def generate_inner_output():
            return (str2)

        str2 = ""
        for curr_i in range(1,len(str1)  + 1) :

            if asc(substring(str1, curr_i - 1, 1)) == 10:
                str2 = str2 + " "

            elif asc(substring(str1, curr_i - 1, 1)) < 32:
                str2 = str2 + ""

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

            elif asc(substring(str1, curr_i - 1, 1)) > 127:
                str2 = str2 + "-"
            else:
                str2 = str2 + substring(str1, curr_i - 1, 1)

        return generate_inner_output()


    if substring(proversion(), 0, 1) == ("1").lower() :
        &elseif substring(proversion(), 0, 1) = "9" THEN


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramgr == 40) & (Htparam.paramnr == 42)).first()
    sm_gastno = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 67)).first()
    rsegcode = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 69)).first()
    resart = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    res_info = query(res_info_list, first=True)

    if res_info:

        guest = db_session.query(Guest).filter(
                 (func.lower(trim(entry(0, Guest.steuernr, "-"))).op("~")((trim(res_info.ota_code.lower().replace("*",".*")))))).first()

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

    res_info = query(res_info_list, first=True)

    if res_info:

        rgast = db_session.query(Rgast).filter(
                 (trim(entry(0, Rgast.steuernr, "|"func.lower())).op("~")((trim(res_info.ota_code.lower().replace("*",".*")))))).first()

        if not rgast:
            error_str = error_str + "Reservation TA File not found for : " + trim(res_info.ota_code) + ". "

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramgr == 40) & (Htparam.paramnr == 42)).first()

            rgast = db_session.query(Rgast).filter(
                     (Rgast.gastnr == htparam.finteger)).first()

            if rgast:
                ota_gastnr = rgast.gastnr
        else:
            ota_gastnr = rgast.gastnr

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.kurzbez == res_info.room_type)).first()

        if not zimkateg:
            error_str = error_str + chr(10) + res_info.room_type + "No such Room Category"

            return generate_output()
        else:
            zikatno = zimkateg.zikatnr
        bookingid = res_info.res_id

        reservation = db_session.query(Reservation).filter(
                 (Reservation.vesrdepot == bookingid) & (Reservation.gastnr == ota_gastnr)).first()

        if reservation:

            res_line = db_session.query(Res_line).filter(
                     (Res_line.gastnr == ota_gastnr) & (Res_line.ankunft == res_info.ci_date) & (func.lower(Res_line.zimmer_wunsch).op("~")(("*voucher" + bookingid + "*".lower().replace("*",".*"))))).first()

            if res_line:
                error_str = error_str + chr(10) + "Reservation " + res_info.res_id + " already exist."


                exist = True

                return generate_output()

        if exist:

            return generate_output()

        if re.match(r"GKY",trim(res_info.ota_code), re.IGNORECASE):
            globekey_rsv = True

        if globekey_rsv:
            n = n + 1

            if num_entries(res_info.amount_at, ";") >= 1:
                globekey_tot_amount =  to_decimal(to_decimal(entry(n) - to_decimal(1 , res_info.amount_at , ";")))
            else:
                globekey_tot_amount =  to_decimal(to_decimal(res_info.amount_at))
            check_vhp_rsv()

            if tot_rmrate_vhp != globekey_tot_amount:
                error_str = error_str + chr(10) +\
                        "Total Roomrate between VHP and Globekey NOT MATCHES" +\
                        " GKY amount:" + to_string(globekey_tot_amount) + chr(10) +\
                        " VHP amount:" + to_string(tot_rmrate_vhp)

                return generate_output()
            else:

                if res_info.no_room > 1:
                    pass
                else:
                    detres = Detres()
                    detres_list.append(detres)

                    detres.reslinnr = 1
                    detres.adult = to_int(res_info.adult)
                    detres.child1 = to_int(res_info.child1)
                    detres.child2 = to_int(res_info.child2)


                    detres.amount = res_info.amount_at
                pass

                if res_info.email != "":

                    guest = db_session.query(Guest).filter(
                                 ((Guest.vorname1 == res_info.given_name) & (Guest.email_adr == res_info.email)) | ((Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name) & (Guest.adresse1 == res_info.address1))).first()
                else:

                    guest = db_session.query(Guest).filter(
                                 ((Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name) & (Guest.adresse1 == res_info.address1))).first()

                if not guest:

                    nation = db_session.query(Nation).filter(
                                 (Nation.bezeich == res_info.country)).first()

                    if nation:
                        guest_nat = nation.kurzbez
                    else:
                        guest_nat = get_output(mapping(1, cou_map, res_info.country))

                        nation = db_session.query(Nation).filter(
                                     (func.lower(Nation.bezeich) == (guest_nat).lower())).first()

                        if nation:
                            guest_nat = nation.kurzbez
                        else:

                            nation = db_session.query(Nation).filter(
                                         (func.lower(Nation.bezeich).op("~")(("*Unknown*".lower().replace("*",".*"))))).first()

                            if nation:
                                guest_nat = nation.kurzbez
                            else:
                                error_str = error_str + chr(10) + "Unknown country not defined."
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
                    guest.land = guest_nat
                    guest.plz = res_info.zip
                    guest.email_adr = res_info.email
                    guest.telefon = res_info.phone
                    guest.nation1 = guest_nat

                    guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == ota_gastnr) & (Guestseg.reihenfolge == 1)).first()

                    if guestseg:
                        rsegm = guestseg.segmentcode
                        guestseg = Guestseg()
                        db_session.add(guestseg)

                        guestseg.gastnr = gastnrmember
                        guestseg.reihenfolge = 1
                        guestseg.segmentcode = rsegm


                else:
                    gastnrmember = guest.gastnr
                bookingid = res_info.res_id
                pass

                guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == rgast.gastnr) & (Guestseg.reihenfolge == 1)).first()

                if not guestseg:

                    guestseg = db_session.query(Guestseg).filter(
                                     (Guestseg.gastnr == rgast.gastnr)).first()

                reservation = db_session.query(Reservation).first()

                if reservation:
                    new_resno = reservation.resnr + 1
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

                for detres in query(detres_list):
                    add_resline()
                done = True
                curr_error_str = "OC" + chDelimeter1 + res_info.ota_code + chDelimeter2 +\
                        "RC" + chDelimeter1 + res_info.rate_code + chDelimeter2 +\
                        "RT" + chDelimeter1 + res_info.room_type + chDelimeter2 +\
                        "CI" + chDelimeter1 + to_string(res_info.ci_date, "99/99/9999") + chDelimeter2 +\
                        "CO" + chDelimeter1 + to_string(res_info.co_date, "99/99/9999") + chDelimeter2 +\
                        "AM" + chDelimeter1 + res_info.amount + chDelimeter2 +\
                        "AMT" + chDelimeter1 + res_info.amount_at + chDelimeter2 +\
                        "NR" + chDelimeter1 + to_string(res_info.no_room) + chDelimeter2 +\
                        "AD" + chDelimeter1 + to_string(res_info.adult) + chDelimeter2 +\
                        "CH1" + chDelimeter1 + to_string(res_info.child1) + chDelimeter2 +\
                        "CH2" + chDelimeter1 + to_string(res_info.child2) + chDelimeter2 +\
                        "GN" + chDelimeter1 + res_info.sure_name + "," + res_info.given_name + chDelimeter2 +\
                        error_str


                error_str = error_str + curr_error_str
                i = i + 1

        else:

            if res_info.no_room > 1:
                qty = res_info.no_room
                for j in range(1,qty  + 1) :
                    detres = Detres()
                    detres_list.append(detres)

                    detres.reslinnr = j

                    if res_info.night == 1:
                        detres.amount = entry(j - 1, res_info.amount, "-")
                        detres.adult = to_int(entry(j - 1, res_info.adult, "-"))
                        detres.child1 = to_int(entry(j - 1, res_info.child1, "-"))
                        detres.child2 = to_int(entry(j - 1, res_info.child2, "-"))


                    else:
                        for k in range(1,res_info.night  + 1) :
                            detres.amount = detres.amount + entry(j - 1, res_info.amount, "-")
            else:
                detres = Detres()
                detres_list.append(detres)

                detres.reslinnr = 1
                detres.adult = to_int(res_info.adult)
                detres.child1 = to_int(res_info.child1)
                detres.child2 = to_int(res_info.child2)


                for k in range(1,res_info.night  + 1) :
                    detres.amount = detres.amount + res_info.amount
            pass

            if res_info.email != "":

                guest = db_session.query(Guest).filter(
                             ((Guest.vorname1 == res_info.given_name) & (Guest.email_adr == res_info.email)) | ((Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name) & (Guest.adresse1 == res_info.address1))).first()
            else:

                guest = db_session.query(Guest).filter(
                             ((Guest.name == res_info.sure_name) & (Guest.vorname1 == res_info.given_name) & (Guest.adresse1 == res_info.address1))).first()

            if not guest:

                nation = db_session.query(Nation).filter(
                             (Nation.bezeich == res_info.country)).first()

                if nation:
                    guest_nat = nation.kurzbez
                else:
                    guest_nat = get_output(mapping(1, cou_map, res_info.country))

                    nation = db_session.query(Nation).filter(
                                 (func.lower(Nation.bezeich) == (guest_nat).lower())).first()

                    if nation:
                        guest_nat = nation.kurzbez
                    else:

                        nation = db_session.query(Nation).filter(
                                     (func.lower(Nation.bezeich).op("~")(("*Unknown*".lower().replace("*",".*"))))).first()

                        if nation:
                            guest_nat = nation.kurzbez
                        else:
                            error_str = error_str + chr(10) + "Unknown country not defined."
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
                guest.land = guest_nat
                guest.plz = res_info.zip
                guest.email_adr = res_info.email
                guest.telefon = res_info.phone
                guest.nation1 = guest_nat

                guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == ota_gastnr) & (Guestseg.reihenfolge == 1)).first()

                if guestseg:
                    rsegm = guestseg.segmentcode
                    guestseg = Guestseg()
                    db_session.add(guestseg)

                    guestseg.gastnr = gastnrmember
                    guestseg.reihenfolge = 1
                    guestseg.segmentcode = rsegm


            else:
                gastnrmember = guest.gastnr
            bookingid = res_info.res_id
            pass

            guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == rgast.gastnr) & (Guestseg.reihenfolge == 1)).first()

            if not guestseg:

                guestseg = db_session.query(Guestseg).filter(
                                 (Guestseg.gastnr == rgast.gastnr)).first()

            reservation = db_session.query(Reservation).first()

            if reservation:
                new_resno = reservation.resnr + 1
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

            for detres in query(detres_list):
                add_resline()
            done = True
            curr_error_str = "OC" + chDelimeter1 + res_info.ota_code + chDelimeter2 +\
                    "RC" + chDelimeter1 + res_info.rate_code + chDelimeter2 +\
                    "RT" + chDelimeter1 + res_info.room_type + chDelimeter2 +\
                    "CI" + chDelimeter1 + to_string(res_info.ci_date, "99/99/9999") + chDelimeter2 +\
                    "CO" + chDelimeter1 + to_string(res_info.co_date, "99/99/9999") + chDelimeter2 +\
                    "AM" + chDelimeter1 + res_info.amount + chDelimeter2 +\
                    "NR" + chDelimeter1 + to_string(res_info.no_room) + chDelimeter2 +\
                    "AD" + chDelimeter1 + to_string(res_info.adult) + chDelimeter2 +\
                    "CH1" + chDelimeter1 + to_string(res_info.child1) + chDelimeter2 +\
                    "CH2" + chDelimeter1 + to_string(res_info.child2) + chDelimeter2 +\
                    "GN" + chDelimeter1 + res_info.sure_name + "," + res_info.given_name + chDelimeter2 +\
                    error_str


            error_str = error_str + curr_error_str
            i = i + 1


    return generate_output()