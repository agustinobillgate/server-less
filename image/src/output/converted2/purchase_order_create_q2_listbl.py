#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_orderhdr, Htparam, Waehrung

def purchase_order_create_q2_listbl(case_type:int, docu_nr:string, lief_nr:int):

    prepare_cache ([L_order, L_orderhdr, Htparam, Waehrung])

    q2_list_list = []
    l_order = l_orderhdr = htparam = waehrung = None

    l_order1 = w_list = q2_list = None

    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
    q2_list_list, Q2_list = create_model("Q2_list", {"lief_nr":int, "docu_nr":string, "bestelldatum":date, "lieferdatum":date, "wabkurz":string, "bestellart":string, "gedruckt":date, "besteller":string, "lief_fax_3":string, "lief_fax_2":string, "rechnungswert":Decimal, "rec_id":int})

    L_order1 = create_buffer("L_order1",L_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q2_list_list, l_order, l_orderhdr, htparam, waehrung
        nonlocal case_type, docu_nr, lief_nr
        nonlocal l_order1


        nonlocal l_order1, w_list, q2_list
        nonlocal w_list_list, q2_list_list

        return {"q2-list": q2_list_list}

    def currency_list():

        nonlocal q2_list_list, l_order, l_orderhdr, htparam, waehrung
        nonlocal case_type, docu_nr, lief_nr
        nonlocal l_order1


        nonlocal l_order1, w_list, q2_list
        nonlocal w_list_list, q2_list_list

        local_nr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            local_nr = waehrung.waehrungsnr
        w_list = W_list()
        w_list_list.append(w_list)


        if local_nr != 0:
            w_list.wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).order_by(Waehrung.wabkurz).all():
            w_list = W_list()
            w_list_list.append(w_list)

            w_list.nr = waehrung.waehrungsnr
            w_list.wabkurz = waehrung.wabkurz


    currency_list()

    l_orderhdr_obj_list = {}
    for l_orderhdr, l_order1 in db_session.query(L_orderhdr, L_order1).join(L_order1,(L_order1.docu_nr == L_orderhdr.docu_nr) & (L_order1.loeschflag == 0) & (L_order1.pos == 0)).filter(
             (L_orderhdr.lief_nr == lief_nr)).order_by(L_orderhdr.bestelldatum, L_orderhdr.docu_nr).all():
        w_list = query(w_list_list, (lambda w_list: w_list.nr == l_orderhdr.angebot_lief[2]), first=True)
        if not w_list:
            continue

        if l_orderhdr_obj_list.get(l_orderhdr._recid):
            continue
        else:
            l_orderhdr_obj_list[l_orderhdr._recid] = True


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
        q2_list.rechnungswert =  to_decimal(l_order1.rechnungswert)
        q2_list.rec_id = l_orderhdr._recid

    return generate_output()