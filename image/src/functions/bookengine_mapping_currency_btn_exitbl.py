from functions.additional_functions import *
import decimal
from models import Queasy

def bookengine_mapping_currency_btn_exitbl(t_mapping_currency:[T_mapping_currency], bookengid:int):
    queasy = None

    t_mapping_currency = None

    t_mapping_currency_list, T_mapping_currency = create_model("T_mapping_currency", {"currencyvhp":str, "currencybe":str, "descr":str, "nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal t_mapping_currency
        nonlocal t_mapping_currency_list
        return {}

    for t_mapping_currency in query(t_mapping_currency_list):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 164) &  (Queasy.number1 == bookengid) &  (Queasy.number2 == t_mapping_currency.nr)).first()

        if queasy:
            queasy.char2 = t_mapping_currency.currencyBE
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 164
            queasy.number1 = bookengid
            queasy.number2 = t_mapping_currency.nr
            queasy.char1 = t_mapping_currency.currency
            END

    return generate_output()