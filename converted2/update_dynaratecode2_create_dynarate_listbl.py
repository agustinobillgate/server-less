#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Ratecode, Queasy, Prmarket

def update_dynaratecode2_create_dynarate_listbl(prcode:string):

    prepare_cache ([Ratecode, Queasy, Prmarket])

    currency = ""
    market = ""
    market_number = 0
    avail_queasy = False
    avail_prmarket = False
    dynarate_list_data = []
    iftask:string = ""
    tokcounter:int = 0
    mestoken:string = ""
    mesvalue:string = ""
    ratecode = queasy = prmarket = None

    dynarate_list = None

    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"counter":int, "rcode":string, "w_day":int, "fr_room":int, "to_room":int, "days1":int, "days2":int, "s_recid":int, "rmtype":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal currency, market, market_number, avail_queasy, avail_prmarket, dynarate_list_data, iftask, tokcounter, mestoken, mesvalue, ratecode, queasy, prmarket
        nonlocal prcode


        nonlocal dynarate_list
        nonlocal dynarate_list_data

        return {"currency": currency, "market": market, "market_number": market_number, "avail_queasy": avail_queasy, "avail_prmarket": avail_prmarket, "dynaRate-list": dynarate_list_data}

    for ratecode in db_session.query(Ratecode).filter(
             (Ratecode.code == (prcode).lower())).order_by(Ratecode._recid).all():
        dynarate_list = Dynarate_list()
        dynarate_list_data.append(dynarate_list)

        dynarate_list.s_recid = ratecode._recid


        iftask = ratecode.char1[4]
        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

            if mestoken == "CN":
                dynarate_list.counter = to_int(mesvalue)
            elif mestoken == "RT":
                dynarate_list.rmtype = mesvalue
            elif mestoken == "WD":
                dynarate_list.w_day = to_int(mesvalue)
            elif mestoken == "FR":
                dynarate_list.fr_room = to_int(mesvalue)
            elif mestoken == "TR":
                dynarate_list.to_room = to_int(mesvalue)
            elif mestoken == "D1":
                dynarate_list.days1 = to_int(mesvalue)
            elif mestoken == "D2":
                dynarate_list.days2 = to_int(mesvalue)
            elif mestoken == "RC":
                dynarate_list.rcode = mesvalue

    dynarate_list = query(dynarate_list_data, first=True)

    if dynarate_list:

        ratecode = get_cache (Ratecode, {"code": [(eq, dynarate_list.rcode)]})

        if ratecode:

            queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, ratecode.marknr)]})

            if queasy:
                avail_queasy = True
                currency = queasy.char3

            prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

            if prmarket:
                avail_prmarket = True
                market = prmarket.bezeich
                market_number = prmarket.nr

    return generate_output()