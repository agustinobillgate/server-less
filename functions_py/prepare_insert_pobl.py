#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, L_order, Htparam, Waehrung, L_lieferant, Parameters, L_artikel

def prepare_insert_pobl(pvilanguage:int, docu_nr:string, lief_nr:int):

    prepare_cache ([Htparam, Waehrung, L_lieferant, Parameters, L_artikel])

    local_nr = 0
    enforce_rflag = False
    zeroprice_flag = False
    potype = 1
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    deptnr = 0
    deptname = ""
    billdate = None
    p_234 = False
    p_266 = to_decimal("0.0")
    t_amount = to_decimal("0.0")
    pos = 0
    currency_add_first = ""
    currency_screen_value = ""
    err_flag = False
    disc_list_data = []
    t_l_artikel_data = []
    t_l_orderhdr_data = []
    t_l_order_data = []
    lvcarea:string = "insert-po"
    l_orderhdr = l_order = htparam = waehrung = l_lieferant = parameters = l_artikel = None

    disc_list = t_l_artikel = t_l_orderhdr = t_l_order = None

    disc_list_data, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "new_created":bool})
    t_l_artikel_data, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":string, "ek_aktuell":Decimal, "ek_letzter":Decimal, "traubensort":string, "lief_einheit":Decimal, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "jahrgang":int, "alkoholgrad":Decimal})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int})

    db_session = local_storage.db_session
    docu_nr = docu_nr.strip()


    def generate_output():
        nonlocal local_nr, enforce_rflag, zeroprice_flag, potype, lieferdatum, bestellart, comments, supplier, deptnr, deptname, billdate, p_234, p_266, t_amount, pos, currency_add_first, currency_screen_value, err_flag, disc_list_data, t_l_artikel_data, t_l_orderhdr_data, t_l_order_data, lvcarea, l_orderhdr, l_order, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal pvilanguage, docu_nr, lief_nr


        nonlocal disc_list, t_l_artikel, t_l_orderhdr, t_l_order
        nonlocal disc_list_data, t_l_artikel_data, t_l_orderhdr_data, t_l_order_data

        return {"local_nr": local_nr, "enforce_rflag": enforce_rflag, "zeroprice_flag": zeroprice_flag, "potype": potype, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "deptnr": deptnr, "deptname": deptname, "billdate": billdate, "p_234": p_234, "p_266": p_266, "t_amount": t_amount, "pos": pos, "currency_add_first": currency_add_first, "currency_screen_value": currency_screen_value, "err_flag": err_flag, "disc-list": disc_list_data, "t-l-artikel": t_l_artikel_data, "t-l-orderhdr": t_l_orderhdr_data, "t-l-order": t_l_order_data}

    def cal_tamount():

        nonlocal local_nr, enforce_rflag, zeroprice_flag, potype, lieferdatum, bestellart, comments, supplier, deptnr, deptname, billdate, p_234, p_266, t_amount, pos, currency_add_first, currency_screen_value, err_flag, disc_list_data, t_l_artikel_data, t_l_orderhdr_data, t_l_order_data, lvcarea, l_orderhdr, l_order, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal pvilanguage, docu_nr, lief_nr


        nonlocal disc_list, t_l_artikel, t_l_orderhdr, t_l_order
        nonlocal disc_list_data, t_l_artikel_data, t_l_orderhdr_data, t_l_order_data


        t_amount =  to_decimal("0")
        pos = 0

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0)).order_by(L_order._recid).all():

            if l_order.loeschflag == 0:
                t_amount =  to_decimal(t_amount) + to_decimal(l_order.warenwert)

            if l_order.pos > pos:
                pos = l_order.pos
            disc_list = Disc_list()
            disc_list_data.append(disc_list)

            disc_list.l_recid = l_order._recid

            if length(l_order.quality) >= 5:
                disc_list.disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) / 100

            if length(l_order.quality) >= 11:
                disc_list.vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) / 100

            if length(l_order.quality) >= 17:
                disc_list.disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) / 100
            disc_list.price0 =  to_decimal(l_order.einzelpreis) / to_decimal((1) - to_decimal(disc_list.disc) * to_decimal(0.01)) / to_decimal((1) - to_decimal(disc_list.disc2) * to_decimal(0.01)) / to_decimal((1) + to_decimal(disc_list.vat) * to_decimal(0.01))
            disc_list.brutto =  to_decimal(disc_list.price0) * to_decimal(l_order.anzahl)


    def get_currency():

        nonlocal local_nr, enforce_rflag, zeroprice_flag, potype, lieferdatum, bestellart, comments, supplier, deptnr, deptname, billdate, p_234, p_266, t_amount, pos, currency_add_first, currency_screen_value, err_flag, disc_list_data, t_l_artikel_data, t_l_orderhdr_data, t_l_order_data, lvcarea, l_orderhdr, l_order, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal pvilanguage, docu_nr, lief_nr


        nonlocal disc_list, t_l_artikel, t_l_orderhdr, t_l_order
        nonlocal disc_list_data, t_l_artikel_data, t_l_orderhdr_data, t_l_order_data

        if l_orderhdr.angebot_lief[2] == 0:
            l_orderhdr.angebot_lief[2] = local_nr

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, l_orderhdr.angebot_lief[2])]})
        currency_add_first = waehrung.wabkurz
        currency_screen_value = waehrung.wabkurz

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        err_flag = True

        return generate_output()
    local_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    enforce_rflag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 776)]})
    zeroprice_flag = htparam.flogical

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

    # l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr.docu_nr == (docu_nr).lower())).with_for_update().first()

    if l_orderhdr.betriebsnr == 1:
        potype = 2
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    deptnr = l_orderhdr.angebot_lief[0]
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_data.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    if deptnr > 0:

        parameters = get_cache (Parameters, {"progname": [(eq, "costcenter")],"section": [(eq, "name")],"varname": [(eq, to_string(deptnr))]})
        deptname = parameters.vstring

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

    if htparam.finteger != 1 and htparam.finteger != 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate
    else:
        billdate = get_current_date()
    cal_tamount()
    get_currency()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 234)]})
    p_234 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 266)]})
    p_266 =  to_decimal(htparam.fdecimal)

    if p_234:

        for l_artikel in db_session.query(L_artikel).filter(
                 ((L_artikel.lief_nr1 == lief_nr) | (L_artikel.lief_nr2 == lief_nr) | (L_artikel.lief_nr3 == lief_nr))).order_by(L_artikel._recid).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_data.append(t_l_artikel)

            t_l_artikel.rec_id = l_artikel._recid
            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
            t_l_artikel.ek_letzter =  to_decimal(l_artikel.ek_letzter)
            t_l_artikel.traubensort = l_artikel.traubensorte
            t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
            t_l_artikel.lief_nr1 = l_artikel.lief_nr1
            t_l_artikel.lief_nr2 = l_artikel.lief_nr2
            t_l_artikel.lief_nr3 = l_artikel.lief_nr3
            t_l_artikel.jahrgang = l_artikel.jahrgang
            t_l_artikel.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)


    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos >= 0) & (L_order.loeschflag == 0)).order_by(L_order._recid).all():
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

    return generate_output()