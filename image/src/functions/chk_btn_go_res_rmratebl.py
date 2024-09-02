from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Reslin_queasy, Waehrung, Res_line, Bediener, Arrangement, Guest_pr, Ratecode, Pricecod, Htparam, Katpreis, Queasy

def chk_btn_go_res_rmratebl(pvilanguage:int, curr_select:str, max_rate:decimal, fact1:decimal, inp_wahrnr:int, inp_zikatnr:int, user_init:str, resnr:int, reslinnr:int, recid_reslin:int, contcode:str, p_list:[P_list]):
    msg_str = ""
    error_found1 = False
    error_code = 0
    t_reslin_queasy_list = []
    lvcarea:str = "chk_btn_go_res_rmrate"
    error_found:bool = False
    exrate2:decimal = 1
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    reslin_queasy = waehrung = res_line = bediener = arrangement = guest_pr = ratecode = pricecod = htparam = katpreis = queasy = None

    t_reslin_queasy = p_list = brq = waehrung1 = breslin = rqy = None

    t_reslin_queasy_list, T_reslin_queasy = create_model("T_reslin_queasy", {"date1":date, "date2":date, "deci1":decimal, "char1":str, "number3":int, "char2":str, "char3":str, "recid_reslin":int})
    p_list_list, P_list = create_model("P_list", {"betrag":decimal, "date1":date, "date2":date, "argt":str, "pax":int, "rcode":str})

    Brq = Reslin_queasy
    Waehrung1 = Waehrung
    Breslin = Reslin_queasy
    Rqy = Reslin_queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_list, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal brq, waehrung1, breslin, rqy


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin, rqy
        nonlocal t_reslin_queasy_list, p_list_list
        return {"msg_str": msg_str, "error_found1": error_found1, "error_code": error_code, "t-reslin-queasy": t_reslin_queasy_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_list, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal brq, waehrung1, breslin, rqy


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin, rqy
        nonlocal t_reslin_queasy_list, p_list_list

        rate:decimal = 0

        if erwachs >= 1 and erwachs <= 4:
            rate = rate + katpreis.perspreis[erwachs - 1]
        rate = rate + kind1 * katpreis.kindpreis[0] + kind2 * katpreis.kindpreis[1]
        return rate

    def check_rate():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_list, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal brq, waehrung1, breslin, rqy


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin, rqy
        nonlocal t_reslin_queasy_list, p_list_list

        error_found = False
        i:int = 0
        n:int = 0
        val:decimal = 0
        max_disc:decimal = 0
        tol_value:decimal = 0
        rack_rate:decimal = 0
        datum:date = None
        exrate1:decimal = 1

        def generate_inner_output():
            return error_found

        if bediener.char1 == "":

            return generate_inner_output()

        if max_rate != 0 and p_list.betrag * fact1 > max_rate:
            msg_str = msg_str + chr(2) + translateExtended ("Room rate incorrect / too large! Check currency.", lvcarea, "")
            error_found = True

            return generate_inner_output()

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == res_line.gastnr)).first()

        if guest_pr:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == guest_pr.CODE)).first()

            if ratecode:

                return generate_inner_output()

            pricecod = db_session.query(Pricecod).filter(
                    (Pricecod.CODE == guest_pr.CODE)).first()

            if pricecod:

                return generate_inner_output()
        n = num_entries(bediener.char1, ";")
        for i in range(1,n + 1) :
            val = to_int(entry(i - 1, bediener.char1, ";")) / 100

            if max_disc < val:
                max_disc = val
        max_disc = max_disc / 100

        if max_disc == 0:

            return generate_inner_output()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exrate1 = waehrung.ankauf / waehrung.einheit

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == inp_wahrnr)).first()

        if waehrung:
            exrate2 = waehrung.ankauf / waehrung.einheit
        for datum in range(p_list.date1,p_list.date2 + 1) :
            rack_rate = 0

            katpreis = db_session.query(Katpreis).filter(
                    (Katpreis.zikatnr == inp_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

            if not katpreis:

                katpreis = db_session.query(Katpreis).filter(
                        (Katpreis.zikatnr == inp_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == 0)).first()

            if katpreis:
                rack_rate = get_rackrate (res_line.erwachs, res_line.kind1, res_line.kind2)
            rack_rate = rack_rate * exrate1 / exrate2

            if truncate(rack_rate, 0) != rack_rate:
                rack_rate = round(rack_rate + 0.5, 0)

            if rack_rate * (1 - max_disc) > p_list.betrag:
                msg_str = msg_str + chr(2) + translateExtended ("Over discounted rate)", lvcarea, "") + " " + translateExtended ("for date  == ", lvcarea, "") + " " + to_string(datum)
                error_found = True

                return generate_inner_output()


        return generate_inner_output()

    def check_currency():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_list, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal brq, waehrung1, breslin, rqy


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin, rqy
        nonlocal t_reslin_queasy_list, p_list_list

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr)).first()

        if not reslin_queasy:

            if not guest_pr:

                return

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (func.lower(Queasy.char1) == (contcode).lower())).first()

            if queasy and queasy.number1 != 0:

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr == queasy.number1)).first()

                if waehrung1 and waehrung1.waehrungsnr != res_line.betriebsnr:

                    res_line = db_session.query(Res_line).first()
                    res_line.betriebsnr = waehrung1.waehrungsnr

                    res_line = db_session.query(Res_line).first()
                    msg_str = msg_str + chr(2) + "&W" + translateExtended ("No AdHoc Rates found; set back the currency code", lvcarea, "") + chr(10) + translateExtended ("to", lvcarea, "") + " " + waehrung1.bezeich + " " + translateExtended ("as defined in the contract rates.", lvcarea, "")

    def res_changes_add():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_list, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal brq, waehrung1, breslin, rqy


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin, rqy
        nonlocal t_reslin_queasy_list, p_list_list

        cid:str = ""
        cdate:str = ""
        Rqy = Reslin_queasy

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Rqy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("ADD Fixrate:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

        rqy = db_session.query(Rqy).first()


    def res_changes_chg():

        nonlocal msg_str, error_found1, error_code, t_reslin_queasy_list, lvcarea, error_found, exrate2, wd_array, reslin_queasy, waehrung, res_line, bediener, arrangement, guest_pr, ratecode, pricecod, htparam, katpreis, queasy
        nonlocal brq, waehrung1, breslin, rqy


        nonlocal t_reslin_queasy, p_list, brq, waehrung1, breslin, rqy
        nonlocal t_reslin_queasy_list, p_list_list

        cid:str = ""
        cdate:str = ""
        Rqy = Reslin_queasy

        if not res_line:

            return

        if res_line.active_flag == 2:

            return

        if res_line.changed != None:
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)


        rqy = Rqy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate FR:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

        rqy = db_session.query(Rqy).first()

        rqy = Rqy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = res_line.resnr
        rqy.reslinnr = res_line.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate TO:") + ";" + to_string(p_list.date1) + "-" + to_string(p_list.betrag) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

        rqy = db_session.query(Rqy).first()

    p_list = query(p_list_list, first=True)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (Reslin_queasy._recid == recid_reslin)).first()

    if p_list.argt != "":

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == p_list.argt)).first()

        if not arrangement:
            msg_str = msg_str + chr(2) + translateExtended ("Arrangement Code incorrect.", lvcarea, "")
            error_code = 1

            return generate_output()

    if curr_select.lower()  == "add":

        brq = db_session.query(Brq).filter(
                (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (bRQ.date1 >= p_list.date1) &  (bRQ.date1 <= p_list.date2)).first()

        if not bRQ:

            brq = db_session.query(Brq).filter(
                    (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (bRQ.date2 >= p_list.date1) &  (bRQ.date2 <= p_list.date2)).first()

        if not bRQ:

            brq = db_session.query(Brq).filter(
                    (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (p_list.date1 >= bRQ.date1) &  (p_list.date1 <= bRQ.date2)).first()

        if not bRQ:

            brq = db_session.query(Brq).filter(
                    (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (p_list.date2 >= bRQ.date1) &  (p_list.date2 <= bRQ.date2)).first()

        if brQ:
            msg_str = msg_str + chr(2) + translateExtended ("Overlapping date found.", lvcarea, "")

            return generate_output()
        error_found = check_rate()

        if error_found:
            error_found1 = error_found

            return generate_output()

        if res_line.active_flag == 0:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "fixrate_trace_record") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr)).first()

            if not reslin_queasy:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "fixrate_trace_record"
                reslin_queasy.resnr = resnr
                reslin_queasy.reslinnr = reslinnr
                reslin_queasy.date1 = get_current_date()
                reslin_queasy.number1 = get_current_time_in_seconds()
                reslin_queasy.char3 = ""

                reslin_queasy = db_session.query(Reslin_queasy).first()

        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "arrangement"
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.date1 = p_list.date1
        reslin_queasy.date2 = p_list.date2
        reslin_queasy.deci1 = p_list.betrag
        reslin_queasy.char1 = p_list.argt
        reslin_queasy.char2 = p_list.rcode
        reslin_queasy.char3 = user_init
        reslin_queasy.number3 = p_list.pax
        reslin_queasy.number2 = get_current_time_in_seconds()
        reslin_queasy.date3 = get_current_date()

        reslin_queasy = db_session.query(Reslin_queasy).first()
        t_reslin_queasy = T_reslin_queasy()
        t_reslin_queasy_list.append(t_reslin_queasy)

        buffer_copy(reslin_queasy, t_reslin_queasy)
        t_reslin_queasy.recid_reslin = reslin_queasy._recid

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == reslin_queasy.resnr) &  (Res_line.reslinnr == reslin_queasy.reslinnr)).first()
        res_changes_add()

    elif curr_select.lower()  == "chg":

        brq = db_session.query(Brq).filter(
                (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (brQ._recid != reslin_queasy._recid) &  (bRQ.date1 >= p_list.date1) &  (bRQ.date1 <= p_list.date2)).first()

        if not bRQ:

            brq = db_session.query(Brq).filter(
                    (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (brQ._recid != reslin_queasy._recid) &  (bRQ.reslinnr == reslinnr) &  (bRQ.date2 >= p_list.date1) &  (bRQ.date2 <= p_list.date2)).first()

        if not bRQ:

            brq = db_session.query(Brq).filter(
                    (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (brQ._recid != reslin_queasy._recid) &  (p_list.date1 >= bRQ.date1) &  (p_list.date1 <= bRQ.date2)).first()

        if not bRQ:

            brq = db_session.query(Brq).filter(
                    (func.lower(Brq.key) == "arrangement") &  (bRQ.resnr == resnr) &  (bRQ.reslinnr == reslinnr) &  (brQ._recid != reslin_queasy._recid) &  (p_list.date2 >= bRQ.date1) &  (p_list.date2 <= bRQ.date2)).first()

        if brQ:
            msg_str = msg_str + chr(2) + translateExtended ("Overlapping date found.", lvcarea, "")

            return generate_output()

        if res_line.active_flag == 0:

            breslin = db_session.query(Breslin).filter(
                    (func.lower(Breslin.key) == "fixrate_trace_record") &  (Breslin.resnr == resnr) &  (Breslin.reslinnr == reslinnr)).first()

            if not breslin:
                breslin = Breslin()
                db_session.add(breslin)

                breslin.key = "fixrate_trace_record"
                breslin.resnr = resnr
                breslin.reslinnr = reslinnr
                breslin.date1 = get_current_date()
                breslin.number1 = get_current_time_in_seconds()
                breslin.char3 = ""

                breslin = db_session.query(Breslin).first()


        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == reslin_queasy.resnr) &  (Res_line.reslinnr == reslin_queasy.reslinnr)).first()
        res_changes_chg()

        reslin_queasy = db_session.query(Reslin_queasy).first()
        reslin_queasy.key = "arrangement"
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.date1 = p_list.date1
        reslin_queasy.date2 = p_list.date2
        reslin_queasy.deci1 = p_list.betrag
        reslin_queasy.char1 = p_list.argt
        reslin_queasy.char2 = p_list.rcode
        reslin_queasy.char3 = user_init
        reslin_queasy.number3 = p_list.pax
        reslin_queasy.number2 = get_current_time_in_seconds()
        reslin_queasy.date3 = get_current_date()

        reslin_queasy = db_session.query(Reslin_queasy).first()
        t_reslin_queasy = T_reslin_queasy()
        t_reslin_queasy_list.append(t_reslin_queasy)

        buffer_copy(reslin_queasy, t_reslin_queasy)
        t_reslin_queasy.recid_reslin = recid_reslin


    else:
        check_currency()

    return generate_output()