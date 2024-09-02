from functions.additional_functions import *
import decimal
from models import Htparam, Waehrung, Hoteldpt

def prepare_quick_postbl():
    foreign_rate = False
    double_currency = False
    price_decimal = 0
    exchg_rate = 0
    curr_local = ""
    curr_foreign = ""
    t_hoteldpt_list = []
    htparam = waehrung = hoteldpt = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal foreign_rate, double_currency, price_decimal, exchg_rate, curr_local, curr_foreign, t_hoteldpt_list, htparam, waehrung, hoteldpt


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list
        return {"foreign_rate": foreign_rate, "double_currency": double_currency, "price_decimal": price_decimal, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "t-hoteldpt": t_hoteldpt_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = fchar

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num

    return generate_output()