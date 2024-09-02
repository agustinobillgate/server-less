from functions.additional_functions import *
import decimal
from datetime import date
from models import L_verbrauch

def stock_consumebl(s_artnr:int, from_date:date, to_date:date):
    qty = 0
    val = 0
    consume_list_list = []
    l_verbrauch = None

    consume_list = None

    consume_list_list, Consume_list = create_model("Consume_list", {"artnr":int, "datum":date, "anz_verbrau":decimal, "wert_verbrau":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal qty, val, consume_list_list, l_verbrauch


        nonlocal consume_list
        nonlocal consume_list_list
        return {"qty": qty, "val": val, "consume-list": consume_list_list}

    if from_date == None:

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                (L_verbrauch.artnr == s_artnr)).all():
            qty = qty + anz_verbrau
            val = val + wert_verbrau

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                (L_verbrauch.artnr == s_artnr)).all():
            consume_list = Consume_list()
            consume_list_list.append(consume_list)

            buffer_copy(l_verbrauch, consume_list)
    else:

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                (L_verbrauch.artnr == s_artnr) &  (L_verbrauch.datum >= from_date) &  (L_verbrauch.datum <= to_date)).all():
            qty = qty + anz_verbrau
            val = val + wert_verbrau

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                (L_verbrauch.artnr == s_artnr) &  (L_verbrauch.datum >= from_date) &  (L_verbrauch.datum <= to_date)).all():
            consume_list = Consume_list()
            consume_list_list.append(consume_list)

            buffer_copy(l_verbrauch, consume_list)

    return generate_output()