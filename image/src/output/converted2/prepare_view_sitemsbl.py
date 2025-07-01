#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Htparam, L_artikel, L_order, L_orderhdr

def prepare_view_sitemsbl(user_init:string, docu_nr:string):

    prepare_cache ([Bediener, Htparam, L_artikel, L_order, L_orderhdr])

    show_price = None
    comments = ""
    sitem_list_list = []
    bediener = htparam = l_artikel = l_order = l_orderhdr = None

    sitem_list = None

    sitem_list_list, Sitem_list = create_model("Sitem_list", {"artnr":int, "bezeich":string, "lief_fax":[string,3], "txtnr":int, "anzahl":Decimal, "geliefert":Decimal, "einzelpreis":Decimal, "warenwert":Decimal, "lieferdatum_eff":date, "angebot_lief":[int,3], "masseinheit":string, "jahrgang":int, "quality":string, "pos":int, "remark":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, comments, sitem_list_list, bediener, htparam, l_artikel, l_order, l_orderhdr
        nonlocal user_init, docu_nr


        nonlocal sitem_list
        nonlocal sitem_list_list

        return {"show_price": show_price, "comments": comments, "sitem-list": sitem_list_list}

    def assign_it():

        nonlocal show_price, comments, sitem_list_list, bediener, htparam, l_artikel, l_order, l_orderhdr
        nonlocal user_init, docu_nr


        nonlocal sitem_list
        nonlocal sitem_list_list


        sitem_list = Sitem_list()
        sitem_list_list.append(sitem_list)

        sitem_list.artnr = l_order.artnr
        sitem_list.bezeich = l_artikel.bezeich
        sitem_list.lief_fax[2] = l_order.lief_fax[2]
        sitem_list.txtnr = l_order.txtnr
        sitem_list.anzahl =  to_decimal(l_order.anzahl)
        sitem_list.geliefert =  to_decimal(l_order.geliefert)
        sitem_list.einzelpreis =  to_decimal(l_order.einzelpreis)
        sitem_list.warenwert =  to_decimal(l_order.warenwert)
        sitem_list.lieferdatum_eff = l_order.lieferdatum_eff
        sitem_list.angebot_lief[0] = l_order.angebot_lief[0]
        sitem_list.masseinheit = l_artikel.masseinheit
        sitem_list.lief_fax[1] = l_order.lief_fax[1]
        sitem_list.jahrgang = l_artikel.jahrgang
        sitem_list.quality = l_order.quality
        sitem_list.pos = l_order.pos
        sitem_list.remark = l_order.besteller


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    if show_price:

        l_order_obj_list = {}
        l_order = L_order()
        l_artikel = L_artikel()
        for l_order.artnr, l_order.lief_fax, l_order.txtnr, l_order.anzahl, l_order.geliefert, l_order.einzelpreis, l_order.warenwert, l_order.lieferdatum_eff, l_order.angebot_lief, l_order.quality, l_order.pos, l_order.besteller, l_order._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.jahrgang, l_artikel._recid in db_session.query(L_order.artnr, L_order.lief_fax, L_order.txtnr, L_order.anzahl, L_order.geliefert, L_order.einzelpreis, L_order.warenwert, L_order.lieferdatum_eff, L_order.angebot_lief, L_order.quality, L_order.pos, L_order.besteller, L_order._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.jahrgang, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0)).order_by(L_order.pos).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            assign_it()

    else:

        l_order_obj_list = {}
        l_order = L_order()
        l_artikel = L_artikel()
        for l_order.artnr, l_order.lief_fax, l_order.txtnr, l_order.anzahl, l_order.geliefert, l_order.einzelpreis, l_order.warenwert, l_order.lieferdatum_eff, l_order.angebot_lief, l_order.quality, l_order.pos, l_order.besteller, l_order._recid, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.jahrgang, l_artikel._recid in db_session.query(L_order.artnr, L_order.lief_fax, L_order.txtnr, L_order.anzahl, L_order.geliefert, L_order.einzelpreis, L_order.warenwert, L_order.lieferdatum_eff, L_order.angebot_lief, L_order.quality, L_order.pos, L_order.besteller, L_order._recid, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.jahrgang, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0)).order_by(L_order.pos).all():
            if l_order_obj_list.get(l_order._recid):
                continue
            else:
                l_order_obj_list[l_order._recid] = True


            assign_it()


    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})

    if l_orderhdr:
        comments = l_orderhdr.lief_fax[2]

    return generate_output()