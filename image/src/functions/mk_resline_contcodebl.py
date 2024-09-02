from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Ratecode, Prmarket, Waehrung

def mk_resline_contcodebl(contcode:str):
    currency = ""
    currency_nr = 0
    t_queasy_list = []
    t_ratecode_list = []
    t_prmarket_list = []
    iftask:str = ""
    statcode:str = ""
    mestoken:str = ""
    mesvalue:str = ""
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


        nonlocal t_queasy, t_ratecode, t_prmarket
        nonlocal t_queasy_list, t_ratecode_list, t_prmarket_list
        return {"currency": currency, "currency_nr": currency_nr, "t-queasy": t_queasy_list, "t-ratecode": t_ratecode_list, "t-prmarket": t_prmarket_list}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (func.lower(Queasy.char1) == (contcode).lower())).first()

    if not queasy:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (substring(Queasy.char1, 0, len((contcode).lower() )) == (contcode).lower())).first()

    if queasy:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (contcode).lower())).first()

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

                ratecode = db_session.query(Ratecode).filter(
                        (func.lower(Ratecode.code) == (statcode).lower())).first()

        if ratecode:

            prmarket = db_session.query(Prmarket).filter(
                    (Prmarket.nr == ratecode.marknr)).first()

        if prmarket:
            t_prmarket = T_prmarket()
            t_prmarket_list.append(t_prmarket)

            buffer_copy(prmarket, t_prmarket)

            if dyna_flag:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 18) &  (Queasy.number1 == prmarket.nr)).first()

                if queasy:
                    currency = queasy.char3

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrung.wabkurz == currency)).first()

                    if waehrung:
                        currency_nr = waehrungsnr

    return generate_output()