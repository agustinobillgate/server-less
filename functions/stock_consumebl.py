#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_verbrauch

def stock_consumebl(s_artnr:int, from_date:date, to_date:date):
    qty = to_decimal("0.0")
    val = to_decimal("0.0")
    consume_list_data = []
    l_verbrauch = None

    consume_list = None

    consume_list_data, Consume_list = create_model("Consume_list", {"artnr":int, "datum":date, "anz_verbrau":Decimal, "wert_verbrau":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal qty, val, consume_list_data, l_verbrauch
        nonlocal s_artnr, from_date, to_date


        nonlocal consume_list
        nonlocal consume_list_data

        return {"qty": qty, "val": val, "consume-list": consume_list_data}

    if from_date == None:

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == s_artnr)).order_by(L_verbrauch._recid).all():
            qty =  to_decimal(qty) + to_decimal(l_verbrauch.anz_verbrau)
            val =  to_decimal(val) + to_decimal(l_verbrauch.wert_verbrau)

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == s_artnr)).order_by(L_verbrauch.datum).all():
            consume_list = Consume_list()
            consume_list_data.append(consume_list)

            buffer_copy(l_verbrauch, consume_list)
    else:

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == s_artnr) & (L_verbrauch.datum >= from_date) & (L_verbrauch.datum <= to_date)).order_by(L_verbrauch._recid).all():
            qty =  to_decimal(qty) + to_decimal(anz_verbrau)
            val =  to_decimal(val) + to_decimal(L_verbrauch.wert_verbrau)

        for l_verbrauch in db_session.query(L_verbrauch).filter(
                 (L_verbrauch.artnr == s_artnr) & (L_verbrauch.datum >= from_date) & (L_verbrauch.datum <= to_date)).order_by(L_verbrauch.datum).all():
            consume_list = Consume_list()
            consume_list_data.append(consume_list)

            buffer_copy(l_verbrauch, consume_list)

    return generate_output()