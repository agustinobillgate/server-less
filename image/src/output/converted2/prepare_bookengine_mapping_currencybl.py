#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Queasy

def prepare_bookengine_mapping_currencybl(bookengid:int):

    prepare_cache ([Waehrung, Queasy])

    t_mapping_currency_list = []
    waehrung = queasy = None

    t_mapping_currency = None

    t_mapping_currency_list, T_mapping_currency = create_model("T_mapping_currency", {"currencyvhp":string, "currencybe":string, "descr":string, "nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mapping_currency_list, waehrung, queasy
        nonlocal bookengid


        nonlocal t_mapping_currency
        nonlocal t_mapping_currency_list

        return {"t-mapping-currency": t_mapping_currency_list}

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
        t_mapping_currency = T_mapping_currency()
        t_mapping_currency_list.append(t_mapping_currency)

        t_mapping_currency.currencyvhp = waehrung.wabkurz
        t_mapping_currency.descr = waehrung.bezeich
        t_mapping_currency.nr = waehrung.waehrungsnr

        queasy = get_cache (Queasy, {"key": [(eq, 164)],"number1": [(eq, bookengid)],"number2": [(eq, waehrung.waehrungsnr)]})

        if queasy:
            t_mapping_currency.currencybe = queasy.char2
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 164
            queasy.number1 = bookengid
            queasy.number2 = waehrung.waehrungsnr
            queasy.char1 = waehrung.wabkurz

    return generate_output()