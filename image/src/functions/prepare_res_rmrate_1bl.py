from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.ratecode_rate import ratecode_rate
from models import Res_line, Waehrung, Htparam, Bediener, Arrangement, Guest, Guest_pr, Queasy, Reslin_queasy, Ratecode

def prepare_res_rmrate_1bl(pvilanguage:int, user_init:str, reslin_list:[Reslin_list]):
    rate_found = False
    ci_date = None
    output_list_list = []
    p_list_list = []
    curr_add_last_list = []
    t_waehrung_list = []
    q2_reslin_queasy_list = []
    ratecode_list_list = []
    rate_flag = False
    price_decimal:int = 0
    exchg_rate:decimal = 1
    ct:str = ""
    curr_wabnr:int = 0
    datum:date = None
    bill_date:date = None
    co_date:date = None
    ebdisc_flag:bool = False
    kbdisc_flag:bool = False
    early_flag:bool = False
    kback_flag:bool = False
    curr_zikatnr:int = 0
    rm_rate:decimal = 0
    lvcarea:str = "prepare_res_rmrate"
    found:bool = False
    curr_time:int = 0
    res_line = waehrung = htparam = bediener = arrangement = guest = guest_pr = queasy = reslin_queasy = ratecode = None

    dynarate_list = ratecode_list = output_list = t_waehrung = q2_reslin_queasy = curr_add_last = p_list = reslin_list = waehrung2 = waehrung1 = None

    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"rcode":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "s_recid":int, "rmtype":str})
    ratecode_list_list, Ratecode_list = create_model("Ratecode_list", {"rcode_str":str})
    output_list_list, Output_list = create_model("Output_list", {"foreign_rate":bool, "double_currency":bool, "curr_foreign":str, "local_nr":int, "msg_str":str, "foreign_nr":int, "max_rate":decimal, "long_digit":bool, "selected":bool, "contcode":str, "currency_add_first":str, "zimmer_wunsch":str, "btn_chgart":bool, "fact1":decimal, "betriebsnr":int, "zipreis":decimal, "adrflag":bool, "recid_resline":int})
    t_waehrung_list, T_waehrung = create_model("T_waehrung", {"wabkurz":str, "bezeich":str, "betriebsnr":int, "waehrungsnr":int, "exrate":decimal})
    q2_reslin_queasy_list, Q2_reslin_queasy = create_model("Q2_reslin_queasy", {"date1":date, "date2":date, "deci1":decimal, "char1":str, "number3":int, "char2":str, "char3":str, "recid_reslin":int})
    curr_add_last_list, Curr_add_last = create_model("Curr_add_last", {"bezeich":str})
    p_list_list, P_list = create_model("P_list", {"betrag":decimal, "date1":date, "date2":date, "argt":str, "pax":int, "rcode":str})
    reslin_list_list, Reslin_list = create_model_like(Res_line)

    Waehrung2 = Waehrung
    Waehrung1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_found, ci_date, output_list_list, p_list_list, curr_add_last_list, t_waehrung_list, q2_reslin_queasy_list, ratecode_list_list, rate_flag, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal waehrung2, waehrung1


        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_list, ratecode_list_list, output_list_list, t_waehrung_list, q2_reslin_queasy_list, curr_add_last_list, p_list_list, reslin_list_list
        return {"rate_found": rate_found, "ci_date": ci_date, "output-list": output_list_list, "p-list": p_list_list, "curr-add-last": curr_add_last_list, "t-waehrung": t_waehrung_list, "q2-reslin-queasy": q2_reslin_queasy_list, "ratecode-list": ratecode_list_list, "rate_flag": rate_flag}

    def fill_p_list():

        nonlocal rate_found, ci_date, output_list_list, p_list_list, curr_add_last_list, t_waehrung_list, q2_reslin_queasy_list, ratecode_list_list, rate_flag, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal waehrung2, waehrung1


        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_list, ratecode_list_list, output_list_list, t_waehrung_list, q2_reslin_queasy_list, curr_add_last_list, p_list_list, reslin_list_list

        if reslin_queasy:
            p_list.betrag = reslin_queasy.deci1
            p_list.date1 = reslin_queasy.date1
            p_list.date2 = reslin_queasy.date2
            p_list.argt = reslin_queasy.char1
            p_list.pax = reslin_queasy.number3
            p_list.rcode = reslin_queasy.char2

    def assign_it():

        nonlocal rate_found, ci_date, output_list_list, p_list_list, curr_add_last_list, t_waehrung_list, q2_reslin_queasy_list, ratecode_list_list, rate_flag, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal waehrung2, waehrung1


        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_list, ratecode_list_list, output_list_list, t_waehrung_list, q2_reslin_queasy_list, curr_add_last_list, p_list_list, reslin_list_list


        curr_add_last = Curr_add_last()
        curr_add_last_list.append(curr_add_last)

        curr_add_last.bezeich = waehrung1.bezeich

    def disp_query():

        nonlocal rate_found, ci_date, output_list_list, p_list_list, curr_add_last_list, t_waehrung_list, q2_reslin_queasy_list, ratecode_list_list, rate_flag, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal waehrung2, waehrung1


        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_list, ratecode_list_list, output_list_list, t_waehrung_list, q2_reslin_queasy_list, curr_add_last_list, p_list_list, reslin_list_list


        output_list.fact1 = waehrung1.ankauf / waehrung1.einheit

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr)).all():
            q2_reslin_queasy = Q2_reslin_queasy()
            q2_reslin_queasy_list.append(q2_reslin_queasy)

            q2_reslin_queasy.date1 = reslin_queasy.date1
            q2_reslin_queasy.date2 = reslin_queasy.date2
            q2_reslin_queasy.deci1 = reslin_queasy.deci1
            q2_reslin_queasy.char1 = reslin_queasy.char1
            q2_reslin_queasy.number3 = reslin_queasy.number3
            q2_reslin_queasy.char2 = reslin_queasy.char2
            q2_reslin_queasy.char3 = reslin_queasy.char3
            q2_reslin_queasy.recid_reslin = reslin_queasy._recid

    def create_dynarate_list():

        nonlocal rate_found, ci_date, output_list_list, p_list_list, curr_add_last_list, t_waehrung_list, q2_reslin_queasy_list, ratecode_list_list, rate_flag, price_decimal, exchg_rate, ct, curr_wabnr, datum, bill_date, co_date, ebdisc_flag, kbdisc_flag, early_flag, kback_flag, curr_zikatnr, rm_rate, lvcarea, found, curr_time, res_line, waehrung, htparam, bediener, arrangement, guest, guest_pr, queasy, reslin_queasy, ratecode
        nonlocal waehrung2, waehrung1


        nonlocal dynarate_list, ratecode_list, output_list, t_waehrung, q2_reslin_queasy, curr_add_last, p_list, reslin_list, waehrung2, waehrung1
        nonlocal dynarate_list_list, ratecode_list_list, output_list_list, t_waehrung_list, q2_reslin_queasy_list, curr_add_last_list, p_list_list, reslin_list_list

        i:int = 0
        tokcounter:int = 0
        iftask:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        occ_rooms:int = 0
        use_it:bool = False

        for ratecode in db_session.query(Ratecode).filter(
                (Ratecode.code == guest_pr.code)).all():
            dynarate_list = Dynarate_list()
            dynarate_list_list.append(dynarate_list)

            dynaRate_list.s_recid = ratecode._recid


            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "RT":
                    dynaRate_list.rmType = mesvalue
                elif mestoken == "FR":
                    dynaRate_list.fr_room = to_int(mesvalue)
                elif mestoken == "TR":
                    dynaRate_list.to_room = to_int(mesvalue)
                elif mestoken == "D1":
                    dynaRate_list.days1 = to_int(mesvalue)
                elif mestoken == "D2":
                    dynaRate_list.days2 = to_int(mesvalue)
                elif mestoken == "RC":
                    dynaRate_list.rCode = mesvalue


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    reslin_list = query(reslin_list_list, first=True)

    for waehrung in db_session.query(Waehrung).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        t_waehrung.wabkurz = waehrung.wabkurz
        t_waehrung.bezeich = waehrung.bezeich
        t_waehrung.betriebsnr = waehrung.betriebsnr
        t_waehrungsnr = waehrungsnr
        t_waehrung.exrate = waehrung.ankauf / waehrung.einheit


    output_list = Output_list()
    output_list_list.append(output_list)


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    arrangement = db_session.query(Arrangement).filter(
            (Arrangement == reslin_list.arrangement)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    output_list.foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    output_list.double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    output_list.curr_foreign = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        output_list.msg_str = output_list.msg_str + chr(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7).", lvcarea, "")

        return generate_output()
    output_list.local_nr = waehrungsnr

    if output_list.foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if not waehrung:
            output_list.msg_str = output_list.msg_str + chr(2) + translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7).", lvcarea, "")

            return generate_output()
        output_list.foreign_nr = waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1108)).first()

    if htparam.feldtyp == 1:

        htparam = db_session.query(Htparam).first()
        htparam.feldtyp = 2
        htparam.fdecimal = htparam.finteger
        htparam.finteger = 0

        htparam = db_session.query(Htparam).first()
    output_list.max_rate = htparam.fdecimal

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 494)).first()
    rate_flag = htparam.flogical

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == reslin_list.resnr) &  (Res_line.reslinnr == reslin_list.reslinnr)).first()
    output_list.betriebsnr = reslin_list.betriebsnr
    output_list.zipreis = reslin_list.zipreis
    output_list.adrflag = reslin_list.adrflag
    output_list.recid_resline = res_line._recid

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == reslin_list.gastnr)).first()

    if guest.notizen[2] != "":

        waehrung2 = db_session.query(Waehrung2).filter(
                (Waehrung2.wabkurz == guest.notizen[2])).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    output_list.long_digit = htparam.flogical

    if output_list.FOREIGN_RATE or output_list.DOUBLE_CURRENCY:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == reslin_list.gastnr)).first()

    if guest_pr:
        output_list.contcode = guest_pr.CODE
        ct = reslin_list.zimmer_wunsch

        if re.match(".*\$CODE\$.*",ct):
            ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
            output_list.contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)
    p_list = P_list()
    p_list_list.append(p_list)


    if arrangement:
        output_list.selected = True
        fill_p_list()
    ebdisc_flag = re.match(".*ebdisc.*",reslin_list.zimmer_wunsch)
    kbdisc_flag = re.match(".*kbdisc.*",reslin_list.zimmer_wunsch)

    if reslin_list.l_zuordnung[0] != 0:
        curr_zikatnr = reslin_list.l_zuordnung[0]
    else:
        curr_zikatnr = reslin_list.zikatnr
    co_date = reslin_list.abreise

    if co_date > reslin_list.ankunft:
        co_date = co_date - 1
    for datum in range(reslin_list.ankunft,co_date + 1) :
        bill_date = datum

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == reslin_list.gastnr)).first()

        if guest_pr:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 18) &  (Queasy.number1 == reslin_list.reserve_int)).first()

            if queasy and queasy.logi3:
                bill_date = reslin_list.ankunft
            rate_found, rm_rate, early_flag, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, guest_pr.CODE, None, bill_date, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

            if rate_found :
                break

    if reslin_list.resstatus == 8:
        1

    elif reslin_list.reserve_char != "" and substring(bediener.permission, 42, 1) < "2":
        output_list.btn_chgart = True
    else:
        output_list.btn_chgart = False

    output_list = query(output_list_list, first=True)

    if reslin_list.betriebsnr != 0:

        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != reslin_list.betriebsnr) &  (Waehrung1.betriebsnr == 0)).all():
            assign_it()

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr == reslin_list.betriebsnr)).first()

    elif waehrung2:
        curr_wabnr = waehrung2.waehrungsnr

        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != curr_wabnr) &  (Waehrung1.betriebsnr == 0)).all():
            assign_it()

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr == curr_wabnr)).first()

    elif reslin_list.betriebsnr == 0 and not reslin_list.adrflag:

        if guest_pr:

            if reslin_list.reserve_int != 0:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 18) &  (Queasy.number1 == reslin_list.reserve_int)).first()

                if not queasy or (queasy and queasy.char3 == ""):

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 2) &  (Queasy.char1 == output_list.contcode)).first()
            else:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (Queasy.char1 == output_list.contcode)).first()

            if queasy:

                if queasy.key == 18:

                    waehrung1 = db_session.query(Waehrung1).filter(
                            (Waehrung1.wabkurz == queasy.char3)).first()
                else:

                    waehrung1 = db_session.query(Waehrung1).filter(
                            (Waehrung1.waehrungsnr == queasy.number1)).first()

                if waehrung1:
                    found = True
                    curr_wabnr = waehrung1.waehrungsnr

                    for waehrung1 in db_session.query(Waehrung1).filter(
                            (Waehrung1.waehrungsnr != curr_wabnr) &  (Waehrung1.betriebsnr == 0)).all():
                        assign_it()

                    waehrung1 = db_session.query(Waehrung1).filter(
                            (Waehrung1.waehrungsnr == curr_wabnr)).first()

        if not found:

            if output_list.foreign_rate:

                for waehrung1 in db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr != output_list.foreign_nr) &  (Waehrung1.betriebsnr == 0)).all():
                    assign_it()

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr == output_list.foreign_nr)).first()
            else:

                for waehrung1 in db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr != output_list.local_nr) &  (Waehrung1.betriebsnr == 0)).all():
                    assign_it()

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr == output_list.local_nr)).first()

    elif reslin_list.betriebsnr == 0 and reslin_list.adrflag:

        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != output_list.local_nr) &  (Waehrung1.betriebsnr == 0)).all():
            assign_it()

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr == output_list.local_nr)).first()
    output_list.currency_add_first = waehrung1.bezeich
    disp_query()
    output_list.zimmer_wunsch = reslin_list.zimmer_wunsch
    curr_time = get_current_time_in_seconds()

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == reslin_list.gastnr)).first()
    while None != guest_pr:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == guest_pr.CODE)).first()

        if queasy:

            if not queasy.logi2:

                ratecode_list = query(ratecode_list_list, filters=(lambda ratecode_list :ratecode_list.rcode_str == guest_pr.CODE), first=True)

                if not ratecode_list:
                    ratecode_list = Ratecode_list()
                    ratecode_list_list.append(ratecode_list)

                    ratecode_list.rcode_str = guest_pr.CODE


            else:
                dynaRate_list_list.clear()
                create_dynarate_list()

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == reslin_list.gastnr)).first()
    curr_time = get_current_time_in_seconds() - curr_time

    for dynarate_list in query(dynarate_list_list):

        ratecode_list = query(ratecode_list_list, filters=(lambda ratecode_list :ratecode_list.rcode_str == dynaRate_list.rcode), first=True)

        if not ratecode_list:
            ratecode_list = Ratecode_list()
            ratecode_list_list.append(ratecode_list)

            ratecode_list.rcode_str = dynaRate_list.rcode

    return generate_output()