#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "new_flag":bool}, {"new_flag": True})

def ins_storerequest_btn_gobl(curr_pos:int, op_list_data:[Op_list], transdate:date, curr_lager:int, deptno:int, transfered:bool, to_stock:int, user_init:string, lscheinnr:string):

    prepare_cache ([L_op, Bediener])

    cost_acct = ""
    price = to_decimal("0.0")
    qty = to_decimal("0.0")
    amount = to_decimal("0.0")
    t_amount = to_decimal("0.0")
    s_artnr = 0
    created = False
    zeit:int = 0
    l_op = bediener = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_acct, price, qty, amount, t_amount, s_artnr, created, zeit, l_op, bediener
        nonlocal curr_pos, transdate, curr_lager, deptno, transfered, to_stock, user_init, lscheinnr


        nonlocal op_list

        return {"curr_pos": curr_pos, "cost_acct": cost_acct, "price": price, "qty": qty, "amount": amount, "t_amount": t_amount, "s_artnr": s_artnr, "created": created}

    def create_l_op(zeit:int):

        nonlocal cost_acct, price, qty, amount, t_amount, s_artnr, created, l_op, bediener
        nonlocal curr_pos, transdate, curr_lager, deptno, transfered, to_stock, user_init, lscheinnr


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

    if curr_pos != None:
        curr_pos = curr_pos - 1


    zeit = get_current_time_in_seconds()

    for op_list in query(op_list_data, filters=(lambda op_list: op_list.anzahl != 0 and op_list.new_flag), sort_by=[("pos",False)]):
        zeit = zeit + 1
        curr_pos = op_list.pos + 1
        s_artnr = op_list.artnr
        qty =  to_decimal(op_list.anzahl)
        price =  to_decimal(op_list.warenwert) / to_decimal(qty)
        cost_acct = op_list.stornogrund


        create_l_op(zeit)

    return generate_output()