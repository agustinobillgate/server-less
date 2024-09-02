from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Ratecode, Queasy, Prmarket

def update_dynaratecode2_create_dynarate_listbl(prcode:str):
    currency = ""
    market = ""
    market_number = 0
    avail_queasy = False
    avail_prmarket = False
    dynarate_list_list = []
    iftask:str = ""
    tokcounter:int = 0
    mestoken:str = ""
    mesvalue:str = ""
    ratecode = queasy = prmarket = None

    dynarate_list = None

    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "rcode":str, "w_day":int, "fr_room":int, "to_room":int, "days1":int, "days2":int, "s_recid":int, "rmtype":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal currency, market, market_number, avail_queasy, avail_prmarket, dynarate_list_list, iftask, tokcounter, mestoken, mesvalue, ratecode, queasy, prmarket


        nonlocal dynarate_list
        nonlocal dynarate_list_list
        return {"currency": currency, "market": market, "market_number": market_number, "avail_queasy": avail_queasy, "avail_prmarket": avail_prmarket, "dynaRate-list": dynarate_list_list}

    for ratecode in db_session.query(Ratecode).filter(
            (func.lower(Ratecode.code) == (prcode).lower())).all():
        dynarate_list = Dynarate_list()
        dynarate_list_list.append(dynarate_list)

        dynaRate_list.s_recid = ratecode._recid


        iftask = ratecode.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

            if mestoken == "CN":
                dynaRate_list.counter = to_int(mesvalue)
            elif mestoken == "RT":
                dynaRate_list.rmType = mesvalue
            elif mestoken == "WD":
                dynaRate_list.w_day = to_int(mesvalue)
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

    dynarate_list = query(dynarate_list_list, first=True)

    if dynaRate_list:

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode.CODE == dynaRate_list.rCode)).first()

        if ratecode:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 18) &  (Queasy.number1 == ratecode.marknr)).first()

            if queasy:
                avail_queasy = True
                currency = queasy.char3

            prmarket = db_session.query(Prmarket).filter(
                    (Prmarket.nr == ratecode.marknr)).first()

            if prmarket:
                avail_prmarket = True
                market = prmarket.bezeich
                market_number = prmarket.nr

    return generate_output()