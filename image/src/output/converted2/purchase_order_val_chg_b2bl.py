#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_order

def purchase_order_val_chg_b2bl(q2_list_docu_nr:string):

    prepare_cache ([L_artikel, L_order])

    q1_list_list = []
    l_artikel = l_order = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rec_id_l_order":int, "lief_nr":int, "docu_nr":string, "pos":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "geliefert":Decimal, "angebot_lief_1":int, "rechnungswert":Decimal, "lief_fax_3":string, "txtnr":int, "lieferdatum_eff":date, "einzelpreis":Decimal, "lief_fax_2":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, l_artikel, l_order
        nonlocal q2_list_docu_nr


        nonlocal q1_list
        nonlocal q1_list_list

        return {"q1-list": q1_list_list}

    l_order_obj_list = {}
    l_order = L_order()
    l_artikel = L_artikel()
    for l_order._recid, l_order.lief_nr, l_order.docu_nr, l_order.pos, l_order.artnr, l_order.anzahl, l_order.geliefert, l_order.angebot_lief, l_order.rechnungswert, l_order.lief_fax, l_order.txtnr, l_order.lieferdatum_eff, l_order.einzelpreis, l_artikel.bezeich, l_artikel._recid in db_session.query(L_order._recid, L_order.lief_nr, L_order.docu_nr, L_order.pos, L_order.artnr, L_order.anzahl, L_order.geliefert, L_order.angebot_lief, L_order.rechnungswert, L_order.lief_fax, L_order.txtnr, L_order.lieferdatum_eff, L_order.einzelpreis, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
             (L_order.docu_nr == (q2_list_docu_nr).lower()) & (L_order.pos > 0) & (L_order.loeschflag == 0)).order_by(L_order.pos).all():
        if l_order_obj_list.get(l_order._recid):
            continue
        else:
            l_order_obj_list[l_order._recid] = True


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.rec_id_l_order = l_order._recid
        q1_list.lief_nr = l_order.lief_nr
        q1_list.docu_nr = l_order.docu_nr
        q1_list.pos = l_order.pos
        q1_list.artnr = l_order.artnr
        q1_list.bezeich = l_artikel.bezeich
        q1_list.anzahl =  to_decimal(l_order.anzahl)
        q1_list.geliefert =  to_decimal(l_order.geliefert)
        q1_list.angebot_lief_1 = l_order.angebot_lief[0]
        q1_list.rechnungswert =  to_decimal(l_order.rechnungswert)
        q1_list.lief_fax_3 = l_order.lief_fax[2]
        q1_list.txtnr = l_order.txtnr
        q1_list.lieferdatum_eff = l_order.lieferdatum_eff
        q1_list.einzelpreis =  to_decimal(l_order.einzelpreis)
        q1_list.lief_fax_2 = l_order.lief_fax[1]

    return generate_output()