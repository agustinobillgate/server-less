#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, Fa_order, Mathis

def fa_polistbl(t_table:string, supplier_nr:int, order_nr:string):

    prepare_cache ([Fa_order, Mathis])

    flag_avail = False
    t_order_list = []
    l_kredit = fa_order = mathis = None

    t_order = None

    t_order_list, T_order = create_model("T_order", {"fa_nr":int, "name":string, "asset":string, "order_qty":int, "order_price":Decimal, "order_amount":Decimal, "order_nr":string, "model":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_avail, t_order_list, l_kredit, fa_order, mathis
        nonlocal t_table, supplier_nr, order_nr


        nonlocal t_order
        nonlocal t_order_list

        return {"flag_avail": flag_avail, "t-order": t_order_list}


    t_order_list.clear()

    if t_table.lower()  == ("l-kredit").lower() :

        l_kredit = get_cache (L_kredit, {"lief_nr": [(eq, supplier_nr)],"name": [(eq, order_nr)],"zahlkonto": [(gt, 0)]})

        if l_kredit:
            flag_avail = True
        else:
            flag_avail = False

    elif t_table.lower()  == ("fa-order").lower() :

        fa_order = get_cache (Fa_order, {"order_nr": [(eq, order_nr)]})

        if fa_order:
            flag_avail = True
        else:
            flag_avail = False

    elif t_table.lower()  == ("fa-order2").lower() :

        fa_order_obj_list = {}
        fa_order = Fa_order()
        mathis = Mathis()
        for fa_order.fa_nr, fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order.order_nr, fa_order._recid, mathis.name, mathis.asset, mathis.model, mathis._recid in db_session.query(Fa_order.fa_nr, Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Mathis.name, Mathis.asset, Mathis.model, Mathis._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).filter(
                 (Fa_order.order_nr == (order_nr).lower()) & (Fa_order.activeflag == 0)).order_by(Fa_order.fa_pos).all():
            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True


            t_order = T_order()
            t_order_list.append(t_order)

            t_order.fa_nr = fa_order.fa_nr
            t_order.name = mathis.name
            t_order.asset = mathis.asset
            t_order.order_qty = fa_order.order_qty
            t_order.order_price =  to_decimal(fa_order.order_price)
            t_order.order_amount =  to_decimal(fa_order.order_amount)
            t_order.order_nr = fa_order.order_nr
            t_order.model = mathis.model

    return generate_output()