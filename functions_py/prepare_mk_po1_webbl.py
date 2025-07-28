#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 28/7/2025
#
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from models import L_order, L_orderhdr, Htparam, Waehrung, L_lieferant, Parameters, L_artikel

def prepare_mk_po1_webbl(docu_nr:string, pvilanguage:int, lief_nr:int, pr_deptnr:int, po_type:int, potype:int, bediener_username:string, ordername_screen_value:string, crterm:int):

    prepare_cache ([Htparam, Waehrung, L_lieferant, Parameters, L_artikel])

    local_nr = 0
    billdate = None
    zeroprice_flag = False
    deptname = ""
    supplier = ""
    curr_liefnr = 0
    p_222 = False
    p_234 = False
    p_266 = to_decimal("0.0")
    pos = 0
    t_amount = to_decimal("0.0")
    currency_add_first = ""
    currency_screen_value = ""
    msg_str = ""
    p_1093 = 0
    p_464 = 0
    p_220 = 0
    docunr = ""
    t_waehrung_data = []
    t_l_order_data = []
    t_l_orderhdr_data = []
    t_parameters_data = []
    lvcarea:string = "mk-po"
    l_order = l_orderhdr = htparam = waehrung = l_lieferant = parameters = l_artikel = None

    t_parameters = t_waehrung = t_l_order = t_l_orderhdr = None

    t_parameters_data, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})
    t_waehrung_data, T_waehrung = create_model("T_waehrung", {"wabkurz":string, "waehrungsnr":int})
    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "a_bezeich":string, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "disc_val":Decimal, "disc2_val":Decimal, "vat_val":Decimal})
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, billdate, zeroprice_flag, deptname, supplier, curr_liefnr, p_222, p_234, p_266, pos, t_amount, currency_add_first, currency_screen_value, msg_str, p_1093, p_464, p_220, docunr, t_waehrung_data, t_l_order_data, t_l_orderhdr_data, t_parameters_data, lvcarea, l_order, l_orderhdr, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal docu_nr, pvilanguage, lief_nr, pr_deptnr, po_type, potype, bediener_username, ordername_screen_value, crterm


        nonlocal t_parameters, t_waehrung, t_l_order, t_l_orderhdr
        nonlocal t_parameters_data, t_waehrung_data, t_l_order_data, t_l_orderhdr_data

        return {"local_nr": local_nr, "billdate": billdate, "zeroprice_flag": zeroprice_flag, "deptname": deptname, "supplier": supplier, 
                "curr_liefnr": curr_liefnr, "p_222": p_222, "p_234": p_234, "p_266": p_266, 
                "pos": pos, "t_amount": t_amount, "currency_add_first": currency_add_first, 
                "currency_screen_value": currency_screen_value, "msg_str": msg_str, 
                "p_1093": p_1093, "p_464": p_464, "p_220": p_220, "docunr": docunr, 
                "t-waehrung": t_waehrung_data, "t-l-order": t_l_order_data, "t-l-orderhdr": t_l_orderhdr_data, "t-parameters": t_parameters_data}

    def new_po_number():

        nonlocal local_nr, billdate, zeroprice_flag, deptname, supplier, curr_liefnr, p_222, p_234, p_266, pos, t_amount, currency_add_first, currency_screen_value, msg_str, p_1093, p_464, p_220, docunr, t_waehrung_data, t_l_order_data, t_l_orderhdr_data, t_parameters_data, lvcarea, l_order, l_orderhdr, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal docu_nr, pvilanguage, lief_nr, pr_deptnr, po_type, potype, bediener_username, ordername_screen_value, crterm


        nonlocal t_parameters, t_waehrung, t_l_order, t_l_orderhdr
        nonlocal t_parameters_data, t_waehrung_data, t_l_order_data, t_l_orderhdr_data

        docunr = ""
        l_orderhdr1 = None
        l_orderhdr2 = None
        s:string = ""
        i:int = 1
        mm:int = 0
        yy:int = 0

        def generate_inner_output():
            return (docunr)

        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)
        L_orderhdr2 =  create_buffer("L_orderhdr2",L_orderhdr)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 973)]})

        if htparam.paramgruppe == 21 and htparam.flogical:
            mm = get_month(billdate)
            yy = get_year(billdate)
            s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")
            pass

            for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                     (get_month(L_orderhdr1.bestelldatum) == mm) & (get_year(L_orderhdr1.bestelldatum) == yy) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
                i = to_int(substring(l_orderhdr1.docu_nr, 5, 5))
                i = i + 1
                docunr = s + to_string(i, "99999")

                l_orderhdr2 = db_session.query(L_orderhdr2).filter(
                         (get_month(L_orderhdr2.bestelldatum) == mm) & (get_year(L_orderhdr2.bestelldatum) == yy) & (L_orderhdr2.betriebsnr <= 1) & (L_orderhdr2.docu_nr == (docunr).lower())).first()

                if l_orderhdr2:
                    i = to_int(substring(l_orderhdr2.docu_nr, 5, 5))
                    i = i + 1
                    docunr = s + to_string(i, "99999")

                return generate_inner_output()
            docunr = s + to_string(i, "99999")

            return generate_inner_output()
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")
        pass

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                 (L_orderhdr1.bestelldatum == billdate) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docunr = s + to_string(i, "999")

            l_orderhdr2 = db_session.query(L_orderhdr2).filter(
                     (L_orderhdr2.docu_nr == (docunr).lower())).first()

            if l_orderhdr2:
                i = to_int(substring(l_orderhdr2.docu_nr, 7, 3))
                i = i + 1
                docunr = s + to_string(i, "999")

            return generate_inner_output()
        docunr = s + to_string(i, "999")

        return generate_inner_output()


    def currency_list():

        nonlocal local_nr, billdate, zeroprice_flag, deptname, supplier, curr_liefnr, p_222, p_234, p_266, pos, t_amount, currency_add_first, currency_screen_value, msg_str, p_1093, p_464, p_220, docunr, t_waehrung_data, t_l_order_data, t_l_orderhdr_data, t_parameters_data, lvcarea, l_order, l_orderhdr, htparam, waehrung, l_lieferant, parameters, l_artikel
        nonlocal docu_nr, pvilanguage, lief_nr, pr_deptnr, po_type, potype, bediener_username, ordername_screen_value, crterm


        nonlocal t_parameters, t_waehrung, t_l_order, t_l_orderhdr
        nonlocal t_parameters_data, t_waehrung_data, t_l_order_data, t_l_orderhdr_data

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, local_nr)]})
        currency_add_first = waehrung.wabkurz
        currency_screen_value = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr != local_nr) & (Waehrung.ankauf > 0) & (Waehrung.betriebsnr != 0)).order_by(Waehrung.wabkurz).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz
            t_waehrung.waehrungsnr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    local_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

    if htparam.finteger != 1 and htparam.finteger != 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 776)]})
    zeroprice_flag = htparam.flogical

    if docu_nr == "":
        docunr = new_po_number()
    else:
        docunr = docu_nr
    currency_list()

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    p_1093 = get_output(htpint(1093))
    p_464 = get_output(htpint(464))
    p_220 = get_output(htpint(220))

    if po_type == 1:

        l_orderhdr = get_cache (L_orderhdr, {"lief_nr": [(eq, lief_nr)],"docu_nr": [(eq, docunr)]})

        if not l_orderhdr:
            l_orderhdr = L_orderhdr()
            db_session.add(l_orderhdr)

            l_orderhdr.lief_nr = lief_nr
            l_orderhdr.docu_nr = docunr


        l_orderhdr.angebot_lief[0] = pr_deptnr
        l_orderhdr.bestelldatum = billdate
        l_orderhdr.lieferdatum = billdate + timedelta(days=1)
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
                         (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == l_orderhdr.angebot_lief[0])).first()

        if parameters:
            deptname = parameters.vstring
        pass
        pass

    l_orderhdr = get_cache (L_orderhdr, {"lief_nr": [(eq, lief_nr)],"docu_nr": [(eq, docunr)]})
    if l_orderhdr is None:
        return generate_output()
    
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_data.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid


    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    curr_liefnr = lief_nr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    p_222 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 234)]})
    p_234 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 266)]})
    p_266 =  to_decimal(htparam.fdecimal)
    pos = 0
    t_amount =  to_decimal("0")

    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == (docunr).lower()) & (L_order.pos > 0)).order_by(L_order._recid).all():
        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})
        t_l_order.a_bezeich = l_artikel.bezeich

        if l_order.lief_nr == lief_nr and l_order.loeschflag == 0 and docunr != "":
            pos = pos + 1

            if length(l_order.quality) >= 5:
                t_l_order.disc = to_int(substring(l_order.quality, 0, 2)) + to_int(substring(l_order.quality, 3, 2)) / 100

            if length(l_order.quality) >= 11:
                t_l_order.vat = to_int(substring(l_order.quality, 6, 2)) + to_int(substring(l_order.quality, 9, 2)) / 100

            if length(l_order.quality) >= 17:
                t_l_order.disc2 = to_int(substring(l_order.quality, 12, 2)) + to_int(substring(l_order.quality, 15, 2)) / 100
            t_l_order.price0 =  to_decimal(l_order.einzelpreis) / to_decimal((1) - to_decimal(t_l_order.disc) * to_decimal(0.01)) / to_decimal((1) - to_decimal(t_l_order.disc2) * to_decimal(0.01)) / to_decimal((1) + to_decimal(t_l_order.vat) * to_decimal(0.01))
            t_l_order.brutto =  to_decimal(t_l_order.price0) * to_decimal(l_order.anzahl)
            t_amount =  to_decimal(t_amount) + to_decimal(l_order.warenwert)

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    return generate_output()