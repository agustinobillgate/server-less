#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, L_ophdr

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "acct_bez":string, "masseinheit":string})

def s_storerequest_btn_gobl(op_list_data:[Op_list], recid_l_ophdr:int, transdate:date, curr_lager:int, transfered:bool, cost_acct:string, deptno:int, to_stock:int, lscheinnr:string, user_init:string):

    prepare_cache ([L_op, Bediener, L_ophdr])

    s_artnr = 0
    qty = to_decimal("0.0")
    price = to_decimal("0.0")
    created = False
    curr_pos:int = 0
    zeit:int = 0
    amount:Decimal = to_decimal("0.0")
    t_amount:Decimal = to_decimal("0.0")
    l_op = bediener = l_ophdr = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_artnr, qty, price, created, curr_pos, zeit, amount, t_amount, l_op, bediener, l_ophdr
        nonlocal recid_l_ophdr, transdate, curr_lager, transfered, cost_acct, deptno, to_stock, lscheinnr, user_init


        nonlocal op_list

        return {"op-list": op_list_data, "s_artnr": s_artnr, "qty": qty, "price": price, "created": created}

    def l_op_pos():

        nonlocal s_artnr, qty, price, created, curr_pos, zeit, amount, t_amount, l_op, bediener, l_ophdr
        nonlocal recid_l_ophdr, transdate, curr_lager, transfered, cost_acct, deptno, to_stock, lscheinnr, user_init


        nonlocal op_list

        pos = 0
        l_op1 = None

        def generate_inner_output():
            return (pos)

        L_op1 =  create_buffer("L_op1",L_op)

        for l_op1 in db_session.query(L_op1).filter(
                 (L_op1.lscheinnr == (lscheinnr).lower()) & (L_op1.loeschflag >= 0) & (L_op1.pos > 0)).order_by(L_op1._recid).all():

            if l_op1.pos > pos:
                pos = l_op1.pos
        pos = pos + 1

        return generate_inner_output()


    def create_l_op(zeit:int):

        nonlocal s_artnr, qty, price, created, curr_pos, amount, t_amount, l_op, bediener, l_ophdr
        nonlocal recid_l_ophdr, transdate, curr_lager, transfered, cost_acct, deptno, to_stock, lscheinnr, user_init


        nonlocal op_list

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        anz_oh:Decimal = to_decimal("0.0")
        val_oh:Decimal = to_decimal("0.0")
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)
        created = True


        l_op = L_op()
        db_session.add(l_op)

        l_op.datum = transdate
        l_op.lager_nr = curr_lager
        l_op.artnr = s_artnr
        l_op.zeit = zeit
        l_op.anzahl =  to_decimal(anzahl)
        l_op.einzelpreis =  to_decimal(price)
        l_op.warenwert =  to_decimal(wert)
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
        pass


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, recid_l_ophdr)]})

    if l_ophdr:
        pass
        l_ophdr.datum = transdate
        l_ophdr.lager_nr = curr_lager

        if not transfered:
            l_ophdr.fibukonto = cost_acct
        pass
        pass
    curr_pos = l_op_pos()
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()

    for op_list in query(op_list_data, filters=(lambda op_list: op_list.anzahl != 0)):
        zeit = zeit + 1
        curr_pos = curr_pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        curr_lager = op_list.lager_nr
        cost_acct = op_list.stornogrund
        create_l_op(zeit)
    op_list_data.clear()

    return generate_output()