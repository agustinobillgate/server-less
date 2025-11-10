#using conversion tools version: 1.0.0.119
#-----------------------------------------
# Rd, 17-July-25
# re download gitlab, 
# update if not available return
# l_order.txt -> l_order.txtnr
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import L_artikel, L_order, L_orderhdr, Waehrung, Htparam, L_lieferant, Queasy, Parameters

def safe_divide(numerator, denominator):
    numerator, denominator = to_decimal(numerator), to_decimal(denominator)
    return (numerator / denominator) if denominator not in (0, None) else to_decimal("0")


def prepare_chg_po_1bl(pvilanguage:int, docu_nr:string, lief_nr:int):

    prepare_cache ([Htparam, L_lieferant, Queasy, Parameters])

    local_nr = 0
    potype = 0
    enforce_rflag = False
    release_flag = False
    prev_flag = False
    pr = ""
    crterm = 30
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    curr_liefnr = 0
    deptnr = 0
    ordername = ""
    deptname = ""
    billdate = None
    t_amount = to_decimal("0.0")
    msg_str = ""
    p_1093 = 0
    p_464 = 0
    p_220 = 0
    p_266 = to_decimal("0.0")
    p_app = False
    t_l_art_data = []
    s_order_data = []
    disc_list_data = []
    t_l_orderhdr_data = []
    t_waehrung_data = []
    t_l_order_data = []
    t_parameters_data = []
    q245_data = []
    lvcarea:string = "chg-po"
    unit_price:Decimal = to_decimal("0.0")
    unit_vatvalue:Decimal = to_decimal("0.0")
    unit_disc1value:Decimal = to_decimal("0.0")
    unit_disc2value:Decimal = to_decimal("0.0")
    l_artikel = l_order = l_orderhdr = waehrung = htparam = l_lieferant = queasy = parameters = None

    disc_list = l_art = s_order = t_l_art = t_l_orderhdr = t_l_order = t_waehrung = t_parameters = q245 = None

    disc_list_data, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal, "disc_val":Decimal, "disc2_val":Decimal, "vat_val":Decimal})
    s_order_data, S_order = create_model_like(L_order, {"rec_id":int, "lief_einheit":Decimal, "addvat_value":Decimal, "amount":Decimal, "addvat_no":int})
    t_l_art_data, T_l_art = create_model_like(L_artikel)
    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int, "avail_addvat":bool})
    t_l_order_data, T_l_order = create_model_like(L_order, {"rec_id":int, "addvat_value":Decimal, "amount":Decimal, "addvat_no":int})
    t_waehrung_data, T_waehrung = create_model_like(Waehrung)
    t_parameters_data, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})
    q245_data, Q245 = create_model("Q245", {"key":int, "docu_nr":string, "user_init":string, "app_id":string, "app_no":int, "sign_id":int})

    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, potype, enforce_rflag, release_flag, prev_flag, pr, crterm, lieferdatum, bestellart, comments, supplier, curr_liefnr, deptnr, ordername, deptname, billdate, t_amount, msg_str, p_1093, p_464, p_220, p_266, p_app, t_l_art_data, s_order_data, disc_list_data, t_l_orderhdr_data, t_waehrung_data, t_l_order_data, t_parameters_data, q245_data, lvcarea, unit_price, unit_vatvalue, unit_disc1value, unit_disc2value, l_artikel, l_order, l_orderhdr, waehrung, htparam, l_lieferant, queasy, parameters
        nonlocal pvilanguage, docu_nr, lief_nr
        nonlocal l_art


        nonlocal disc_list, l_art, s_order, t_l_art, t_l_orderhdr, t_l_order, t_waehrung, t_parameters, q245
        nonlocal disc_list_data, s_order_data, t_l_art_data, t_l_orderhdr_data, t_l_order_data, t_waehrung_data, t_parameters_data, q245_data

        return {"local_nr": local_nr, "potype": potype, "enforce_rflag": enforce_rflag, "release_flag": release_flag, "prev_flag": prev_flag, "pr": pr, "crterm": crterm, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "curr_liefnr": curr_liefnr, "deptnr": deptnr, "ordername": ordername, "deptname": deptname, "billdate": billdate, "t_amount": t_amount, "msg_str": msg_str, "p_1093": p_1093, "p_464": p_464, "p_220": p_220, "p_266": p_266, "p_app": p_app, "t-l-art": t_l_art_data, "s-order": s_order_data, "disc-list": disc_list_data, "t-l-orderhdr": t_l_orderhdr_data, "t-waehrung": t_waehrung_data, "t-l-order": t_l_order_data, "t-parameters": t_parameters_data, "q245": q245_data}

    def cal_tamount():

        nonlocal local_nr, potype, enforce_rflag, release_flag, prev_flag, pr, crterm, lieferdatum, bestellart, comments, supplier, curr_liefnr, deptnr, ordername, deptname, billdate, t_amount, msg_str, p_1093, p_464, p_220, p_266, p_app, t_l_art_data, s_order_data, disc_list_data, t_l_orderhdr_data, t_waehrung_data, t_l_order_data, t_parameters_data, q245_data, lvcarea, unit_price, unit_vatvalue, unit_disc1value, unit_disc2value, l_artikel, l_order, l_orderhdr, waehrung, htparam, l_lieferant, queasy, parameters
        nonlocal pvilanguage, docu_nr, lief_nr
        nonlocal l_art


        nonlocal disc_list, l_art, s_order, t_l_art, t_l_orderhdr, t_l_order, t_waehrung, t_parameters, q245
        nonlocal disc_list_data, s_order_data, t_l_art_data, t_l_orderhdr_data, t_l_order_data, t_waehrung_data, t_parameters_data, q245_data


        t_amount =  to_decimal("0")

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.loeschflag == 0)).order_by(L_order._recid).all():
            t_amount =  to_decimal(t_amount) + to_decimal(l_order.warenwert)
            s_order = S_order()
            s_order_data.append(s_order)

            s_order.docu_nr = l_order.docu_nr
            s_order.artnr = l_order.artnr
            s_order.betriebsnr = l_order._recid
            s_order.lief_fax[2] = l_order.lief_fax[2]
            s_order.artnr = l_order.artnr
            s_order.geliefert =  to_decimal(l_order.geliefert)

            # Rd 4/9/2025
            # s_order.txtnr = l_order.txt
            s_order.txtnr = l_order.txtnr
            s_order.anzahl =  to_decimal(l_order.anzahl)
            s_order.flag = l_order.flag
            s_order.quality = l_order.quality
            s_order.besteller = l_order.besteller
            s_order.einzelpreis =  to_decimal(l_order.einzelpreis)
            s_order.warenwert =  to_decimal(l_order.warenwert)
            s_order.stornogrund = l_order.stornogrund
            s_order.pos = l_order.pos
            s_order.rec_id = l_order._recid

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_order.artnr)]})

            if l_artikel:
                s_order.lief_einheit =  to_decimal(l_artikel.lief_einheit)

            queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_order.docu_nr)],"number1": [(eq, l_order.artnr)]})

            if queasy:
                s_order.addvat_value =  to_decimal(queasy.deci1)
                s_order.addvat_no = queasy.number2
                s_order.amount =  to_decimal(s_order.amount) + to_decimal((l_order.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )


            else:
                s_order.amount =  to_decimal(s_order.amount) + to_decimal(l_order.warenwert)
            disc_list = Disc_list()
            disc_list_data.append(disc_list)

            disc_list.l_recid = s_order.rec_id

            if substring(substring(s_order.quality, 0, 2) , 1, 2) == (".").lower() :
                disc_list.disc = to_decimal(substring(s_order.quality, 0, 5))
                disc_list.vat = to_decimal(substring(s_order.quality, 5, 5))
                disc_list.disc2 = to_decimal(substring(s_order.quality, 10, 5))


            else:
                disc_list.disc = to_decimal(substring(s_order.quality, 0, 5))
                disc_list.vat = to_decimal(substring(s_order.quality, 6, 5))
                disc_list.disc2 = to_decimal(substring(s_order.quality, 11, 5))


            disc_list.disc_val = to_decimal(substring(s_order.quality, 18, 18))
            disc_list.disc2_val = to_decimal(substring(s_order.quality, 36, 18))
            disc_list.vat_val = to_decimal(substring(s_order.quality, 54, 18))


            disc_list.price0 = to_decimal(substring(s_order.quality, 72, 18))
            disc_list.brutto = to_decimal(substring(s_order.quality, 90, 18))
            
            # Rd, 4/9/2025
            # disc_list.price0 =  to_decimal(disc_list.brutto) / to_decimal(s_order.anzahl)
            disc_list.price0 =  safe_divide(disc_list.brutto, s_order.anzahl)

            if disc_list.price0 == None:
                disc_list.price0 =  to_decimal("0")

            if disc_list.price0 == 0 and disc_list.brutto == 0 and s_order.warenwert != 0 and s_order.anzahl != 0:
                unit_price =  safe_divide(to_decimal(s_order.warenwert), to_decimal(s_order.anzahl))
                unit_vatvalue =  safe_divide(to_decimal(disc_list.vat_val), to_decimal(s_order.anzahl))
                unit_disc1value =  to_decimal(disc_list.disc_val)
                unit_disc2value =  to_decimal(disc_list.disc2_val)
                disc_list.price0 =  to_decimal(unit_price) - to_decimal(unit_vatvalue)
                disc_list.price0 =  to_decimal(disc_list.price0) + to_decimal(disc_list.disc_val) + to_decimal(disc_list.disc2_val)

                if disc_list.price0 == None:
                    disc_list.price0 =  to_decimal("0")


                disc_list.brutto =  to_decimal(disc_list.price0) * to_decimal(s_order.anzahl)


    p_266 = get_output(htpint(266))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 71)]})

    if htparam.paramgruppe == 21:
        p_app = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    local_nr = waehrung.waehrungsnr

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
    # Rd, 17-July-25
    # if l_lieferant is None:
    #     return generate_output()
    if l_lieferant:
        tmp_l_lieferant_firma = l_lieferant.firma
        tmp_l_lieferant_wohnort = l_lieferant.wohnort
    else:
        tmp_l_lieferant_firma = None
        tmp_l_lieferant_wohnort = None
        
    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    if l_orderhdr:

        if l_orderhdr.betriebsnr == 1:
            potype = 2
        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_data.append(t_l_orderhdr)

        buffer_copy(l_orderhdr, t_l_orderhdr)
        t_l_orderhdr.rec_id = l_orderhdr._recid

        queasy = get_cache (Queasy, {"key": [(eq, 303)]})

        if queasy:
            t_l_orderhdr.avail_addvat = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
        enforce_rflag = htparam.flogical
        release_flag = (l_orderhdr.gedruckt != None)
        prev_flag = release_flag

        l_order = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"lief_nr": [(eq, lief_nr)],"pos": [(eq, 0)]})
        # Rd, 17-July-25
        # if l_order is None:
        #     return generate_output()
        if l_order:
            tmp_pr = l_order.lief_fax[0]
        else:
            tmp_pr = None
        
        pr = tmp_pr
        crterm = l_orderhdr.angebot_lief[1]
        lieferdatum = l_orderhdr.lieferdatum
        bestellart = l_orderhdr.bestellart
        comments = l_orderhdr.lief_fax[2]
        if tmp_l_lieferant_firma == None or tmp_l_lieferant_wohnort == None:
            supplier = None
        else:
            supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
        curr_liefnr = lief_nr
        deptnr = l_orderhdr.angebot_lief[0]
        ordername = l_orderhdr.lief_fax[1]


        t_l_order = T_l_order()
        t_l_order_data.append(t_l_order)

        buffer_copy(l_order, t_l_order)
        t_l_order.rec_id = l_order._recid
        t_l_order.amount =  to_decimal(l_order.warenwert)

        queasy = get_cache (Queasy, {"key": [(eq, 304)],"char1": [(eq, l_order.docu_nr)],"number1": [(eq, l_order.artnr)]})

        if queasy:
            t_l_order.addvat_value =  to_decimal(queasy.deci1)
            t_l_order.addvat_no = queasy.number2
            t_l_order.amount =  to_decimal(t_l_order.amount) + to_decimal((l_order.warenwert) * to_decimal((queasy.deci1) / to_decimal(100)) )

        if deptnr > 0:

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptnr)).first()
            deptname = parameters.vstring

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if htparam.finteger != 1 and htparam.finteger != 2:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
            billdate = htparam.fdate
        else:
            billdate = get_current_date()
        cal_tamount()

        for s_order in query(s_order_data):

            l_art = db_session.query(L_art).filter(
                     (L_art.artnr == s_order.artnr)).first()

            if l_art:

                t_l_art = query(t_l_art_data, filters=(lambda t_l_art: t_l_art.artnr == l_art.artnr), first=True)

                if not t_l_art:
                    t_l_art = T_l_art()
                    t_l_art_data.append(t_l_art)

                    buffer_copy(l_art, t_l_art)

        for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
            t_parameters = T_parameters()
            t_parameters_data.append(t_parameters)

            t_parameters.varname = parameters.varname
            t_parameters.vstring = parameters.vstring


        p_1093 = get_output(htpint(1093))
        p_464 = get_output(htpint(464))
        p_220 = get_output(htpint(220))

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 245) & (Queasy.char1 == (docu_nr).lower())).order_by(Queasy.number1).all():
            q245 = Q245()
            q245_data.append(q245)

            q245.key = queasy.key
            q245.docu_nr = queasy.char1
            q245.user_init = queasy.char2
            q245.app_id = queasy.char3
            q245.app_no = queasy.number1
            q245.sign_id = queasy.number2

    return generate_output()