from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Waehrung, Res_line, Guest, Htparam, Queasy, Ratecode, Reslin_queasy, Guest_pr

def mk_resline_get_currencybl(reslin_list_betriebsnr:int, marknr:int, foreign_rate:bool, t_contcode:str, reslin_list_resnr:int, reslin_list_reslinnr:int, reslin_list_adrflag:bool, res_mode:str, gastnr:int, resnr:int, reslinnr:int):
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
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    rcode:str = ""
    found:bool = False
    waehrung = res_line = guest = htparam = queasy = ratecode = reslin_queasy = guest_pr = None

    t_waehrung1 = waehrung1 = rline = gbuff = None

    t_waehrung1_list, T_waehrung1 = create_model_like(Waehrung)

    Waehrung1 = Waehrung
    Rline = Res_line
    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, foreign_nr, guest_currency, curr_wabnr, waehrung1_wabkurz, err_msg, return_flag, err_whr, t_waehrung1_list, tokcounter, iftask, mestoken, mesvalue, rcode, found, waehrung, res_line, guest, htparam, queasy, ratecode, reslin_queasy, guest_pr
        nonlocal waehrung1, rline, gbuff


        nonlocal t_waehrung1, waehrung1, rline, gbuff
        nonlocal t_waehrung1_list
        return {"local_nr": local_nr, "foreign_nr": foreign_nr, "guest_currency": guest_currency, "curr_wabnr": curr_wabnr, "waehrung1_wabkurz": waehrung1_wabkurz, "err_msg": err_msg, "return_flag": return_flag, "err_whr": err_whr, "t-waehrung1": t_waehrung1_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung1 = db_session.query(Waehrung1).filter(
            (Waehrung1.wabkurz == htparam.fchar)).first()

    if not waehrung1:
        err_msg = 1

        return generate_output()
    local_nr = waehrung1.waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung1 = db_session.query(Waehrung1).filter(
            (Waehrung1.wabkurz == htparam.fchar)).first()

    if (not waehrung1) and foreign_rate:
        err_msg = 2

        return generate_output()

    if waehrung1:
        foreign_nr = waehrung1.waehrungsnr

    gbuff = db_session.query(Gbuff).filter(
            (Gbuff.gastnr == gastnr)).first()

    if gbuff.notizen[2] != "":

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.wabkurz == gbuff.notizen[2])).first()

        if waehrung1:
            guest_currency = waehrung1.waehrungsnr

    if t_contcode != "":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (func.lower(Queasy.char1) == (t_contcode).lower())).first()

        if queasy and queasy.logi2:

            ratecode = db_session.query(Ratecode).filter(
                    (func.lower(Ratecode.code) == (t_contcode).lower())).first()
            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "RC":
                    rcode = mesvalue

        if rcode != "":

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == rcode)).first()

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 18) &  (Queasy.number1 == ratecode.marknr)).first()

            if queasy:

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.wabkurz == queasy.char3)).first()

                if waehrung1:
                    waehrung1_wabkurz = waehrung1.wabkurz
                    curr_wabnr = waehrung1.waehrungsnr


                return_flag = 1

                return generate_output()

    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list_resnr) &  (Reslin_queasy.reslinnr == reslin_list_reslinnr)).first()

    if reslin_queasy:

        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != reslin_list_betriebsnr) &  (Waehrung1.betriebsnr == 0)).all():
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

        if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci" or marknr != 0):


            if t_contcode != "":

                guest_pr = db_session.query(Guest_pr).filter(
                        (func.lower(Guest_pr.code) == (t_contcode).lower())).first()

            if not guest_pr:

                guest_pr = db_session.query(Guest_pr).filter(
                        (Guest_pr.gastnr == gastnr)).first()

            if guest_pr:

                if marknr != 0:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 18) &  (Queasy.number1 == marknr)).first()

                    if not queasy or (queasy and queasy.char3 == ""):

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()
                else:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()

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

                        rline = db_session.query(Rline).filter(
                                (Rline.resnr == resnr) &  (Rline.reslinnr == reslinnr)).first()

                        if rline:
                            rline.betriebsnr = waehrung1.waehrungsnr

                            rline = db_session.query(Rline).first()
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
                    (Waehrung1.waehrungsnr != curr_wabnr) &  (Waehrung1.betriebsnr == 0)).all():
                t_waehrung1 = T_waehrung1()
                t_waehrung1_list.append(t_waehrung1)

                buffer_copy(waehrung1, t_waehrung1)

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == curr_wabnr)).first()
            err_whr = 1
    else:

        for waehrung1 in db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr != reslin_list_betriebsnr) &  (Waehrung1.betriebsnr == 0)).all():
            t_waehrung1 = T_waehrung1()
            t_waehrung1_list.append(t_waehrung1)

            buffer_copy(waehrung1, t_waehrung1)

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.waehrungsnr == reslin_list_betriebsnr)).first()
        err_whr = 2
    waehrung1_wabkurz = waehrung1.wabkurz

    return generate_output()