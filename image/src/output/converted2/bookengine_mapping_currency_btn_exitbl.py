#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_mapping_currency_list, T_mapping_currency = create_model("T_mapping_currency", {"currencyvhp":string, "currencybe":string, "descr":string, "nr":int})

def bookengine_mapping_currency_btn_exitbl(t_mapping_currency_list:[T_mapping_currency], bookengid:int):

    prepare_cache ([Queasy])

    queasy = None

    t_mapping_currency = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal bookengid


        nonlocal t_mapping_currency

        return {}

    for t_mapping_currency in query(t_mapping_currency_list):

        queasy = get_cache (Queasy, {"key": [(eq, 164)],"number1": [(eq, bookengid)],"number2": [(eq, t_mapping_currency.nr)]})

        if queasy:
            queasy.char2 = t_mapping_currency.currencybe
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 164
            queasy.number1 = bookengid
            queasy.number2 = t_mapping_currency.nr
            queasy.char1 = t_mapping_currency.currencyvhp

    return generate_output()