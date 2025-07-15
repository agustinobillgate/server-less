#using conversion tools version: 1.0.0.27

from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, L_lieferant, L_artikel, Bediener, L_op

def stock_retourlist_create_listbl(from_date:date, to_date:date, from_sup:str, to_sup:str, show_price:bool):
    str_list_list = []
    amount1:decimal = to_decimal("0.0")
    amount2:decimal = to_decimal("0.0")
    long_digit:bool = False
    htparam = l_lieferant = l_artikel = bediener = l_op = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"s":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, amount1, amount2, long_digit, htparam, l_lieferant, l_artikel, bediener, l_op
        nonlocal from_date, to_date, from_sup, to_sup, show_price


        nonlocal str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def create_list():

        nonlocal str_list_list, amount1, amount2, long_digit, htparam, l_lieferant, l_artikel, bediener, l_op
        nonlocal from_date, to_date, from_sup, to_sup, show_price


        nonlocal str_list
        nonlocal str_list_list

        i:int = 0
        price_decimal:int = 0

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger
        str_list_list.clear()
        amount1 =  to_decimal("0")
        amount2 =  to_decimal("0")

        l_op_obj_list = []
        for l_op, l_lieferant, l_artikel, bediener in db_session.query(L_op, L_lieferant, L_artikel, Bediener).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr) & (func.lower(L_lieferant.firma) >= (from_sup).lower()) & (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(Bediener,(Bediener.nr == L_op.fuellflag)).filter(
                 (L_op.pos > 0) & (L_op.anzahl < 0) & (L_op.loeschflag <= 1) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.lscheinnr, L_op.artnr).all():
            if l_op._recid in l_op_obj_list:
                continue
            else:
                l_op_obj_list.append(l_op._recid)


            str_list = Str_list()
            str_list_list.append(str_list)

            str_list.s = to_string(l_op.datum) + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)")

            if l_op.anzahl < 0:
                str_list.s = str_list.s + to_string(- l_op.anzahl, ">>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(l_op.anzahl, ">>>,>>9.99")

            if show_price:

                if not long_digit:
                    str_list.s = str_list.s + to_string(l_op.einzelpreis, ">>,>>>,>>9.99") + to_string(- l_op.warenwert, ">>,>>>,>>9.99") + to_string(l_op.stornogrund, "x(16)") + to_string(bediener.userinit, "x(2)") + to_string(l_op.lscheinnr, "x(20)") + to_string(l_op.lager_nr, "99")
                else:
                    str_list.s = str_list.s + to_string(l_op.einzelpreis, ">,>>>,>>>,>>9") + to_string(- l_op.warenwert, ">,>>>,>>>,>>9") + to_string(l_op.stornogrund, "x(16)") + to_string(bediener.userinit, "x(2)") + to_string(l_op.lscheinnr, "x(20)") + to_string(l_op.lager_nr, "99")
            else:

                if not long_digit:
                    str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99") + to_string(0, ">>,>>>,>>9.99") + to_string(l_op.stornogrund, "x(16)") + to_string(bediener.userinit, "x(2)") + to_string(l_op.lscheinnr, "x(20)") + to_string(l_op.lager_nr, "99")
                else:
                    str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9") + to_string(0, ">,>>>,>>>,>>9") + to_string(l_op.stornogrund, "x(16)") + to_string(bediener.userinit, "x(2)") + to_string(l_op.lscheinnr, "x(20)") + to_string(l_op.lager_nr, "99")


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    create_list()

    return generate_output()