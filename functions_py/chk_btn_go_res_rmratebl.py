#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 25/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Waehrung, Res_line, Bediener, Arrangement, Guest_pr, Ratecode, Pricecod, Htparam, Katpreis, Queasy

p_list_data, P_list = create_model("P_list", {"betrag":Decimal, "date1":date, "date2":date, "argt":string, "pax":int, "rcode":string})

def chk_btn_go_res_rmratebl(pvilanguage:int, curr_select:string, max_rate:Decimal, fact1:Decimal, inp_wahrnr:int, inp_zikatnr:int, user_init:string, resnr:int, reslinnr:int, recid_reslin:int, contcode:string, p_list_data:[P_list]):

    prepare_cache ([Reslin_queasy, Waehrung, Res_line, Bediener, Arrangement, Guest_pr, Htparam, Katpreis, Queasy])

    msg_str = ""
    error_found1 = False
    error_code = 0
    t_reslin_queasy_data = []
    lvcarea:string = "chk-btn-go-res-rmrate"
    error_found:bool = False
    exrate2:Decimal = 1
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    reslin_queasy = waehrung = res_line = bediener = arrangement = guest_pr = ratecode = pricecod = htparam = katpreis = queasy = None

    t_reslin_queasy = p_list = brq = waehrung1 = breslin = None

    t_reslin_queasy_data, T_reslin_queasy = create_model("T_reslin_queasy", {"date1":date, "date2":date, "deci1":Decimal, "char1":string, "number3":int, "char2":string, "char3":string, "recid_reslin":int})

    Brq = create_buffer("Brq",Reslin_queasy)
    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Breslin = create_buffer("Breslin",Reslin_queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode
        nonlocal brq, waehrung1, breslin


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin
        nonlocal t_reslin_queasy_data

        return {"msg_str": msg_str, "error_found1": error_found1, "error_code": error_code, "t-reslin-queasy": t_reslin_queasy_data}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode
        nonlocal brq, waehrung1, breslin


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin
        nonlocal t_reslin_queasy_data

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def check_rate():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode
        nonlocal brq, waehrung1, breslin


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin
        nonlocal t_reslin_queasy_data

        error_found = False
        i:int = 0
        n:int = 0
        val:Decimal = to_decimal("0.0")
        max_disc:Decimal = to_decimal("0.0")
        tol_value:Decimal = to_decimal("0.0")
        rack_rate:Decimal = to_decimal("0.0")
        datum:date = None
        exrate1:Decimal = 1

        def generate_inner_output():
            return (error_found)


        if bediener.char1 == "":

            return generate_inner_output()

        if max_rate != 0 and p_list.betrag * fact1 > max_rate:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Room rate incorrect / too large! Check currency.", lvcarea, "")
            error_found = True

            return generate_inner_output()

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        if guest_pr:

            ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)]})

            if ratecode:

                return generate_inner_output()

            pricecod = get_cache (Pricecod, {"code": [(eq, guest_pr.code)]})

            if pricecod:

                return generate_inner_output()
        n = num_entries(bediener.char1, ";")
        for i in range(1,n + 1) :
            val =  to_decimal(to_int(entry(i) - to_decimal(1 , bediener.char1 , ";"))) / to_decimal("100")

            if max_disc < val:
                max_disc =  to_decimal(val)
        max_disc =  to_decimal(max_disc) / to_decimal("100")

        if max_disc == 0:

            return generate_inner_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exrate1 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, inp_wahrnr)]})

        if waehrung:
            exrate2 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        for datum in date_range(p_list.date1,p_list.date2) :
            rack_rate =  to_decimal("0")

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, inp_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

            if not katpreis:

                katpreis = get_cache (Katpreis, {"zikatnr": [(eq, inp_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})

            if katpreis:
                rack_rate =  to_decimal(get_rackrate (res_line.erwachs , res_line.kind1 , res_line.kind2))
            rack_rate =  to_decimal(rack_rate) * to_decimal(exrate1) / to_decimal(exrate2)

            if truncate(rack_rate, 0) != rack_rate:
                rack_rate = to_decimal(round(rack_rate + 0.5 , 0))

            if rack_rate * (1 - max_disc) > p_list.betrag:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Over discounted rate)", lvcarea, "") + " " + translateExtended ("for date =", lvcarea, "") + " " + to_string(datum)
                error_found = True

                return generate_inner_output()

        return generate_inner_output()


    def check_currency():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode
        nonlocal brq, waehrung1, breslin


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin
        nonlocal t_reslin_queasy_data

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        if not reslin_queasy:

            if not guest_pr:

                return

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

            if queasy and queasy.number1 != 0:

                waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:
                    pass
                    res_line.betriebsnr = waehrung1.waehrungsnr
                    pass
                    msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("No AdHoc Rates found; set back the currency code", lvcarea, "") + chr_unicode(10) + translateExtended ("to", lvcarea, "") + " " + waehrung1.bezeich + " " + translateExtended ("as defined in the contract rates.", lvcarea, "")


    def res_changes_add():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode
        nonlocal brq, waehrung1, breslin


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin
        nonlocal t_reslin_queasy_data

        cid:string = ""
        cdate:string = " "
        rqy = None
        Rqy =  create_buffer("Rqy",Reslin_queasy)

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("ADD Fixrate:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        pass
        pass


    def res_changes_chg():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_data, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal pvilanguage, curr_select, max_rate, fact1, inp_wahrnr, inp_zikatnr, user_init, resnr, reslinnr, recid_reslin, contcode
        nonlocal brq, waehrung1, breslin


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin
        nonlocal t_reslin_queasy_data

        cid:string = ""
        cdate:string = " "
        rqy = None
        Rqy =  create_buffer("Rqy",Reslin_queasy)

        if not res_line:

            return

        if res_line.active_flag == 2 and res_line.resstatus != 12:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate FR:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        pass
        pass
        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate TO:") + ";" + to_string(p_list.date1) + "-" + to_string(p_list.betrag) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        pass
        pass

    p_list = query(p_list_data, first=True)

    # res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    res_line = db_session.query(Res_line).filter(Res_line.resnr == resnr, Res_line.reslinnr == reslinnr).with_for_update().first()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    reslin_queasy = get_cache (Reslin_queasy, {"_recid": [(eq, recid_reslin)]})

    if p_list.argt != "":

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, p_list.argt)]})

        if not arrangement:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Arrangement Code incorrect.", lvcarea, "")
            error_code = 1

            return generate_output()

    if curr_select.lower()  == ("add").lower() :

        brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"date1": [(ge, p_list.date1),(le, p_list.date2)]})

        if not brq:

            brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"date2": [(ge, p_list.date1),(le, p_list.date2)]})

        if not brq:

            brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"date1": [(le, p_list.date1)],"date2": [(ge, p_list.date1)]})

        if not brq:

            brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"date1": [(le, p_list.date2)],"date2": [(ge, p_list.date2)]})

        if brq:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Overlapping date found.", lvcarea, "")

            return generate_output()
        error_found = check_rate()

        if error_found:
            error_found1 = error_found

            return generate_output()

        if res_line.active_flag == 0:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fixrate-trace-record")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

            if not reslin_queasy:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "fixrate-trace-record"
                reslin_queasy.resnr = resnr
                reslin_queasy.reslinnr = reslinnr
                reslin_queasy.date1 = get_current_date()
                reslin_queasy.number1 = get_current_time_in_seconds()
                reslin_queasy.char3 = ""


                pass
                pass
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "arrangement"
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.date1 = p_list.date1
        reslin_queasy.date2 = p_list.date2
        reslin_queasy.deci1 =  to_decimal(p_list.betrag)
        reslin_queasy.char1 = p_list.argt
        reslin_queasy.char2 = p_list.rcode
        reslin_queasy.char3 = user_init
        reslin_queasy.number3 = p_list.pax
        reslin_queasy.number2 = get_current_time_in_seconds()
        reslin_queasy.date3 = get_current_date()


        pass
        t_reslin_queasy = T_reslin_queasy()
        t_reslin_queasy_data.append(t_reslin_queasy)

        buffer_copy(reslin_queasy, t_reslin_queasy)
        t_reslin_queasy.recid_reslin = reslin_queasy._recid

        res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})
        res_changes_add()

    elif curr_select.lower()  == ("chg").lower() :

        brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"_recid": [(ne, reslin_queasy._recid)],"date1": [(ge, p_list.date1),(le, p_list.date2)]})

        if not brq:

            brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"_recid": [(ne, reslin_queasy._recid)],"reslinnr": [(eq, reslinnr)],"date2": [(ge, p_list.date1),(le, p_list.date2)]})

        if not brq:

            brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"_recid": [(ne, reslin_queasy._recid)],"date1": [(le, p_list.date1)],"date2": [(ge, p_list.date1)]})

        if not brq:

            brq = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"_recid": [(ne, reslin_queasy._recid)],"date1": [(le, p_list.date2)],"date2": [(ge, p_list.date2)]})

        if brq:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Overlapping date found.", lvcarea, "")

            return generate_output()

        if res_line.active_flag == 0:

            breslin = get_cache (Reslin_queasy, {"key": [(eq, "fixrate-trace-record")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

            if not breslin:
                breslin = Reslin_queasy()
                db_session.add(breslin)

                breslin.key = "fixrate-trace-record"
                breslin.resnr = resnr
                breslin.reslinnr = reslinnr
                breslin.date1 = get_current_date()
                breslin.number1 = get_current_time_in_seconds()
                breslin.char3 = ""


                pass
                pass

        res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})
        res_changes_chg()
        pass
        reslin_queasy.key = "arrangement"
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.date1 = p_list.date1
        reslin_queasy.date2 = p_list.date2
        reslin_queasy.deci1 =  to_decimal(p_list.betrag)
        reslin_queasy.char1 = p_list.argt
        reslin_queasy.char2 = p_list.rcode
        reslin_queasy.char3 = user_init
        reslin_queasy.number3 = p_list.pax
        reslin_queasy.number2 = get_current_time_in_seconds()
        reslin_queasy.date3 = get_current_date()


        pass
        t_reslin_queasy = T_reslin_queasy()
        t_reslin_queasy_data.append(t_reslin_queasy)

        buffer_copy(reslin_queasy, t_reslin_queasy)
        t_reslin_queasy.recid_reslin = recid_reslin


    else:
        check_currency()

    return generate_output()