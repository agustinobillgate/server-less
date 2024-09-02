from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from models import L_artikel, L_order, L_orderhdr, Waehrung, Htparam, L_lieferant, Parameters, Queasy

def prepare_chg_po_1bl(pvilanguage:int, docu_nr:str, lief_nr:int):
    local_nr = 0
    potype = 0
    enforce_rflag = False
    release_flag = False
    prev_flag = False
    pr = ""
    crterm = 0
    lieferdatum = None
    bestellart = ""
    comments = ""
    supplier = ""
    curr_liefnr = 0
    deptnr = 0
    ordername = ""
    deptname = ""
    billdate = None
    t_amount = 0
    msg_str = ""
    p_1093 = 0
    p_464 = 0
    p_220 = 0
    p_266 = 0
    p_app = False
    t_l_art_list = []
    s_order_list = []
    disc_list_list = []
    t_l_orderhdr_list = []
    t_waehrung_list = []
    t_l_order_list = []
    t_parameters_list = []
    q245_list = []
    lvcarea:str = "chg_po"
    l_artikel = l_order = l_orderhdr = waehrung = htparam = l_lieferant = parameters = queasy = None

    disc_list = l_art = s_order = t_l_art = t_l_orderhdr = t_l_order = t_waehrung = t_parameters = q245 = None

    disc_list_list, Disc_list = create_model("Disc_list", {"l_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal, "disc_val":decimal, "disc2_val":decimal, "vat_val":decimal})
    s_order_list, S_order = create_model_like(L_order, {"rec_id":int, "lief_einheit":decimal})
    t_l_art_list, T_l_art = create_model_like(L_artikel)
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})
    t_l_order_list, T_l_order = create_model_like(L_order, {"rec_id":int})
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)
    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})
    q245_list, Q245 = create_model("Q245", {"key":int, "docu_nr":str, "user_init":str, "app_id":str, "app_no":int, "sign_id":int})

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal local_nr, potype, enforce_rflag, release_flag, prev_flag, pr, crterm, lieferdatum, bestellart, comments, supplier, curr_liefnr, deptnr, ordername, deptname, billdate, t_amount, msg_str, p_1093, p_464, p_220, p_266, p_app, t_l_art_list, s_order_list, disc_list_list, t_l_orderhdr_list, t_waehrung_list, t_l_order_list, t_parameters_list, q245_list, lvcarea, l_artikel, l_order, l_orderhdr, waehrung, htparam, l_lieferant, parameters, queasy
        nonlocal l_art


        nonlocal disc_list, l_art, s_order, t_l_art, t_l_orderhdr, t_l_order, t_waehrung, t_parameters, q245
        nonlocal disc_list_list, s_order_list, t_l_art_list, t_l_orderhdr_list, t_l_order_list, t_waehrung_list, t_parameters_list, q245_list
        return {"local_nr": local_nr, "potype": potype, "enforce_rflag": enforce_rflag, "release_flag": release_flag, "prev_flag": prev_flag, "pr": pr, "crterm": crterm, "lieferdatum": lieferdatum, "bestellart": bestellart, "comments": comments, "supplier": supplier, "curr_liefnr": curr_liefnr, "deptnr": deptnr, "ordername": ordername, "deptname": deptname, "billdate": billdate, "t_amount": t_amount, "msg_str": msg_str, "p_1093": p_1093, "p_464": p_464, "p_220": p_220, "p_266": p_266, "p_app": p_app, "t-l-art": t_l_art_list, "s-order": s_order_list, "disc-list": disc_list_list, "t-l-orderhdr": t_l_orderhdr_list, "t-waehrung": t_waehrung_list, "t-l-order": t_l_order_list, "t-parameters": t_parameters_list, "q245": q245_list}

    def cal_tamount():

        nonlocal local_nr, potype, enforce_rflag, release_flag, prev_flag, pr, crterm, lieferdatum, bestellart, comments, supplier, curr_liefnr, deptnr, ordername, deptname, billdate, t_amount, msg_str, p_1093, p_464, p_220, p_266, p_app, t_l_art_list, s_order_list, disc_list_list, t_l_orderhdr_list, t_waehrung_list, t_l_order_list, t_parameters_list, q245_list, lvcarea, l_artikel, l_order, l_orderhdr, waehrung, htparam, l_lieferant, parameters, queasy
        nonlocal l_art


        nonlocal disc_list, l_art, s_order, t_l_art, t_l_orderhdr, t_l_order, t_waehrung, t_parameters, q245
        nonlocal disc_list_list, s_order_list, t_l_art_list, t_l_orderhdr_list, t_l_order_list, t_waehrung_list, t_parameters_list, q245_list


        t_amount = 0

        l_order_obj_list = []
        for l_order, l_art in db_session.query(L_order, L_art).join(L_art,(L_art.artnr == L_order.artnr)).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
            if l_order._recid in l_order_obj_list:
                continue
            else:
                l_order_obj_list.append(l_order._recid)


            t_amount = t_amount + l_order.warenwert
            s_order = S_order()
            s_order_list.append(s_order)

            s_order.docu_nr = l_order.docu_nr
            s_order.betriebsnr = l_order._recid
            s_order.lief_fax[2] = l_order.lief_fax[2]
            s_order.artnr = l_order.artnr
            s_order.geliefert = l_order.geliefert
            s_order.txtnr = l_order.txt
            s_order.anzahl = l_order.anzahl
            s_order.flag = l_order.flag
            s_order.quality = l_order.quality
            s_order.besteller = l_order.besteller
            s_order.einzelpreis = l_order.einzelpreis
            s_order.warenwert = l_order.warenwert
            s_order.stornogrund = l_order.stornogrund
            s_order.pos = l_order.pos
            s_order.rec_id = l_order._recid

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_order.artnr)).first()
            s_order.lief_einheit = l_artikel.lief_einheit


            disc_list = Disc_list()
            disc_list_list.append(disc_list)

            disc_list.l_recid = s_order.rec_id
            disc_list.disc = to_int(substring(s_order.quality, 0, 2)) +\
                    to_int(substring(s_order.quality, 3, 2)) * 0.01
            disc_list.vat = to_int(substring(s_order.quality, 6, 2)) +\
                    to_int(substring(s_order.quality, 9, 2)) * 0.01
            disc_list.disc2 = to_int(substring(s_order.quality, 12, 2)) +\
                    to_int(substring(s_order.quality, 15, 2)) * 0.01
            disc_list.disc_val = to_int(substring(s_order.quality, 18, 18))
            disc_list.disc2_val = to_int(substring(s_order.quality, 36, 18))
            disc_list.vat_val = to_int(substring(s_order.quality, 54))


            disc_list.brutto = (s_order.warenwert + disc_list.disc_val + disc_list.disc2_val) - disc_list.vat_val
            disc_list.price0 = disc_list.brutto / s_order.anzahl

    p_266 = get_output(htpint(266))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 71)).first()

    if htparam.paramgruppe == 21:
        p_app = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if not waehrung:
        msg_str = msg_str + chr(2) + translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "")

        return generate_output()
    local_nr = waehrungsnr

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == lief_nr)).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if l_orderhdr.betriebsnr == 1:
        potype = 2
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical
    release_flag = (l_orderhdr.gedruckt != None)
    prev_flag = release_flag

    l_order = db_session.query(L_order).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.lief_nr == lief_nr) &  (L_order.pos == 0)).first()
    pr = l_order.lief_fax[0]
    crterm = l_orderhdr.angebot_lief[1]
    lieferdatum = l_orderhdr.lieferdatum
    bestellart = l_orderhdr.bestellart
    comments = l_orderhdr.lief_fax[2]
    supplier = l_lieferant.firma + " - " + l_lieferant.wohnort
    curr_liefnr = lief_nr
    deptnr = l_orderhdr.angebot_lief[0]
    ordername = l_orderhdr.lief_fax[1]


    t_l_order = T_l_order()
    t_l_order_list.append(t_l_order)

    buffer_copy(l_order, t_l_order)
    t_l_order.rec_id = l_order._recid

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

    for s_order in query(s_order_list):

        l_art = db_session.query(L_art).filter(
                (L_art.artnr == s_order.artnr)).first()

        if l_art:
            t_l_art = T_l_art()
            t_l_art_list.append(t_l_art)

            buffer_copy(l_art, t_l_art)

    for waehrung in db_session.query(Waehrung).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        buffer_copy(waehrung, t_waehrung)

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring


    p_1093 = get_output(htpint(1093))
    p_464 = get_output(htpint(464))
    p_220 = get_output(htpint(220))

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 245) &  (func.lower(Queasy.char1) == (docu_nr).lower())).all():
        q245 = Q245()
        q245_list.append(q245)

        q245.key = queasy.KEY
        q245.docu_nr = queasy.char1
        q245.user_init = queasy.char2
        q245.app_id = queasy.char3
        q245.app_no = queasy.number1
        q245.sign_id = queasy.number2

    return generate_output()