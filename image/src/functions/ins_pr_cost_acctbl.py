from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Bediener, L_order

def ins_pr_cost_acctbl(user_init:str, pos:int, s_artnr:int, bemerkung:str, docu_nr:str, qty:decimal, delivery:date, bestelldatum:date, traubensort:str, cost_acct:str, lief_einheit:decimal):
    ins_list_list = []
    price0:decimal = 0
    int_costacct:int = None
    l_artikel = bediener = l_order = None

    s_list = ins_list = l_art = None

    s_list_list, S_list = create_model("S_list", {"pos":int, "artnr":int, "new_created":bool, "bemerk":str})
    ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":str, "anzahl":decimal, "traubensort":str, "txtnr":int, "lieferdatum":date, "stornogrund":str, "bemerk":str, "quality":str, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":str, "bestelldatum":date})

    L_art = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ins_list_list, price0, int_costacct, l_artikel, bediener, l_order
        nonlocal l_art


        nonlocal s_list, ins_list, l_art
        nonlocal s_list_list, ins_list_list
        return {"ins-list": ins_list_list}

    def create_list():

        nonlocal ins_list_list, price0, int_costacct, l_artikel, bediener, l_order
        nonlocal l_art


        nonlocal s_list, ins_list, l_art
        nonlocal s_list_list, ins_list_list

        for l_order in db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.loeschflag <= 1)).all():
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.artnr = l_order.artnr
            s_list.pos = l_order.pos
            s_list.bemerk = l_order.besteller
            pos = l_order.pos

    create_list()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    pos = pos + 1
    s_list = S_list()
    s_list_list.append(s_list)

    s_list.artnr = s_artnr
    s_list.new_created = True
    s_list.pos = pos
    s_list.bemerk = bemerkung


    l_order = L_order()
    db_session.add(l_order)

    l_order.docu_nr = docu_nr
    l_order.artnr = s_artnr
    l_order.anzahl = qty
    l_order.lieferdatum = delivery
    l_order.pos = pos
    l_order.bestelldatum = bestelldatum
    l_order.op_art = 1
    l_order.lief_fax[0] = bediener.username
    l_order.lief_fax[2] = traubensort
    l_order.flag = True
    l_order.besteller = bemerkung


    int_costacct = to_int(cost_acct)

    if int_costacct != 0:
        l_order.stornogrund = cost_acct

    if lief_einheit != 0:
        l_order.txtnr = lief_einheit


    l_order_obj_list = []
    for l_order, l_art, s_list in db_session.query(L_order, L_art, S_list).join(L_art,(L_art.artnr == L_order.artnr)).join(S_list,(S_list.artnr == L_order.artnr)).filter(
            (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos > 0) &  (L_order.lief_nr == 0) &  (L_order.loeschflag <= 1)).all():
        if l_order._recid in l_order_obj_list:
            continue
        else:
            l_order_obj_list.append(l_order._recid)


        ins_list = Ins_list()
        ins_list_list.append(ins_list)

        ins_list.t_recid = l_order._recid
        ins_list.artnr = l_order.artnr
        ins_list.bezeich = l_art.bezeich
        ins_list.anzahl = l_order.anzahl
        ins_list.traubensort = l_art.traubensort
        ins_list.txtnr = l_order.txtnr
        ins_list.lieferdatum = l_order.lieferdatum
        ins_list.stornogrund = l_order.stornogrund
        ins_list.bemerk = s_list.bemerk
        ins_list.quality = l_order.quality
        ins_list.jahrgang = l_art.jahrgang
        ins_list.new_created = s_list.new_created
        ins_list.lief_nr = l_order.lief_nr
        ins_list.op_art = l_order.op_art
        ins_list.docu_nr = l_order.docu_nr
        ins_list.bestelldatum = l_order.bestelldatum

    return generate_output()