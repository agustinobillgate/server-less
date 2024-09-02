from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, Bediener

def ins_storerequest_btn_gobl(curr_pos:int, op_list:[Op_list], transdate:date, curr_lager:int, deptno:int, transfered:bool, to_stock:int, user_init:str, lscheinnr:str):
    cost_acct = ""
    price = 0
    qty = 0
    amount = 0
    t_amount = 0
    s_artnr = 0
    created = False
    zeit:int = 0
    l_op = bediener = None

    op_list = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "new_flag":bool}, {"new_flag": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_acct, price, qty, amount, t_amount, s_artnr, created, zeit, l_op, bediener


        nonlocal op_list
        nonlocal op_list_list
        return {"cost_acct": cost_acct, "price": price, "qty": qty, "amount": amount, "t_amount": t_amount, "s_artnr": s_artnr, "created": created}

    def create_l_op(zeit:int):

        nonlocal cost_acct, price, qty, amount, t_amount, s_artnr, created, zeit, l_op, bediener


        nonlocal op_list
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
    curr_pos = curr_pos - 1
    zeit = get_current_time_in_seconds()

    for op_list in query(op_list_list, filters=(lambda op_list :op_list.anzahl != 0 and op_list.new_flag)):
        zeit = zeit + 1
        curr_pos = op_list.pos + 1
        s_artnr = op_list.artnr
        qty = op_list.anzahl
        price = op_list.warenwert / qty
        cost_acct = op_list.stornogrund


        create_l_op(zeit)

    return generate_output()