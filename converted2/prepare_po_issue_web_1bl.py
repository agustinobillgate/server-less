#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_orderhdr, L_lager, Htparam, Bediener, L_lieferant, Parameters, L_artikel, Queasy, Waehrung

def prepare_po_issue_web_1bl(pvilanguage:int, lief_nr:int, user_init:string, docu_nr:string):

    prepare_cache ([Htparam, L_lieferant, Parameters, L_artikel, Queasy, Waehrung])

    enforce_rflag = False
    show_price = False
    higherprice_flag = False
    disc_flag = False
    price_decimal = 0
    qty_flag = False
    qty_tol = 0
    crterm = 0
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    deptname = ""
    f_endkum = 0
    b_endkum = 0
    m_endkum = 0
    billdate = None
    fb_closedate = None
    m_closedate = None
    last_mdate = None
    last_fbdate = None
    err_code = 0
    t_amount = to_decimal("0.0")
    waehrung_wabkurz = ""
    exchg_rate = 1
    msg_str = ""
    ci_date = None
    t_l_orderhdr_data = []
    t_l_lager_data = []
    t_l_order_data = []
    l_order = l_orderhdr = l_lager = htparam = bediener = l_lieferant = parameters = l_artikel = queasy = waehrung = None

    t_l_order = t_l_orderhdr = t_l_lager = None

    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "jahrgang":int, "alkoholgrad":Decimal, "curr_disc":int, "curr_disc2":int, "curr_vat":int, "add_vat":Decimal, "addvat_no":int, "addvat_value":Decimal, "amount":Decimal, "traubensorte":string, "masseinheit":string})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_lager_data, T_l_lager = create_model_like(L_lager)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, show_price, higherprice_flag, disc_flag, price_decimal, qty_flag, qty_tol, crterm, lieferdatum, bestellart, comments, supplier, deptname, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, err_code, t_amount, waehrung_wabkurz, exchg_rate, msg_str, ci_date, t_l_orderhdr_data, t_l_lager_data, t_l_order_data, l_order, l_orderhdr, l_lager, htparam, bediener, l_lieferant, parameters, l_artikel, queasy, waehrung
        nonlocal pvilanguage, lief_nr, user_init, docu_nr


        nonlocal t_l_order, t_l_orderhdr, t_l_lager
        nonlocal t_l_order_data, t_l_orderhdr_data, t_l_lager_data

        return {"enforce_rflag": enforce_rflag, "show_price": show_price, "higherprice_flag": higherprice_flag, "disc_flag": disc_flag, "price_decimal": price_decimal, "qty_flag": qty_flag, "qty_tol": qty_tol, "crterm": crterm, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "deptname": deptname, "f_endkum": f_endkum, "b_endkum": b_endkum, "m_endkum": m_endkum, "billdate": billdate, "fb_closedate": fb_closedate, "m_closedate": m_closedate, "last_mdate": last_mdate, "last_fbdate": last_fbdate, "err_code": err_code, "t_amount": t_amount, "waehrung_wabkurz": waehrung_wabkurz, "exchg_rate": exchg_rate, "msg_str": msg_str, "ci_date": ci_date, "t-l-orderhdr": t_l_orderhdr_data, "t-l-lager": t_l_lager_data, "t-l-order": t_l_order_data}

    def cal_tamount():

        nonlocal enforce_rflag, show_price, higherprice_flag, disc_flag, price_decimal, qty_flag, qty_tol, crterm, lieferdatum, bestellart, comments, supplier, deptname, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, err_code, t_amount, waehrung_wabkurz, exchg_rate, msg_str, ci_date, t_l_orderhdr_data, t_l_lager_data, t_l_order_data, l_order, l_orderhdr, l_lager, htparam, bediener, l_lieferant, parameters, l_artikel, queasy, waehrung
        nonlocal pvilanguage, lief_nr, user_init, docu_nr


        nonlocal t_l_order, t_l_orderhdr, t_l_lager
        nonlocal t_l_order_data, t_l_orderhdr_data, t_l_lager_data


        t_amount =  to_decimal("0")


    def get_currency():

        nonlocal enforce_rflag, show_price, higherprice_flag, disc_flag, price_decimal, qty_flag, qty_tol, crterm, lieferdatum, bestellart, comments, supplier, deptname, f_endkum, b_endkum, m_endkum, billdate, fb_closedate, m_closedate, last_mdate, last_fbdate, err_code, t_amount, waehrung_wabkurz, exchg_rate, msg_str, ci_date, t_l_orderhdr_data, t_l_lager_data, t_l_order_data, l_order, l_orderhdr, l_lager, htparam, bediener, l_lieferant, parameters, l_artikel, queasy, waehrung
        nonlocal pvilanguage, lief_nr, user_init, docu_nr


        nonlocal t_l_order, t_l_orderhdr, t_l_lager
        nonlocal t_l_order_data, t_l_orderhdr_data, t_l_lager_data

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})

        if waehrung:
            waehrung_wabkurz = waehrung.wabkurz
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    if not l_orderhdr:
        err_code = 1

        return generate_output()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_data.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})

    if htparam:
        enforce_rflag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})

    if htparam:
        show_price = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 350)]})

    if htparam:
        higherprice_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 349)]})

    if htparam:

        if htparam.feldtyp != 4:
            disc_flag = False


        else:
            disc_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1010)],"paramgruppe": [(eq, 21)]})

    if htparam:
        qty_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1011)],"paramgruppe": [(eq, 21)]})

        if htparam:
            qty_tol = htparam.finteger


    crterm = l_orderhdr.angebot_lief[1]

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

    if parameters:
        deptname = parameters.vstring

    htparam = get_cache (Htparam, {"paramnr": [(eq, 257)]})
    f_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 258)]})
    b_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    m_endkum = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    fb_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    m_closedate = htparam.fdate

    if billdate == None or billdate > get_current_date():
        billdate = get_current_date()
    else:

        if m_closedate != None:
            last_mdate = date_mdy(get_month(m_closedate) , 1, get_year(m_closedate)) - timedelta(days=1)

        if fb_closedate != None:
            last_fbdate = date_mdy(get_month(fb_closedate) , 1, get_year(fb_closedate)) - timedelta(days=1)

        if (billdate <= last_mdate) or (billdate <= last_fbdate):
            msg_str = msg_str + chr_unicode(2) + "&W" + "Receiving Date might be incorrect (too old)," + chr_unicode(10) + "Please re-check it."

        htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})

        if htparam.fdate != None and billdate <= htparam.fdate:
            msg_str = msg_str + chr_unicode(2) + "&W" + "Wrong receiving date (ParamNo 474):" + chr_unicode(10) + "Older than last transfer date to the G/L."

            return generate_output()
    cal_tamount()
    get_currency()

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_order in db_session.query(L_order).filter(
             (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.docu_nr == (docu_nr).lower())).order_by(L_order._recid).all():
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

        if l_artikel:
            t_l_order.a_bezeich = l_artikel.bezeich
            t_l_order.jahrgang = l_artikel.jahrgang
            t_l_order.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)
            t_l_order.curr_disc = to_int(substring(t_l_order.quality, 0, 2)) * 100 + to_int(substring(t_l_order.quality, 3, 2))
            t_l_order.curr_vat = to_int(substring(t_l_order.quality, 6, 2)) * 100 + to_int(substring(t_l_order.quality, 9, 2))
            t_l_order.curr_disc2 = 0
            t_l_order.traubensorte = l_artikel.traubensorte
            t_l_order.masseinheit = l_artikel.masseinheit

            if l_artikel.lief_einheit > 1 and t_l_order.geliefert > 0:
                t_l_order.angebot_lief[0] = t_l_order.geliefert % l_artikel.lief_einheit
                t_l_order.geliefert = ( to_decimal(t_l_order.geliefert) - to_decimal(t_l_order.angebot_lief [0])) / to_decimal(l_artikel.lief_einheit)

        if length(t_l_order.quality) >= 17:
            t_l_order.curr_disc2 = to_int(substring(t_l_order.quality, 12, 2)) * 100 + to_int(substring(t_l_order.quality, 15, 2))
        t_l_order.amount =  to_decimal(t_l_order.warenwert)

        queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_order.docu_nr)],"number1": [(eq, l_order.artnr)]})

        if queasy:
            t_l_order.add_vat =  to_decimal(l_order.warenwert) * to_decimal((queasy.deci1) / to_decimal("100") )
            t_l_order.addvat_no = queasy.number2
            t_l_order.addvat_value =  to_decimal(queasy.deci1)
            t_l_order.amount =  to_decimal(t_l_order.amount) + to_decimal(t_l_order.add_vat)

    return generate_output()