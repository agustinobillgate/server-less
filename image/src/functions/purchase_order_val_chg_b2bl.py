from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, L_order

def purchase_order_val_chg_b2bl(q2_list_docu_nr:str):
    q1_list_list = []
    l_artikel = l_order = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"rec_id_l_order":int, "lief_nr":int, "docu_nr":str, "pos":int, "artnr":int, "bezeich":str, "anzahl":decimal, "geliefert":decimal, "angebot_lief_1":int, "rechnungswert":decimal, "lief_fax_3":str, "txtnr":int, "lieferdatum_eff":date, "einzelpreis":decimal, "lief_fax_2":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, l_artikel, l_order


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    l_order_obj_list = []
    for l_order, l_artikel in db_session.query(L_order, L_artikel).join(L_artikel,(l_artikel.artnr == L_order.artnr)).filter(
            (func.lower(L_order.docu_nr) == (q2_list_docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.loeschflag == 0)).all():
        if l_order._recid in l_order_obj_list:
            continue
        else:
            l_order_obj_list.append(l_order._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.rec_id_l_order = l_order._recid
        q1_list.lief_nr = l_order.lief_nr
        q1_list.docu_nr = l_order.docu_nr
        q1_list.pos = l_order.pos
        q1_list.artnr = l_order.artnr
        q1_list.bezeich = l_artikel.bezeich
        q1_list.anzahl = l_order.anzahl
        q1_list.geliefert = l_order.geliefert
        q1_list.angebot_lief_1 = l_order.angebot_lief[0]
        q1_list.rechnungswert = l_order.rechnungswert
        q1_list.lief_fax_3 = l_order.lief_fax[2]
        q1_list.txtnr = l_order.txtnr
        q1_list.lieferdatum_eff = l_order.lieferdatum_eff
        q1_list.einzelpreis = l_order.einzelpreis
        q1_list.lief_fax_2 = l_order.lief_fax[1]

    return generate_output()