from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, Bediener, L_ophdr

def s_storerequest_btn_gobl(op_list:[Op_list], recid_l_ophdr:int, transdate:date, curr_lager:int, transfered:bool, cost_acct:str, deptno:int, to_stock:int, lscheinnr:str, user_init:str):
    s_artnr = 0
    qty = 0
    price = 0
    created = False
    curr_pos:int = 0
    zeit:int = 0
    amount:decimal = 0
    t_amount:decimal = 0
    l_op = bediener = l_ophdr = None

    op_list = l_op1 = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "acct_bez":str, "masseinheit":str})

    L_op1 = L_op

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, qty, price, created, curr_pos, zeit, amount, t_amount, l_op, bediener, l_ophdr
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list
        return {"s_artnr": s_artnr, "qty": qty, "price": price, "created": created}

    def l_op_pos():

        nonlocal s_artnr, qty, price, created, curr_pos, zeit, amount, t_amount, l_op, bediener, l_ophdr
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list

        pos = 0

        def generate_inner_output():
            return pos
        L_op1 = L_op

        for l_op1 in db_session.query(L_op1).filter(
                (func.lower(L_op1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (L_op1.loeschflag >= 0) &  (L_op1.pos > 0)).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1


        return generate_inner_output()

    def create_l_op(zeit:int):

        nonlocal s_artnr, qty, price, created, curr_pos, zeit, amount, t_amount, l_op, bediener, l_ophdr
        nonlocal l_op1


        nonlocal op_list, l_op1
        nonlocal op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        anz_oh:decimal = 0
        val_oh:decimal = 0
        anzahl = qty
        wert = qty * price
        amount = wert
        t_amount = t_amount + wert
        created = True


        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = zeit
        l_op.anzahl = anzahl
        l_op.einzelpreis = price
        l_op.warenwert = wert
        l_op.reorgflag = deptno

        if transfered:
            l_op.op_art = 14
        else:
            l_op.op_art = 13
        l_op.herkunftflag = 1
        l_op.lscheinnr = lscheinnr

        if not transfered:
            l_op.pos = curr_pos
            l_op.stornogrund = cost_acct


        else:
            l_op.pos = to_stock
        l_op.fuellflag = bediener.nr

        l_op = db_session.query(L_op).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == recid_l_ophdr)).first()

    l_ophdr = db_session.query(L_ophdr).first()
    l_ophdr.datum = transdate
    l_ophdr.lager_nr = curr_lager

    if not transfered:
        l_ophdr.fibukonto = cost_acct

    l_ophdr = db_session.query(L_ophdr).first()

    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()

    for op_list in query(op_list_list, filters=(lambda op_list :op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        curr_lager = op_list.lager_nr
        cost_acct = op_list.stornogrund
        create_l_op(zeit)
    op_list_list.clear()

    return generate_output()