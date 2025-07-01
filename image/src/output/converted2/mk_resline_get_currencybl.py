#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Res_line, Guest, Htparam, Queasy, Ratecode, Reslin_queasy, Guest_pr

def mk_resline_get_currencybl(reslin_list_betriebsnr:int, marknr:int, foreign_rate:bool, t_contcode:string, reslin_list_resnr:int, reslin_list_reslinnr:int, reslin_list_adrflag:bool, res_mode:string, gastnr:int, resnr:int, reslinnr:int):

    prepare_cache ([Res_line, Guest, Htparam, Queasy, Ratecode, Guest_pr])

    local_nr = 0
    foreign_nr = 0
    guest_currency = 0
    curr_wabnr = 0
    waehrung1_wabkurz = ""
    err_msg = 0
    return_flag = 0
    err_whr = 0
    t_waehrung1_list = []
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    rcode:string = ""
    found:bool = False
    waehrung = res_line = guest = htparam = queasy = ratecode = reslin_queasy = guest_pr = None

    t_waehrung1 = waehrung1 = rline = gbuff = None

    t_waehrung1_list, T_waehrung1 = create_model_like(Waehrung)

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Rline = create_buffer("Rline",Res_line)
    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, foreign_nr, guest_currency, curr_wabnr, waehrung1_wabkurz, err_msg, return_flag, err_whr, t_waehrung1_list, tokcounter, iftask, mestoken, mesvalue, rcode, found, waehrung, res_line, guest, htparam, queasy, ratecode, reslin_queasy, guest_pr
        nonlocal reslin_list_betriebsnr, marknr, foreign_rate, t_contcode, reslin_list_resnr, reslin_list_reslinnr, reslin_list_adrflag, res_mode, gastnr, resnr, reslinnr
        nonlocal waehrung1, rline, gbuff


        nonlocal t_waehrung1, waehrung1, rline, gbuff
        nonlocal t_waehrung1_list

        return {"reslin_list_betriebsnr": reslin_list_betriebsnr, "local_nr": local_nr, "foreign_nr": foreign_nr, "guest_currency": guest_currency, "curr_wabnr": curr_wabnr, "waehrung1_wabkurz": waehrung1_wabkurz, "err_msg": err_msg, "return_flag": return_flag, "err_whr": err_whr, "t-waehrung1": t_waehrung1_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung1 = db_session.query(Waehrung1).filter(
             (Waehrung1.wabkurz == htparam.fchar)).first()

    if not waehrung1:
        err_msg = 1

        return generate_output()
    local_nr = waehrung1.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung1 = db_session.query(Waehrung1).filter(
             (Waehrung1.wabkurz == htparam.fchar)).first()

    if (not waehrung1) and foreign_rate:
        err_msg = 2

        return generate_output()

    if waehrung1:
        foreign_nr = waehrung1.waehrungsnr

    gbuff = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if gbuff.notizen[2] != "":

        waehrung1 = db_session.query(Waehrung1).filter(
                 (Waehrung1.wabkurz == gbuff.notizen[2])).first()

        if waehrung1:
            guest_currency = waehrung1.waehrungsnr

    if t_contcode != "":

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, t_contcode)]})

        if queasy and queasy.logi2:

            ratecode = get_cache (Ratecode, {"code": [(eq, t_contcode)]})
            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "RC":
                    rcode = mesvalue

            if rcode != "":

                ratecode = get_cache (Ratecode, {"code": [(eq, rcode)]})

                queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, ratecode.marknr)]})

                if queasy:

                    waehrung1 = db_session.query(Waehrung1).filter(
                             (Waehrung1.wabkurz == queasy.char3)).first()

                    if waehrung1:
                        waehrung1_wabkurz = waehrung1.wabkurz
                        curr_wabnr = waehrung1.waehrungsnr


                    return_flag = 1

                    return generate_output()

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list_resnr)],"reslinnr": [(eq, reslin_list_reslinnr)]})

    if reslin_queasy:

        for waehrung1 in db_session.query(Waehrung1).filter(
                 (Waehrung1.waehrungsnr != reslin_list_betriebsnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
            t_waehrung1 = T_waehrung1()
            t_waehrung1_list.append(t_waehrung1)

            buffer_copy(waehrung1, t_waehrung1)

        waehrung1 = db_session.query(Waehrung1).filter(
                 (Waehrung1.waehrungsnr == reslin_list_betriebsnr)).first()

        if waehrung1:
            waehrung1_wabkurz = waehrung1.wabkurz
        return_flag = 2

        return generate_output()

    if reslin_list_betriebsnr == 0 or marknr != 0:

        if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()  or marknr != 0):
            pass

            if t_contcode != "":

                guest_pr = get_cache (Guest_pr, {"code": [(eq, t_contcode)]})

            if not guest_pr:

                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr)]})

            if guest_pr:

                if marknr != 0:

                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, marknr)]})

                    if not queasy or (queasy and queasy.char3 == ""):

                        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})
                else:

                    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

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

                        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

                        if rline:
                            rline.betriebsnr = waehrung1.waehrungsnr
                            pass
                            reslin_list_betriebsnr = rline.betriebsnr

        if not found:

            if reslin_list_adrflag  or not foreign_rate:
                curr_wabnr = local_nr
                reslin_list_betriebsnr = local_nr

                waehrung1 = db_session.query(Waehrung1).filter(
                         (Waehrung1.waehrungsnr == local_nr)).first()
            else:

                if guest_currency != 0:
                    curr_wabnr = guest_currency
                else:
                    curr_wabnr = foreign_nr
                reslin_list_betriebsnr = curr_wabnr

            for waehrung1 in db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr != curr_wabnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                t_waehrung1 = T_waehrung1()
                t_waehrung1_list.append(t_waehrung1)

                buffer_copy(waehrung1, t_waehrung1)

            waehrung1 = db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr == curr_wabnr)).first()
            err_whr = 1
    else:

        for waehrung1 in db_session.query(Waehrung1).filter(
                 (Waehrung1.waehrungsnr != reslin_list_betriebsnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
            t_waehrung1 = T_waehrung1()
            t_waehrung1_list.append(t_waehrung1)

            buffer_copy(waehrung1, t_waehrung1)

        waehrung1 = db_session.query(Waehrung1).filter(
                 (Waehrung1.waehrungsnr == reslin_list_betriebsnr)).first()
        err_whr = 2
    waehrung1_wabkurz = waehrung1.wabkurz

    return generate_output()