from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from models import L_order, L_orderhdr, Htparam, Waehrung, L_lieferant, Parameters, L_artikel

def prepare_mk_po_webbl(docu_nr:str, pvilanguage:int, lief_nr:int, pr_deptnr:int, po_type:int, potype:int, bediener_username:str, ordername_screen_value:str, crterm:int):
    local_nr = 0
    billdate = None
    zeroprice_flag = False
    deptname = ""
    supplier = ""
    curr_liefnr = 0
    p_222 = False
    p_234 = False
    p_266 = 0
    pos = 0
    t_amount = 0
    currency_add_first = ""
    currency_screen_value = ""
    msg_str = ""
    p_1093 = 0
    p_464 = 0
    p_220 = 0
    t_waehrung_list = []
    t_l_order_list = []
    t_l_orderhdr_list = []
    t_parameters_list = []
    lvcarea:str = "mk_po"
    l_order = l_orderhdr = htparam = waehrung = l_lieferant = parameters = l_artikel = None

    t_parameters = t_waehrung = t_l_order = t_l_orderhdr = l_orderhdr1 = None

    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})
    t_waehrung_list, T_waehrung = create_model("T_waehrung", {"wabkurz":str})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":str, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_val":decimal, "disc2_val":decimal, "vat_val":decimal})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    L_orderhdr1 = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, billdate, zeroprice_flag, deptname, supplier, curr_liefnr, p_222, p_234, p_266, pos, t_amount, currency_add_first, currency_screen_value, msg_str, p_1093, p_464, p_220, t_waehrung_list, t_l_order_list, t_l_orderhdr_list, t_parameters_list, lvcarea, l_order, l_orderhdr, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal l_orderhdr1


        nonlocal t_parameters, t_waehrung, t_l_order, t_l_orderhdr, l_orderhdr1
        nonlocal t_parameters_list, t_waehrung_list, t_l_order_list, t_l_orderhdr_list
        return {"local_nr": local_nr, "billdate": billdate, "zeroprice_flag": zeroprice_flag, "deptname": deptname, "supplier": supplier, "curr_liefnr": curr_liefnr, "p_222": p_222, "p_234": p_234, "p_266": p_266, "pos": pos, "t_amount": t_amount, "currency_add_first": currency_add_first, "currency_screen_value": currency_screen_value, "msg_str": msg_str, "p_1093": p_1093, "p_464": p_464, "p_220": p_220, "t-waehrung": t_waehrung_list, "t-l-order": t_l_order_list, "t-l-orderhdr": t_l_orderhdr_list, "t-parameters": t_parameters_list}

    def new_po_number():

        nonlocal local_nr, billdate, zeroprice_flag, deptname, supplier, curr_liefnr, p_222, p_234, p_266, pos, t_amount, currency_add_first, currency_screen_value, msg_str, p_1093, p_464, p_220, t_waehrung_list, t_l_order_list, t_l_orderhdr_list, t_parameters_list, lvcarea, l_order, l_orderhdr, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal l_orderhdr1


        nonlocal t_parameters, t_waehrung, t_l_order, t_l_orderhdr, l_orderhdr1
        nonlocal t_parameters_list, t_waehrung_list, t_l_order_list, t_l_orderhdr_list

        s:str = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        L_orderhdr1 = L_orderhdr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 973)).first()

        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(billdate)
            yy = get_year(billdate)
            s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                    (get_month(L_orderhdr1.bestelldatum) == mm) &  (get_year(L_orderhdr1.bestelldatum) == yy) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
                i = to_int(substring(l_orderhdr1.docu_nr, 5, 5))
                i = i + 1
                docu_nr = s + to_string(i, "99999")

                return
            docu_nr = s + to_string(i, "99999")

            return
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                (L_orderhdr1.bestelldatum == billdate) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")

            return
        docu_nr = s + to_string(i, "999")

    def currency_list():

        nonlocal local_nr, billdate, zeroprice_flag, deptname, supplier, curr_liefnr, p_222, p_234, p_266, pos, t_amount, currency_add_first, currency_screen_value, msg_str, p_1093, p_464, p_220, t_waehrung_list, t_l_order_list, t_l_orderhdr_list, t_parameters_list, lvcarea, l_order, l_orderhdr, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal l_orderhdr1


        nonlocal t_parameters, t_waehrung, t_l_order, t_l_orderhdr, l_orderhdr1
        nonlocal t_parameters_list, t_waehrung_list, t_l_order_list, t_l_orderhdr_list

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == local_nr)).first()
        currency_add_first = waehrung.wabkurz
        currency_screen_value = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                (Waehrungsnr != local_nr) &  (Waehrung.ankauf > 0) &  (Waehrung.betriebsnr != 0)).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        msg_str = msg_str + chr(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    local_nr = waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 975)).first()

    if htparam.finteger != 1 and htparam.finteger != 2:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate
    else:
        billdate = get_current_date()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 776)).first()
    zeroprice_flag = flogical

    if docu_nr == "":
        new_po_number()
    currency_list()

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()
    p_1093 = get_output(htpint(1093))
    p_464 = get_output(htpint(464))
    p_220 = get_output(htpint(220))

    if po_type == 1:

        l_orderhdr = db_session.query(L_orderhdr).filter(
                    (L_orderhdr.lief_nr == lief_nr) &  (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

        if not l_orderhdr:
            l_orderhdr = L_orderhdr()
            db_session.add(l_orderhdr)

            l_orderhdr.lief_nr = lief_nr
            l_orderhdr.docu_nr = docu_nr


        l_orderhdr.angebot_lief[0] = pr_deptnr
        l_orderhdr.bestelldatum = billdate
        l_orderhdr.lieferdatum = billdate + 1
        l_orderhdr.besteller = bediener_username
        l_orderhdr.lief_fax[0] = l_lieferant.fax
        l_orderhdr.lief_fax[1] = ordername_screen_value
        l_orderhdr.angebot_lief[1] = crterm
        l_orderhdr.angebot_lief[2] = local_nr
        l_orderhdr.gedruckt = None

        if potype == 2:
            l_orderhdr.betriebsnr = 1

        if pr_deptnr != 0:

            parameters = db_session.query(Parameters).filter(
                        (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

        if parameters:
            deptname = parameters.vstring

        l_orderhdr = db_session.query(L_orderhdr).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
                (L_orderhdr.lief_nr == lief_nr) &  (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    curr_liefnr = lief_nr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    p_222 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 234)).first()
    p_234 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 266)).first()
    p_266 = htparam.fdecimal
    pos = 0
    t_amount = 0

    for l_order in db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
        t_l_order = T_l_order()
        t_l_order_list.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == l_order.artnr)).first()
        t_l_order.a_bezeich = l_artikel.bezeich

        if l_order.lief_nr == lief_nr and l_order.loeschflag == 0 and docu_nr != "":
            pos = pos + 1

            if len(l_order.quality) >= 5:
                t_l_order.disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) / 100

            if len(l_order.quality) >= 11:
                t_l_order.vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) / 100

            if len(l_order.quality) >= 17:
                t_l_order.disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) / 100
            t_l_order.price0 = l_order.einzelpreis / (1 - t_l_order.disc * 0.01) / (1 - t_l_order.disc2 * 0.01) / (1 + t_l_order.vat * 0.01)
            t_l_order.brutto = t_l_order.price0 * l_order.anzahl
            t_amount = t_amount + l_order.warenwert

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    return generate_output()