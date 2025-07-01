#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Ratecode, Prmarket, Waehrung

def mk_resline_contcodebl(contcode:string):

    prepare_cache ([Waehrung])

    currency = ""
    currency_nr = 0
    t_queasy_list = []
    t_ratecode_list = []
    t_prmarket_list = []
    iftask:string = ""
    statcode:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    tokcounter:int = 0
    dyna_flag:bool = False
    queasy = ratecode = prmarket = waehrung = None

    t_queasy = t_ratecode = t_prmarket = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_ratecode_list, T_ratecode = create_model_like(Ratecode)
    t_prmarket_list, T_prmarket = create_model_like(Prmarket)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal currency, currency_nr, t_queasy_list, t_ratecode_list, t_prmarket_list, iftask, statcode, mestoken, mesvalue, tokcounter, dyna_flag, queasy, ratecode, prmarket, waehrung
        nonlocal contcode


        nonlocal t_queasy, t_ratecode, t_prmarket
        nonlocal t_queasy_list, t_ratecode_list, t_prmarket_list

        return {"currency": currency, "currency_nr": currency_nr, "t-queasy": t_queasy_list, "t-ratecode": t_ratecode_list, "t-prmarket": t_prmarket_list}

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, contcode)]})

    if not queasy:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (substring(Queasy.char1, 0, length((contcode).lower() )) == (contcode).lower())).first()

    if queasy:

        ratecode = get_cache (Ratecode, {"code": [(eq, contcode)]})

        if ratecode:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)
            t_ratecode = T_ratecode()
            t_ratecode_list.append(t_ratecode)

            buffer_copy(ratecode, t_ratecode)

            if queasy.logi2:
                dyna_flag = True
                iftask = ratecode.char1[4]


                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "RC":
                        statcode = mesvalue

                if statcode != "":

                    ratecode = get_cache (Ratecode, {"code": [(eq, statcode)]})

            if ratecode:

                prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

            if prmarket:
                t_prmarket = T_prmarket()
                t_prmarket_list.append(t_prmarket)

                buffer_copy(prmarket, t_prmarket)

                if dyna_flag:

                    queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, prmarket.nr)]})

                    if queasy:
                        currency = queasy.char3

                        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency)]})

                        if waehrung:
                            currency_nr = waehrung.waehrungsnr

    return generate_output()