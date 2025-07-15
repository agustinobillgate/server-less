#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam, L_artikel, L_order, L_orderhdr

def view_detailpobl(docu_nr:string, user_init:string):

    prepare_cache ([Bediener, Htparam, L_artikel, L_order, L_orderhdr])

    show_price = False
    q1_list_data = []
    bediener = htparam = l_artikel = l_order = l_orderhdr = None

    q1_list = None

    q1_list_data, Q1_list = create_model("Q1_list", {"artnr":int, "pos":int, "bezeich":string, "geliefert":Decimal, "angebot_lief1":int, "masseinheit":string, "lief_fax3":string, "txtnr":int, "lieferdatum_eff":date, "anzahl":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "lief_fax2":string, "jahrgang":int, "comment":string, "curr_bez":string, "fg_col":int}, {"curr_bez": ""})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, q1_list_data, bediener, htparam, l_artikel, l_order, l_orderhdr
        nonlocal docu_nr, user_init


        nonlocal q1_list
        nonlocal q1_list_data

        return {"show_price": show_price, "q1-list": q1_list_data}

    def assign_it():

        nonlocal show_price, q1_list_data, bediener, htparam, l_artikel, l_order, l_orderhdr
        nonlocal docu_nr, user_init


        nonlocal q1_list
        nonlocal q1_list_data


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.artnr = l_order.artnr
        q1_list.pos = l_order.pos
        q1_list.bezeich = l_artikel.bezeich
        q1_list.geliefert =  to_decimal(l_order.geliefert)
        q1_list.angebot_lief1 = l_order.angebot_lief[0]
        q1_list.masseinheit = l_artikel.masseinheit
        q1_list.lief_fax3 = l_order.lief_fax[2]
        q1_list.txtnr = l_order.txtnr
        q1_list.lieferdatum_eff = l_order.lieferdatum_eff
        q1_list.anzahl =  to_decimal(l_order.anzahl)
        q1_list.einzelpreis =  to_decimal(l_order.einzelpreis)
        q1_list.warenwert =  to_decimal(l_order.warenwert)
        q1_list.lief_fax2 = l_order.lief_fax[1]
        q1_list.jahrgang = l_artikel.jahrgang

        l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)],"lief_nr": [(eq, l_order.lief_nr)]})

        if l_orderhdr:
            q1_list.comment = l_orderhdr.lief_fax[2]

        if l_artikel and l_artikel.jahrgang == 1 and l_order and length(l_order.quality) > 11:
            q1_list.fg_col = 12

        if l_artikel.jahrgang == 1:

            if length(l_order.quality) > 11:
                q1_list.curr_bez = substring(l_order.quality, 11, length(l_order.quality))


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    if show_price:

        l_order_obj_list = {}
        l_order = L_order()
        l_artikel = L_artikel()
        for l_order.artnr, l_order.pos, l_order.geliefert, l_order.angebot_lief, l_order.lief_fax, l_order.txtnr, l_order.lieferdatum_eff, l_order.anzahl, l_order.einzelpreis, l_order.warenwert, l_order.lief_nr, l_order.quality, l_order._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.jahrgang, l_artikel._recid in db_session.query(L_order.artnr, L_order.pos, L_order.geliefert, L_order.angebot_lief, L_order.lief_fax, L_order.txtnr, L_order.lieferdatum_eff, L_order.anzahl, L_order.einzelpreis, L_order.warenwert, L_order.lief_nr, L_order.quality, L_order._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.jahrgang, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag <= 1)).order_by(L_order.pos).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            assign_it()

    else:

        l_order_obj_list = {}
        l_order = L_order()
        l_artikel = L_artikel()
        for l_order.artnr, l_order.pos, l_order.geliefert, l_order.angebot_lief, l_order.lief_fax, l_order.txtnr, l_order.lieferdatum_eff, l_order.anzahl, l_order.einzelpreis, l_order.warenwert, l_order.lief_nr, l_order.quality, l_order._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.jahrgang, l_artikel._recid in db_session.query(L_order.artnr, L_order.pos, L_order.geliefert, L_order.angebot_lief, L_order.lief_fax, L_order.txtnr, L_order.lieferdatum_eff, L_order.anzahl, L_order.einzelpreis, L_order.warenwert, L_order.lief_nr, L_order.quality, L_order._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.jahrgang, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag <= 1)).order_by(L_order.pos).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            assign_it()


    return generate_output()