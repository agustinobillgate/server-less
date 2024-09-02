from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_lieferant, L_orderhdr, Htparam, Waehrung

def pchase_stockin_disp_itbl(sorttype:int, ponum:str, supplier:str, to_supp:str, order_date:date):
    q2_list_list = []
    l_order = l_lieferant = l_orderhdr = htparam = waehrung = None

    w_list = l_order1 = q2_list = None

    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":str})
    q2_list_list, Q2_list = create_model("Q2_list", {"lief_nr":int, "lief_fax_1":[str], "docu_nr":str, "firma":str, "bestelldatum":date, "lieferdatum":date, "wabkurz":str, "bestellart":str, "lief_fax_3":str, "besteller":str, "lief_fax_2":[str], "betriebsnr":int, "gedruckt":date})

    L_order1 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_list, l_order, l_lieferant, l_orderhdr, htparam, waehrung
        nonlocal l_order1


        nonlocal w_list, l_order1, q2_list
        nonlocal w_list_list, q2_list_list
        return {"q2-list": q2_list_list}

    def currency_list():

        nonlocal q2_list_list, l_order, l_lieferant, l_orderhdr, htparam, waehrung
        nonlocal l_order1


        nonlocal w_list, l_order1, q2_list
        nonlocal w_list_list, q2_list_list

        local_nr:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 152)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            local_nr = waehrungsnr
        w_list = W_list()
        w_list_list.append(w_list)


        if local_nr != 0:
            w_list.wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).all():
            w_list = W_list()
            w_list_list.append(w_list)

            w_list.nr = waehrungsnr
            w_list.wabkurz = waehrung.wabkurz

    def assign_it():

        nonlocal q2_list_list, l_order, l_lieferant, l_orderhdr, htparam, waehrung
        nonlocal l_order1


        nonlocal w_list, l_order1, q2_list
        nonlocal w_list_list, q2_list_list


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.lief_nr = l_orderhdr.lief_nr
        q2_list.lief_fax_1 = l_order1.lief_fax[0]
        q2_list.docu_nr = l_orderhdr.docu_nr
        q2_list.firma = l_lieferant.firma
        q2_list.bestelldatum = l_orderhdr.bestelldatum
        q2_list.lieferdatum = l_orderhdr.lieferdatum
        q2_list.wabkurz = w_list.wabkurz
        q2_list.bestellart = l_orderhdr.bestellart
        q2_list.lief_fax_3 = l_orderhdr.lief_fax[2]
        q2_list.besteller = l_orderhdr.besteller
        q2_list.lief_fax_2 = l_order1.lief_fax[1]
        q2_list.betriebsnr = l_orderhdr.betriebsnr
        q2_list.gedruckt = l_orderhdr.gedruckt

    currency_list()

    if sorttype == 1:

        l_orderhdr_obj_list = []
        for l_orderhdr, w_list, l_lieferant, l_order1 in db_session.query(L_orderhdr, W_list, L_lieferant, L_order1).join(W_list,(W_list.nr == L_orderhdr.angebot_lief[2])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (supplier).lower()) &  (func.lower(L_lieferant.firma) <= (to_supp).lower())).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                (L_orderhdr.betriebsnr <= 1) &  (func.lower(L_orderhdr.docu_nr) >= (ponum).lower())).all():
            if l_orderhdr._recid in l_orderhdr_obj_list:
                continue
            else:
                l_orderhdr_obj_list.append(l_orderhdr._recid)


            assign_it()

    else:

        l_orderhdr_obj_list = []
        for l_orderhdr, w_list, l_lieferant, l_order1 in db_session.query(L_orderhdr, W_list, L_lieferant, L_order1).join(W_list,(W_list.nr == L_orderhdr.angebot_lief[2])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr)).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
                (L_orderhdr.bestelldatum == order_date) &  (L_orderhdr.betriebsnr <= 1) &  (func.lower(L_orderhdr.docu_nr) >= (ponum).lower())).all():
            if l_orderhdr._recid in l_orderhdr_obj_list:
                continue
            else:
                l_orderhdr_obj_list.append(l_orderhdr._recid)


            assign_it()


    return generate_output()