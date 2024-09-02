from functions.additional_functions import *
import decimal
from models import Waehrung, Hoteldpt, Artikel, Htparam

def prepare_money_exchgbl():
    local_nr = 0
    local_code = ""
    price_decimal = 0
    err_code = 0
    t_waehrung_list = []
    t_hoteldpt_list = []
    art1_list = []
    waehrung = hoteldpt = artikel = htparam = None

    t_waehrung = t_hoteldpt = art1 = art2 = None

    t_waehrung_list, T_waehrung = create_model_like(Waehrung)
    t_hoteldpt_list, T_hoteldpt = create_model_like(Hoteldpt)
    art1_list, Art1 = create_model_like(Artikel)

    Art2 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, local_code, price_decimal, err_code, t_waehrung_list, t_hoteldpt_list, art1_list, waehrung, hoteldpt, artikel, htparam
        nonlocal art2


        nonlocal t_waehrung, t_hoteldpt, art1, art2
        nonlocal t_waehrung_list, t_hoteldpt_list, art1_list
        return {"local_nr": local_nr, "local_code": local_code, "price_decimal": price_decimal, "err_code": err_code, "t-waehrung": t_waehrung_list, "t-hoteldpt": t_hoteldpt_list, "art1": art1_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 112)).first()

    art2 = db_session.query(Art2).filter(
            (Art2.artnr == htparam.finteger) &  (Art2.departement == 0) &  (Art2.artart == 6) &  (not Art2.pricetab)).first()

    if not art2:
        err_code = 1

        return generate_output()
    local_nr = art2.artnr
    art1 = Art1()
    art1_list.append(art1)

    buffer_copy(art2, art1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    local_code = htparam.fchar

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == local_code)).first()

    if not waehrung:
        err_code = 2

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    for waehrung in db_session.query(Waehrung).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    for hoteldpt in db_session.query(Hoteldpt).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()