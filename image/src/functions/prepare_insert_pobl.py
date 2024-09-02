from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, L_order, Htparam, Waehrung, L_lieferant, Parameters, L_artikel

def prepare_insert_pobl(pvilanguage:int, docu_nr:str, lief_nr:int):
    local_nr = 0
    enforce_rflag = False
    zeroprice_flag = False
    potype = 0
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    deptnr = 0
    deptname = ""
    billdate = None
    p_234 = False
    p_266 = 0
    t_amount = 0
    pos = 0
    currency_add_first = ""
    currency_screen_value = ""
    err_flag = False
    disc_list_list = []
    t_l_artikel_list = []
    t_l_orderhdr_list = []
    t_l_order_list = []
    lvcarea:str = "insert_po"
    l_orderhdr = l_order = htparam = waehrung = l_lieferant = parameters = l_artikel = None

    disc_list = t_l_artikel = t_l_orderhdr = t_l_order = None

    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "new_created":bool})
    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":str, "ek_aktuell":decimal, "ek_letzter":decimal, "traubensort":str, "lief_einheit":decimal, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "jahrgang":int, "alkoholgrad":decimal})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, enforce_rflag, zeroprice_flag, potype, lieferdatum, bestellart, comments, supplier, deptnr, deptname, billdate, p_234, p_266, t_amount, pos, currency_add_first, currency_screen_value, err_flag, disc_list_list, t_l_artikel_list, t_l_orderhdr_list, t_l_order_list, lvcarea, l_orderhdr, l_order, htparam, waehrung, l_lieferant, parameters, l_artikel


        nonlocal disc_list, t_l_artikel, t_l_orderhdr, t_l_order
        nonlocal disc_list_list, t_l_artikel_list, t_l_orderhdr_list, t_l_order_list
        return {"local_nr": local_nr, "enforce_rflag": enforce_rflag, "zeroprice_flag": zeroprice_flag, "potype": potype, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "deptnr": deptnr, "deptname": deptname, "billdate": billdate, "p_234": p_234, "p_266": p_266, "t_amount": t_amount, "pos": pos, "currency_add_first": currency_add_first, "currency_screen_value": currency_screen_value, "err_flag": err_flag, "disc-list": disc_list_list, "t-l-artikel": t_l_artikel_list, "t-l-orderhdr": t_l_orderhdr_list, "t-l-order": t_l_order_list}

    def cal_tamount():

        nonlocal local_nr, enforce_rflag, zeroprice_flag, potype, lieferdatum, bestellart, comments, supplier, deptnr, deptname, billdate, p_234, p_266, t_amount, pos, currency_add_first, currency_screen_value, err_flag, disc_list_list, t_l_artikel_list, t_l_orderhdr_list, t_l_order_list, lvcarea, l_orderhdr, l_order, htparam, waehrung, l_lieferant, parameters, l_artikel


        nonlocal disc_list, t_l_artikel, t_l_orderhdr, t_l_order
        nonlocal disc_list_list, t_l_artikel_list, t_l_orderhdr_list, t_l_order_list


        t_amount = 0
        pos = 0

        for l_order in db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0)).all():

            if l_order.loeschflag == 0:
                t_amount = t_amount + l_order.warenwert

            if l_order.pos > pos:
                pos = l_order.pos
            disc_list = Disc_list()
            disc_list_list.append(disc_list)

            disc_list.l_recid = l_order._recid

            if len(l_order.quality) >= 5:
                disc_list.disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) / 100

            if len(l_order.quality) >= 11:
                disc_list.vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) / 100

            if len(l_order.quality) >= 17:
                disc_list.disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) / 100
            disc_list.price0 = l_order.einzelpreis / (1 - disc_list.disc * 0.01) / (1 - disc_list.disc2 * 0.01) / (1 + disc_list.vat * 0.01)
            disc_list.brutto = disc_list.price0 * l_order.anzahl

    def get_currency():

        nonlocal local_nr, enforce_rflag, zeroprice_flag, potype, lieferdatum, bestellart, comments, supplier, deptnr, deptname, billdate, p_234, p_266, t_amount, pos, currency_add_first, currency_screen_value, err_flag, disc_list_list, t_l_artikel_list, t_l_orderhdr_list, t_l_order_list, lvcarea, l_orderhdr, l_order, htparam, waehrung, l_lieferant, parameters, l_artikel


        nonlocal disc_list, t_l_artikel, t_l_orderhdr, t_l_order
        nonlocal disc_list_list, t_l_artikel_list, t_l_orderhdr_list, t_l_order_list

        if l_orderhdr.angebot_lief[2] == 0:
            l_orderhdr.angebot_lief[2] = local_nr

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == l_orderhdr.angebot_lief[2])).first()
        currency_add_first = waehrung.wabkurz
        currency_screen_value = waehrung.wabkurz


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        err_flag = True

        return generate_output()
    local_nr = waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 776)).first()
    zeroprice_flag = flogical

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if l_orderhdr.betriebsnr == 1:
        potype = 2
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    deptnr = l_orderhdr.angebot_lief[0]
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    if deptnr > 0:

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname == to_string(deptnr))).first()
        deptname = parameters.vstring

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 975)).first()

    if htparam.finteger != 1 and htparam.finteger != 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate
    else:
        billdate = get_current_date()
    cal_tamount()
    get_currency()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 234)).first()
    p_234 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 266)).first()
    p_266 = htparam.fdecimal

    if p_234:

        for l_artikel in db_session.query(L_artikel).filter(
                ((L_artikel.lief_nr1 == lief_nr) |  (L_artikel.lief_nr2 == lief_nr) |  (L_artikel.lief_nr3 == lief_nr))).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_list.append(t_l_artikel)

            t_l_artikel.rec_id = l_artikel._recid
            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
            t_l_artikel.ek_letzter = l_artikel.ek_letzter
            t_l_artikel.traubensort = l_artikel.traubensorte
            t_l_artikel.lief_einheit = l_artikel.lief_einheit
            t_l_artikel.lief_nr1 = l_artikel.lief_nr1
            t_l_artikel.lief_nr2 = l_artikel.lief_nr2
            t_l_artikel.lief_nr3 = l_artikel.lief_nr3
            t_l_artikel.jahrgang = l_artikel.jahrgang
            t_l_artikel.alkoholgrad = l_artikel.alkoholgrad


    for l_order in db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos >= 0) &  (L_order.loeschflag == 0)).all():
        t_l_order = T_l_order()
        t_l_order_list.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

    return generate_output()