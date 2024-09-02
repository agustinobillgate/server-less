from functions.additional_functions import *
import decimal
from models import Waehrung, Queasy

def prepare_bookengine_mapping_currencybl(bookengid:int):
    t_mapping_currency_list = []
    waehrung = queasy = None

    t_mapping_currency = None

    t_mapping_currency_list, T_mapping_currency = create_model("T_mapping_currency", {"currencyvhp":str, "currencybe":str, "descr":str, "nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mapping_currency_list, waehrung, queasy


        nonlocal t_mapping_currency
        nonlocal t_mapping_currency_list
        return {"t-mapping-currency": t_mapping_currency_list}

    for waehrung in db_session.query(Waehrung).all():
        t_mapping_currency = T_mapping_currency()
        t_mapping_currency_list.append(t_mapping_currency)

        t_mapping_currency.currencyVHP = waehrung.wabkurz
        t_mapping_currency.descr = waehrung.bezeich
        t_mapping_currency.nr = waehrungsnr

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 164) &  (Queasy.number1 == bookengid) &  (Queasy.number2 == waehrungsnr)).first()

        if queasy:
            t_mapping_currency.currencyBE = queasy.char2
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 164
            queasy.number1 = bookengid
            queasy.number2 = waehrungsnr
            queasy.char1 = waehrung.wabkurz

    return generate_output()