from functions.additional_functions import *
import decimal
from datetime import date
from models import L_order, L_orderhdr, Htparam, Waehrung

def purchase_order_create_q2_listbl(case_type:int, docu_nr:str, lief_nr:int):
    q2_list_list = []
    l_order = l_orderhdr = htparam = waehrung = None

    l_order1 = w_list = q2_list = None

    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":str})
    q2_list_list, Q2_list = create_model("Q2_list", {"lief_nr":int, "docu_nr":str, "bestelldatum":date, "lieferdatum":date, "wabkurz":str, "bestellart":str, "gedruckt":date, "besteller":str, "lief_fax_3":str, "lief_fax_2":str, "rechnungswert":decimal, "rec_id":int})

    L_order1 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_list, l_order, l_orderhdr, htparam, waehrung
        nonlocal l_order1


        nonlocal l_order1, w_list, q2_list
        nonlocal w_list_list, q2_list_list
        return {"q2-list": q2_list_list}

    def currency_list():

        nonlocal q2_list_list, l_order, l_orderhdr, htparam, waehrung
        nonlocal l_order1


        nonlocal l_order1, w_list, q2_list
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

    currency_list()

    l_orderhdr_obj_list = []
    for l_orderhdr, w_list, l_order1 in db_session.query(L_orderhdr, W_list, L_order1).join(W_list,(W_list.nr == L_orderhdr.angebot_lief[2])).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) &  (L_order1.loeschflag == 0) &  (L_order1.pos == 0)).filter(
            (L_orderhdr.lief_nr == lief_nr)).all():
        if l_orderhdr._recid in l_orderhdr_obj_list:
            continue
        else:
            l_orderhdr_obj_list.append(l_orderhdr._recid)


        q2_list = Q2_list()
        q2_list_list.append(q2_list)

        q2_list.lief_nr = l_orderhdr.lief_nr
        q2_list.docu_nr = l_orderhdr.docu_nr
        q2_list.bestelldatum = l_orderhdr.bestelldatum
        q2_list.lieferdatum = l_orderhdr.lieferdatum
        q2_list.wabkurz = w_list.wabkurz
        q2_list.bestellart = l_orderhdr.bestellart
        q2_list.gedruckt = l_orderhdr.gedruckt
        q2_list.besteller = l_orderhdr.besteller
        q2_list.lief_fax_3 = l_orderhdr.lief_fax[2]
        q2_list.lief_fax_2 = l_order1.lief_fax[1]
        q2_list.rechnungswert = l_order1.rechnungswert
        q2_list.rec_id = l_orderhdr._recid

    return generate_output()