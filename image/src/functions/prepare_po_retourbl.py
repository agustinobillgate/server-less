from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_orderhdr, Htparam, L_lieferant, L_artikel, Waehrung

def prepare_po_retourbl(bediener_permissions:str, docu_nr:str):
    show_price = False
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    price_decimal = 0
    lieferdatum = None
    comments = ""
    supplier = ""
    currency_add_first = ""
    currency_screen_value = ""
    exchg_rate = 0
    t_amount = 0
    bestellart = ""
    fl_code = 0
    p_1016 = False
    p_224 = None
    p_221 = None
    p_474 = None
    t_l_orderhdr_list = []
    t_l_order_list = []
    t_l_artikel_list = []
    l_order = l_orderhdr = htparam = l_lieferant = l_artikel = waehrung = None

    t_l_artikel = t_l_order = t_l_orderhdr = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "vk_preis":decimal, "ek_aktuell":decimal, "bezeich":str, "endkum":int, "jahrgang":int})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, price_decimal, lieferdatum, comments, supplier, currency_add_first, currency_screen_value, exchg_rate, t_amount, bestellart, fl_code, p_1016, p_224, p_221, p_474, t_l_orderhdr_list, t_l_order_list, t_l_artikel_list, l_order, l_orderhdr, htparam, l_lieferant, l_artikel, waehrung


        nonlocal t_l_artikel, t_l_order, t_l_orderhdr
        nonlocal t_l_artikel_list, t_l_order_list, t_l_orderhdr_list
        return {"show_price": show_price, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "price_decimal": price_decimal, "lieferdatum": lieferdatum, "comments": comments, "supplier": supplier, "currency_add_first": currency_add_first, "currency_screen_value": currency_screen_value, "exchg_rate": exchg_rate, "t_amount": t_amount, "bestellart": bestellart, "fl_code": fl_code, "p_1016": p_1016, "p_224": p_224, "p_221": p_221, "p_474": p_474, "t-l-orderhdr": t_l_orderhdr_list, "t-l-order": t_l_order_list, "t-l-artikel": t_l_artikel_list}

    def get_currency():

        nonlocal show_price, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, price_decimal, lieferdatum, comments, supplier, currency_add_first, currency_screen_value, exchg_rate, t_amount, bestellart, fl_code, p_1016, p_224, p_221, p_474, t_l_orderhdr_list, t_l_order_list, t_l_artikel_list, l_order, l_orderhdr, htparam, l_lieferant, l_artikel, waehrung


        nonlocal t_l_artikel, t_l_order, t_l_orderhdr
        nonlocal t_l_artikel_list, t_l_order_list, t_l_orderhdr_list

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()

        if waehrung:
            fl_code = 1
            currency_add_first = waehrung.wabkurz
            currency_screen_value = waehrung.wabkurz
            exchg_rate = waehrung.ankauf / waehrung.einheit

    def cal_tamount():

        nonlocal show_price, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, price_decimal, lieferdatum, comments, supplier, currency_add_first, currency_screen_value, exchg_rate, t_amount, bestellart, fl_code, p_1016, p_224, p_221, p_474, t_l_orderhdr_list, t_l_order_list, t_l_artikel_list, l_order, l_orderhdr, htparam, l_lieferant, l_artikel, waehrung


        nonlocal t_l_artikel, t_l_order, t_l_orderhdr
        nonlocal t_l_artikel_list, t_l_order_list, t_l_orderhdr_list


        t_amount = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    p_224 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    p_221 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    p_474 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1016)).first()
    p_1016 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener_permissions, 21, 1) != "0":
        show_price = True

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 257)).first()
    f_endkum = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 258)).first()
    b_endkum = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 268)).first()
    m_endkum = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    fb_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    m_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    cal_tamount()
    get_currency()

    for l_order in db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.geliefert >= 0)).all():

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_order.artnr)).first()

        if l_artikel:
            t_l_artikel = T_l_artikel()
            t_l_artikel_list.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.vk_preis = l_artikel.vk_preis
            t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.endkum = l_artikel.endkum
            t_l_artikel.jahrgang = l_artikel.jahrgang


            t_l_order = T_l_order()
            t_l_order_list.append(t_l_order)

            buffer_copy(l_order, t_l_order)
            t_l_order.rec_id = l_order._recid

    return generate_output()