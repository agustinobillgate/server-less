#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Bediener, L_order

def ins_pr_cost_acctbl(user_init:string, pos:int, s_artnr:int, bemerkung:string, docu_nr:string, qty:Decimal, delivery:date, bestelldatum:date, traubensort:string, cost_acct:string, lief_einheit:Decimal):

    prepare_cache ([L_artikel, Bediener, L_order])

    ins_list_list = []
    price0:Decimal = to_decimal("0.0")
    int_costacct:int = None
    l_artikel = bediener = l_order = None

    s_list = ins_list = l_art = None

    s_list_list, S_list = create_model("S_list", {"pos":int, "artnr":int, "new_created":bool, "bemerk":string})
    ins_list_list, Ins_list = create_model("Ins_list", {"t_recid":int, "artnr":int, "bezeich":string, "anzahl":Decimal, "traubensort":string, "txtnr":int, "lieferdatum":date, "stornogrund":string, "bemerk":string, "quality":string, "jahrgang":int, "new_created":bool, "lief_nr":int, "op_art":int, "docu_nr":string, "bestelldatum":date})

    L_art = create_buffer("L_art",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ins_list_list, price0, int_costacct, l_artikel, bediener, l_order
        nonlocal user_init, pos, s_artnr, bemerkung, docu_nr, qty, delivery, bestelldatum, traubensort, cost_acct, lief_einheit
        nonlocal l_art


        nonlocal s_list, ins_list, l_art
        nonlocal s_list_list, ins_list_list

        return {"ins-list": ins_list_list}

    def create_list():

        nonlocal ins_list_list, price0, int_costacct, l_artikel, bediener, l_order
        nonlocal user_init, pos, s_artnr, bemerkung, docu_nr, qty, delivery, bestelldatum, traubensort, cost_acct, lief_einheit
        nonlocal l_art


        nonlocal s_list, ins_list, l_art
        nonlocal s_list_list, ins_list_list

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag <= 1)).order_by(L_order.pos).all():
            s_list = S_list()
            s_list_list.append(s_list)

            s_list.artnr = l_order.artnr
            s_list.pos = l_order.pos
            s_list.bemerk = l_order.besteller
            pos = l_order.pos


    create_list()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
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
    l_order.anzahl =  to_decimal(qty)
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
    pass

    l_order_obj_list = {}
    for l_order, l_art in db_session.query(L_order, L_art).join(L_art,(L_art.artnr == L_order.artnr)).filter(
             (L_order.docu_nr == (docu_nr).lower()) & (L_order.pos > 0) & (L_order.lief_nr == 0) & (L_order.loeschflag <= 1)).order_by(s_list.pos.desc()).all():
        s_list = query(s_list_list, (lambda s_list: s_list.artnr == l_order.artnr), first=True)
        if not s_list:
            continue

        if l_order_obj_list.get(l_order._recid):
            continue
        else:
            l_order_obj_list[l_order._recid] = True


        ins_list = Ins_list()
        ins_list_list.append(ins_list)

        ins_list.t_recid = l_order._recid
        ins_list.artnr = l_order.artnr
        ins_list.bezeich = l_art.bezeich
        ins_list.anzahl =  to_decimal(l_order.anzahl)
        ins_list.traubensort = l_art.traubensorte
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