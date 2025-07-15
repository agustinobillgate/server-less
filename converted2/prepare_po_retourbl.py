#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_orderhdr, Htparam, L_lieferant, L_artikel, Waehrung

def prepare_po_retourbl(bediener_permissions:string, docu_nr:string):

    prepare_cache ([Htparam, L_lieferant, L_artikel, Waehrung])

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
    exchg_rate = 1
    t_amount = to_decimal("0.0")
    bestellart = ""
    fl_code = 0
    p_1016 = False
    p_224 = None
    p_221 = None
    p_474 = None
    t_l_orderhdr_data = []
    t_l_order_data = []
    t_l_artikel_data = []
    l_order = l_orderhdr = htparam = l_lieferant = l_artikel = waehrung = None

    t_l_artikel = t_l_order = t_l_orderhdr = None

    t_l_artikel_data, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "vk_preis":Decimal, "ek_aktuell":Decimal, "bezeich":string, "endkum":int, "jahrgang":int})
    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, price_decimal, lieferdatum, comments, supplier, currency_add_first, currency_screen_value, exchg_rate, t_amount, bestellart, fl_code, p_1016, p_224, p_221, p_474, t_l_orderhdr_data, t_l_order_data, t_l_artikel_data, l_order, l_orderhdr, htparam, l_lieferant, l_artikel, waehrung
        nonlocal bediener_permissions, docu_nr


        nonlocal t_l_artikel, t_l_order, t_l_orderhdr
        nonlocal t_l_artikel_data, t_l_order_data, t_l_orderhdr_data

        return {"show_price": show_price, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "price_decimal": price_decimal, "lieferdatum": lieferdatum, "comments": comments, "supplier": supplier, "currency_add_first": currency_add_first, "currency_screen_value": currency_screen_value, "exchg_rate": exchg_rate, "t_amount": t_amount, "bestellart": bestellart, "fl_code": fl_code, "p_1016": p_1016, "p_224": p_224, "p_221": p_221, "p_474": p_474, "t-l-orderhdr": t_l_orderhdr_data, "t-l-order": t_l_order_data, "t-l-artikel": t_l_artikel_data}

    def get_currency():

        nonlocal show_price, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, price_decimal, lieferdatum, comments, supplier, currency_add_first, currency_screen_value, exchg_rate, t_amount, bestellart, fl_code, p_1016, p_224, p_221, p_474, t_l_orderhdr_data, t_l_order_data, t_l_artikel_data, l_order, l_orderhdr, htparam, l_lieferant, l_artikel, waehrung
        nonlocal bediener_permissions, docu_nr


        nonlocal t_l_artikel, t_l_order, t_l_orderhdr
        nonlocal t_l_artikel_data, t_l_order_data, t_l_orderhdr_data

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

        if waehrung:
            fl_code = 1
            currency_add_first = waehrung.wabkurz
            currency_screen_value = waehrung.wabkurz
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    def cal_tamount():

        nonlocal show_price, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, price_decimal, lieferdatum, comments, supplier, currency_add_first, currency_screen_value, exchg_rate, t_amount, bestellart, fl_code, p_1016, p_224, p_221, p_474, t_l_orderhdr_data, t_l_order_data, t_l_artikel_data, l_order, l_orderhdr, htparam, l_lieferant, l_artikel, waehrung
        nonlocal bediener_permissions, docu_nr


        nonlocal t_l_artikel, t_l_order, t_l_orderhdr
        nonlocal t_l_artikel_data, t_l_order_data, t_l_orderhdr_data


        t_amount =  to_decimal("0")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if htparam:
        p_224 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

    if htparam:
        p_221 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})

    if htparam:
        p_474 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1016)]})

    if htparam:
        p_1016 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})

    if htparam:
        show_price = htparam.flogical

    if substring(bediener_permissions, 21, 1) != ("0").lower() :
        show_price = True

    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    if not l_orderhdr:

        return generate_output()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_data.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})

    if htparam:
        f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})

    if htparam:
        b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})

    if htparam:
        m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})

    if htparam:
        billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if htparam:
        fb_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

    if htparam:
        m_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_orderhdr.lief_nr)]})

    if l_lieferant:
        supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    cal_tamount()
    get_currency()

    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.geliefert >= 0)).order_by(L_order._recid).all():

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

        if l_artikel:
            t_l_artikel = T_l_artikel()
            t_l_artikel_data.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.vk_preis =  to_decimal(l_artikel.vk_preis)
            t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.endkum = l_artikel.endkum
            t_l_artikel.jahrgang = l_artikel.jahrgang


            t_l_order = T_l_order()
            t_l_order_data.append(t_l_order)

            buffer_copy(l_order, t_l_order)
            t_l_order.rec_id = l_order._recid

    return generate_output()