#using conversion tools version: 1.0.0.117
# =================================================
# Rulita, 29-10-2025
# - Recompile program  
# - Missing table name arrangement
# - Fixing find fist do while resline to foreach
# - Fixing find first arrangement
# =================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
import re
from functions.ratecode_rate import ratecode_rate
from models import Res_line, Htparam, Waehrung, Reservation, Guest, Arrangement, Artikel, Reslin_queasy, Guest_pr, Queasy, Segment, Zimkateg, Fixleist, Katpreis, Pricecod, Argt_line, Pricegrp

def nt_rmratebl():

    prepare_cache ([Res_line, Htparam, Waehrung, Reservation, Arrangement, Reslin_queasy, Guest_pr, Queasy, Segment, Katpreis, Pricecod, Argt_line, Pricegrp])

    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    new_contrate:bool = False
    double_currency:bool = False
    master_exist:bool = False
    bill_date:date = None
    created_date:date = None
    exchg_rate:Decimal = 1
    price_decimal:int = 0
    user_init:string = ""
    ct:string = ""
    st1:string = ""
    st2:string = ""
    contcode:string = ""
    segment_flag:bool = False
    res_line = htparam = waehrung = reservation = guest = arrangement = artikel = reslin_queasy = guest_pr = queasy = segment = zimkateg = fixleist = katpreis = pricecod = argt_line = pricegrp = None

    rline = na_list = None

    na_list_data, Na_list = create_model("Na_list", {"zinr":string, "name":string, "zipreis":Decimal})

    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wd_array, new_contrate, double_currency, master_exist, bill_date, created_date, exchg_rate, price_decimal, user_init, ct, st1, st2, contcode, segment_flag, res_line, htparam, waehrung, reservation, guest, arrangement, artikel, reslin_queasy, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp
        nonlocal rline


        nonlocal rline, na_list
        nonlocal na_list_data

        return {}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal wd_array, new_contrate, double_currency, master_exist, bill_date, created_date, exchg_rate, price_decimal, user_init, ct, st1, st2, contcode, segment_flag, res_line, htparam, waehrung, reservation, guest, arrangement, artikel, reslin_queasy, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp
        nonlocal rline


        nonlocal rline, na_list
        nonlocal na_list_data

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def rm_charge():

        nonlocal wd_array, new_contrate, double_currency, master_exist, bill_date, created_date, exchg_rate, price_decimal, user_init, ct, st1, st2, contcode, segment_flag, res_line, htparam, waehrung, reservation, guest, arrangement, artikel, reslin_queasy, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp
        nonlocal rline


        nonlocal rline, na_list
        nonlocal na_list_data

        bonus:bool = False
        roomrate:Decimal = to_decimal("0.0")
        cid:string = " "
        cdate:string = " "
        argt:string = ""
        c:string = ""
        pax:int = 0
        n:int = 0
        rbuff = None
        Rbuff =  create_buffer("Rbuff",Res_line)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & ((Res_line.erwachs != 0) | (Res_line.kind1 != 0) | (Res_line.kind2 != 0)) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

            guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnr)).first()
            
            # Rulita,
            # - Fixing find first arrangement
            # arrangement = db_session.query(Arrangement).filter(
            #                 (Arrangement.arrangement == res_line.arrangement)).first()
            arrangement = db_session.query(Arrangement).filter(
                            func.lower(func.trim(Arrangement.arrangement)) == func.lower(func.trim(res_line.arrangement))).first()

            artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == arrangement.argt_artikelnr) \
                            & (Artikel.departement == 0)).first()
        
            n = 0

            if matches(res_line.zimmer_wunsch,r"*DATE,*"):
                n = get_index(res_line.zimmer_wunsch, "Date,")

            if n > 0:
                c = substring(res_line.zimmer_wunsch, n + 5 - 1, 8)
                created_date = date_mdy(to_int(substring(c, 4, 2)) , to_int(substring(c, 6, 2)) , to_int(substring(c, 0, 4)))
            else:
                created_date = reservation.resdat
            contcode = ""
            segment_flag = False

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(ge, bill_date),(le, bill_date)]})

            if reslin_queasy and reslin_queasy.char2 != "":
                segment_flag = True
                contcode = reslin_queasy.char2
                ct = res_line.zimmer_wunsch

                rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})

                if not matches(ct,r"*$CODE$*"):
                    rline.zimmer_wunsch = ct + "$CODE$" + contcode + ";"
                else:
                    st1 = substring(ct, 0, get_index(ct, "$CODE$") - 1)
                    st2 = substring(ct, length(st1) + 1 - 1)
                    st2 = substring(st2, get_index(st2, ";") + 1 - 1)
                    ct = st1 + "$CODE$" + contcode + ";" + st2
                    rline.zimmer_wunsch = trim(ct)


                pass
            else:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

                if guest_pr:
                    contcode = guest_pr.code
                ct = res_line.zimmer_wunsch

                if matches(ct,r"*$CODE$*"):
                    ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                    contcode = substring(ct, 0, get_index(ct, ";") - 1)

            if segment_flag  and (contcode != ""):

                queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

                if queasy and entry(0, queasy.char3, ";") != "":

                    segment = get_cache (Segment, {"bezeich": [(eq, entry(0, queasy.char3, ";"))]})

                    if segment:

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                        reservation.segmentcode = segment.segmentcode
                        pass
            bonus = check_bonus()
            roomrate =  to_decimal(res_line.zipreis)
            argt = res_line.arrangement
            pax = res_line.erwachs

            if bonus:
                roomrate =  to_decimal("0")
            else:

                if new_contrate:
                    roomrate, argt, pax = new_update_zipreis(roomrate, argt, pax)
                else:
                    roomrate, argt, pax = update_zipreis(roomrate, argt, pax)

            if (res_line.zipreis != roomrate) or (res_line.arrangement.lower()  != (argt).lower()) or (res_line.erwachs != pax):
                cid = " "
                cdate = " "

                if trim(res_line.changed_id) != "":
                    cid = res_line.changed_id
                    cdate = to_string(res_line.changed)
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "ResChanges"
                reslin_queasy.resnr = res_line.resnr
                reslin_queasy.reslinnr = res_line.reslinnr
                reslin_queasy.date2 = get_current_date()
                reslin_queasy.number2 = get_current_time_in_seconds()


                reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(pax) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(argt) + ";" + to_string(res_line.zipreis) + ";" + to_string(roomrate) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string(res_line.name) + ";"

                if res_line.was_status == 0:
                    reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";" + to_string("YES") + ";"
                else:
                    reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";" + to_string("YES") + ";"
                pass
                pass

                rbuff = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                rbuff.zipreis =  to_decimal(roomrate)

                if argt != rbuff.arrangement:
                    rbuff.arrangement = argt

                if pax != rbuff.erwachs:
                    rbuff.erwachs = pax
                pass
            na_list = Na_list()
            na_list_data.append(na_list)

            na_list.zinr = res_line.zinr
            na_list.name = res_line.name
            na_list.zipreis =  to_decimal(roomrate)


    def check_bonus():

        nonlocal wd_array, new_contrate, double_currency, master_exist, bill_date, created_date, exchg_rate, price_decimal, user_init, ct, st1, st2, contcode, segment_flag, res_line, htparam, waehrung, reservation, guest, arrangement, artikel, reslin_queasy, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp
        nonlocal rline


        nonlocal rline, na_list
        nonlocal na_list_data

        bonus = False
        bonus_array:List[bool] = create_empty_list(999, False)
        i:int = 0
        j:int = 1
        k:int = 0
        n:int = 0
        stay:int = 0
        pay:int = 0
        num_bonus:int = 0
        curr_zikatnr:int = 0
        rmcat = None

        def generate_inner_output():
            return (bonus)

        Rmcat =  create_buffer("Rmcat",Zimkateg)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:

            return generate_inner_output()

        if not guest_pr:

            return generate_inner_output()

        if res_line.l_zuordnung[0] != 0:

            rmcat = db_session.query(Rmcat).filter(
                     (Rmcat.zikatnr == res_line.l_zuordnung[0])).first()
            curr_zikatnr = rmcat.zikatnr
        else:
            curr_zikatnr = res_line.zikatnr

        if new_contrate:

            return generate_inner_output()

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
        j = 1
        for i in range(1,4 + 1) :
            
            # Rulita,
            # - Missing table name arrangement
            stay = to_int(substring(arrangement.options, j - 1, 2))
            pay = to_int(substring(arrangement.options, j + 2 - 1, 2))

            if (stay - pay) > 0:
                n = num_bonus + pay + 1
                for k in range(n,stay + 1) :
                    bonus_array[k - 1] = True
                num_bonus = stay - pay
            j = j + 4
        n = (bill_date - res_line.ankunft + 1).days

        if n >= 1:
            bonus = bonus_array[n - 1]

        return generate_inner_output()


    def new_update_zipreis(roomrate:Decimal, argt:string, pax:int):

        nonlocal wd_array, new_contrate, double_currency, master_exist, bill_date, created_date, exchg_rate, price_decimal, user_init, ct, st1, st2, contcode, segment_flag, res_line, htparam, waehrung, reservation, guest, arrangement, artikel, reslin_queasy, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp
        nonlocal rline


        nonlocal rline, na_list
        nonlocal na_list_data

        rm_rate:Decimal = to_decimal("0.0")
        add_it:bool = False
        qty:int = 0
        it_exist:bool = False
        argt_defined:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
        child1:int = 0
        fix_rate:bool = False
        post_date:date = None
        curr_zikatnr:int = 0
        w_day:int = 0
        ebdisc_flag:bool = False
        kbdisc_flag:bool = False
        rate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        w1 = None
        publish_rate:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (roomrate, argt, pax)

        W1 =  create_buffer("W1",Waehrung)
        rm_rate =  to_decimal(roomrate)
        ebdisc_flag = matches(res_line.zimmer_wunsch, ("*ebdisc*"))
        kbdisc_flag = matches(res_line.zimmer_wunsch, ("*kbdisc*"))

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if not reslin_queasy and res_line.abreise <= bill_date:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, res_line.abreise - timedelta(days=1))],"date2": [(ge, res_line.abreise - timedelta(days=1))]})

        if reslin_queasy:
            roomrate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.char1.lower()  != "" and reslin_queasy.char1.lower()  != (argt).lower() :
                argt = reslin_queasy.char1

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            return generate_inner_output()
        else:

            if it_exist:

                return generate_inner_output()

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if guest_pr:
            post_date = bill_date

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

            if queasy and queasy.logi3:
                post_date = res_line.ankunft
            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, res_line.resnr, res_line.reslinnr, contcode, created_date, post_date, res_line.ankunft, res_line.abreise, res_line.reserve_int, arrangement.argtnr, curr_zikatnr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.reserve_dec, res_line.betriebsnr))

            if rm_rate <= 0.01:
                rm_rate =  to_decimal("0")

            fixleist = get_cache (Fixleist, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
            while None != fixleist:

                # reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"reslinnr": [(eq, res_line.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})
                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == "argt-line") & (Reslin_queasy.char1 == contcode) & (Reslin_queasy.number1 == res_line.reserve_int) & (Reslin_queasy.number2 == arrangement.argtnr) & (Reslin_queasy.reslinnr == res_line.zikatnr) & (Reslin_queasy.number3 == fixleist.artnr) & (Reslin_queasy.resnr == fixleist.departement) & (Reslin_queasy.date1 <= post_date) & (Reslin_queasy.date2 >= post_date)).with_for_update().first()

                if reslin_queasy:
                    pass
                    fixleist.betrag =  to_decimal(reslin_queasy.deci1)
                    pass

                curr_recid = fixleist._recid
                fixleist = db_session.query(Fixleist).filter(
                         (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist._recid > curr_recid)).first()
            roomrate =  to_decimal(rm_rate)

            return generate_inner_output()
        else:
            w_day = wd_array[get_weekday(bill_date - 1) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date - timedelta(days=1))],"endperiode": [(ge, bill_date - timedelta(days=1))],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date - timedelta(days=1))],"endperiode": [(ge, bill_date - timedelta(days=1))],"betriebsnr": [(eq, 0)]})

            if not katpreis:

                return generate_inner_output()

            if res_line.zipreis != get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2):

                return generate_inner_output()
            w_day = wd_array[get_weekday(bill_date) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

            if katpreis:
                publish_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                if publish_rate == 0:

                    return generate_inner_output()
                roomrate =  to_decimal(publish_rate)

        return generate_inner_output()


    def update_zipreis(roomrate:Decimal, argt:string, pax:int):

        nonlocal wd_array, new_contrate, double_currency, master_exist, bill_date, created_date, exchg_rate, price_decimal, user_init, ct, st1, st2, contcode, segment_flag, res_line, htparam, waehrung, reservation, guest, arrangement, artikel, reslin_queasy, guest_pr, queasy, segment, zimkateg, fixleist, katpreis, pricecod, argt_line, pricegrp
        nonlocal rline


        nonlocal rline, na_list
        nonlocal na_list_data

        rm_rate:Decimal = to_decimal("0.0")
        resline = None
        add_it:bool = False
        qty:int = 0
        it_exist:bool = False
        argt_defined:bool = False
        exrate1:Decimal = 1
        ex2:Decimal = 1
        child1:int = 0
        fix_rate:bool = False
        post_date:date = None
        curr_zikatnr:int = 0
        w_day:int = 0
        w1 = None
        publish_rate:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (roomrate, argt, pax)

        Resline =  create_buffer("Resline",Res_line)
        W1 =  create_buffer("W1",Waehrung)
        rm_rate =  to_decimal(roomrate)

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, bill_date)],"date2": [(ge, bill_date)]})

        if reslin_queasy:
            roomrate =  to_decimal(reslin_queasy.deci1)

            if reslin_queasy.char1.lower()  != "" and reslin_queasy.char1.lower()  != (argt).lower() :
                argt = reslin_queasy.char1

            if reslin_queasy.number3 != 0:
                pax = reslin_queasy.number3

            return generate_inner_output()
        else:

            if it_exist:

                return generate_inner_output()

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if guest_pr:
            post_date = bill_date

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_line.reserve_int)]})

            if queasy and queasy.logi3:
                post_date = res_line.ankunft

            pricecod = get_cache (Pricecod, {"code": [(eq, contcode)],"marknr": [(eq, res_line.reserve_int)],"argtnr": [(eq, arrangement.argtnr)],"zikatnr": [(eq, curr_zikatnr)],"startperiode": [(le, post_date)],"endperiode": [(ge, post_date)]})

            if pricecod:

                if res_line.kind1 <= pricecod.betriebsnr:
                    child1 = 0
                else:
                    child1 = res_line.kind1 - pricecod.betriebsnr
                rm_rate =  to_decimal(pricecod.perspreis[res_line.erwachs - 1] + pricecod.kindpreis[0]) * to_decimal(child1 + pricecod.kindpreis[1]) * to_decimal(res_line.kind2)

                w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})

                if w1:
                    exrate1 =  to_decimal(w1.ankauf) / to_decimal(w1.einheit)

                if res_line.reserve_dec != 0:
                    ex2 =  to_decimal(ex2) / to_decimal(res_line.reserve_dec)
                else:

                    w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if w1:
                        ex2 = ( to_decimal(w1.ankauf) / to_decimal(w1.einheit))

                for argt_line in db_session.query(Argt_line).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind1) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
                    add_it = False

                    if argt_line.vt_percnt == 0:

                        if argt_line.betriebsnr == 0:
                            qty = res_line.erwachs
                        else:
                            qty = argt_line.betriebsnr

                    elif argt_line.vt_percnt == 1:
                        qty = child1

                    elif argt_line.vt_percnt == 2:
                        qty = res_line.kind2

                    if qty > 0:

                        if argt_line.fakt_modus == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 2:

                            if res_line.ankunft == post_date:
                                add_it = True

                        elif argt_line.fakt_modus == 3:

                            if (res_line.ankunft + 1) == post_date:
                                add_it = True

                        elif argt_line.fakt_modus == 4 and get_day(post_date) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 5 and get_day(post_date + 1) == 1:
                            add_it = True

                        elif argt_line.fakt_modus == 6:

                            if (res_line.ankunft + (argt_line.intervall - 1)) >= post_date:
                                add_it = True

                    if add_it:
                        argt_defined = False

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"number1": [(eq, argt_line.departement)],"number2": [(eq, argt_line.argtnr)],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number3": [(eq, argt_line.argt_artnr)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})

                        if reslin_queasy:
                            argt_defined = True

                            if argt_line.vt_percnt == 0:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                            elif argt_line.vt_percnt == 1:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                            elif argt_line.vt_percnt == 2:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)

                        if not argt_defined:

                            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, pricecod.code)],"number1": [(eq, pricecod.marknr)],"number2": [(eq, pricecod.argtnr)],"reslinnr": [(eq, pricecod.zikatnr)],"number3": [(eq, argt_line.argt_artnr)],"resnr": [(eq, argt_line.departement)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})

                            if reslin_queasy:

                                if argt_line.vt_percnt == 0:
                                    rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci1) * to_decimal(qty)

                                elif argt_line.vt_percnt == 1:
                                    rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci2) * to_decimal(qty)

                                elif argt_line.vt_percnt == 2:
                                    rm_rate =  to_decimal(rm_rate) + to_decimal(reslin_queasy.deci3) * to_decimal(qty)
                            else:
                                rm_rate =  to_decimal(rm_rate) + to_decimal(argt_line.betrag) * to_decimal(qty) * to_decimal(exrate1) / to_decimal(ex2)

                fixleist = get_cache (Fixleist, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})
                while None != fixleist:

                    # reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, pricecod.code)],"number1": [(eq, pricecod.marknr)],"number2": [(eq, pricecod.argtnr)],"reslinnr": [(eq, pricecod.zikatnr)],"number3": [(eq, fixleist.artnr)],"resnr": [(eq, fixleist.departement)],"date1": [(le, post_date)],"date2": [(ge, post_date)]})
                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == "argt-line") & (Reslin_queasy.char1 == pricecod.code) & (Reslin_queasy.number1 == pricecod.marknr) & (Reslin_queasy.number2 == pricecod.argtnr) & (Reslin_queasy.reslinnr == pricecod.zikatnr) & (Reslin_queasy.number3 == fixleist.artnr) & (Reslin_queasy.resnr == fixleist.departement) & (Reslin_queasy.date1 <= post_date) & (Reslin_queasy.date2 >= post_date)).with_for_update().first()

                    if reslin_queasy:
                        pass
                        fixleist.betrag =  to_decimal(reslin_queasy.deci1)
                        pass

                    curr_recid = fixleist._recid
                    fixleist = db_session.query(Fixleist).filter(
                                 (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr) & (Fixleist._recid > curr_recid)).first()
            else:

                pricegrp = get_cache (Pricegrp, {"code": [(eq, contcode)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)]})

                if pricegrp:
                    rm_rate =  to_decimal(pricegrp.perspreis[res_line.erwachs - 1])

                if res_line.kind1 == 1 or res_line.kind1 == 2:
                    rm_rate =  to_decimal(rm_rate) + to_decimal(pricecod.kindpreis[res_line.kind1 - 1])
            roomrate =  to_decimal(rm_rate)

            return generate_inner_output()
        else:
            w_day = wd_array[get_weekday(bill_date - 1) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date - timedelta(days=1))],"endperiode": [(ge, bill_date - timedelta(days=1))],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date - timedelta(days=1))],"endperiode": [(ge, bill_date - timedelta(days=1))],"betriebsnr": [(eq, 0)]})

            if not katpreis:

                return generate_inner_output()

            if res_line.zipreis != get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2):

                return generate_inner_output()
            w_day = wd_array[get_weekday(bill_date) - 1]

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, w_day)]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, bill_date)],"endperiode": [(ge, bill_date)],"betriebsnr": [(eq, 0)]})

            if katpreis:
                publish_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))

                if publish_rate == 0:

                    return generate_inner_output()
                roomrate =  to_decimal(publish_rate)

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
    user_init = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})

    if htparam.flogical or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    rm_charge()

    return generate_output()