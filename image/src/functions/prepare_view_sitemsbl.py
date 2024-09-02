from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Htparam, L_artikel, L_order, L_orderhdr

def prepare_view_sitemsbl(user_init:str, docu_nr:str):
    show_price = None
    comments = ""
    sitem_list_list = []
    bediener = htparam = l_artikel = l_order = l_orderhdr = None

    sitem_list = None

    sitem_list_list, Sitem_list = create_model("Sitem_list", {"artnr":int, "bezeich":str, "lief_fax":[str], "txtnr":int, "anzahl":decimal, "geliefert":decimal, "einzelpreis":decimal, "warenwert":decimal, "lieferdatum_eff":date, "angebot_lief":[int], "masseinheit":str, "jahrgang":int, "quality":str, "pos":int, "remark":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, comments, sitem_list_list, bediener, htparam, l_artikel, l_order, l_orderhdr


        nonlocal sitem_list
        nonlocal sitem_list_list
        return {"show_price": show_price, "comments": comments, "sitem-list": sitem_list_list}

    def assign_it():

        nonlocal show_price, comments, sitem_list_list, bediener, htparam, l_artikel, l_order, l_orderhdr


        nonlocal sitem_list
        nonlocal sitem_list_list


        sitem_list = Sitem_list()
        sitem_list_list.append(sitem_list)

        sitem_list.artnr = l_order.artnr
        sitem_list.bezeich = l_artikel.bezeich
        sitem_list.lief_fax[2] = l_order.lief_fax[2]
        sitem_list.txtnr = l_order.txtnr
        sitem_list.anzahl = l_order.anzahl
        sitem_list.geliefert = l_order.geliefert
        sitem_list.einzelpreis = l_order.einzelpreis
        sitem_list.warenwert = l_order.warenwert
        sitem_list.lieferdatum_eff = l_order.lieferdatum_eff
        sitem_list.angebot_lief[0] = l_order.angebot_lief[0]
        sitem_list.masseinheit = l_artikel.masseinheit
        sitem_list.lief_fax[1] = l_order.lief_fax[1]
        sitem_list.jahrgang = l_artikel.jahrgang
        sitem_list.quality = l_order.quality
        sitem_list.pos = l_order.pos
        sitem_list.remark = l_order.besteller

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    if show_price:

        l_order_obj_list = []
        for l_order, l_artikel in db_session.query(L_order, L_artikel).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
            if l_order._recid in l_order_obj_list:
                continue
            else:
                l_order_obj_list.append(l_order._recid)


            assign_it()

    else:

        l_order_obj_list = []
        for l_order, l_artikel in db_session.query(L_order, L_artikel).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
            if l_order._recid in l_order_obj_list:
                continue
            else:
                l_order_obj_list.append(l_order._recid)


            assign_it()


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()

    if l_orderhdr:
        comments = l_orderhdr.lief_fax[2]

    return generate_output()