from functions.additional_functions import *
import decimal
from models import Htparam, Waehrung

def prepare_chg_pr_select_currbl():
    t_currency_list = []
    htparam = waehrung = None

    t_currency = None

    t_currency_list, T_currency = create_model("T_currency", {"currnr":int, "currid":str, "exrate":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_currency_list, htparam, waehrung


        nonlocal t_currency
        nonlocal t_currency_list
        return {"t-currency": t_currency_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        t_currency = T_currency()
        t_currency_list.append(t_currency)

        t_currency.currNr = waehrungsnr
        t_currency.currID = waehrung.wabkurz
        t_currency.exrate = waehrung.ankauf / waehrung.einheit

    for waehrung in db_session.query(Waehrung).filter(
            (Waehrung.wabkurz != htparam.fchar) &  (Waehrung.ankauf > 0)).all():
        t_currency = T_currency()
        t_currency_list.append(t_currency)

        t_currency.currNr = waehrungsnr
        t_currency.currID = waehrung.wabkurz
        t_currency.exrate = waehrung.ankauf / waehrung.einheit

    return generate_output()