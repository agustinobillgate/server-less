# using conversion tools version: 1.0.0.117
"""_yusufiwjasena_26/01/2026

        remark: - optimize query for fa-order2
"""
from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, Fa_order, Mathis


def fa_polistbl(t_table: string, supplier_nr: int, order_nr: string):

    prepare_cache([Fa_order, Mathis])

    flag_avail = False
    t_order_data = []
    l_kredit = fa_order = mathis = None

    t_order = None

    t_order_data, T_order = create_model(
        "T_order",
        {
            "fa_nr": int,
            "name": string,
            "asset": string,
            "order_qty": int,
            "order_price": Decimal,
            "order_amount": Decimal,
            "order_nr": string,
            "model": string
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_avail, t_order_data, l_kredit, fa_order, mathis
        nonlocal t_table, supplier_nr, order_nr
        nonlocal t_order
        nonlocal t_order_data

        return {
            "flag_avail": flag_avail,
            "t-order": t_order_data
        }

    t_order_data.clear()

    if t_table.lower() == "l-kredit":

        l_kredit = get_cache(L_kredit, {"lief_nr": [(eq, supplier_nr)], "name": [
                             (eq, order_nr)], "zahlkonto": [(gt, 0)]})

        if l_kredit:
            flag_avail = True
        else:
            flag_avail = False

    elif t_table.lower() == "fa-order":

        fa_order = get_cache(Fa_order, {"order_nr": [(eq, order_nr)]})

        if fa_order:
            flag_avail = True
        else:
            flag_avail = False

    elif t_table.lower() == "fa-order2":

        fa_order_obj_list = {}
        # fa_order = Fa_order()
        # mathis = Mathis()
        fa_order_data = (
            db_session.query(Fa_order, Mathis)
            .join(Mathis, (Mathis.nr == Fa_order.fa_nr))
            .filter(
                 (Fa_order.order_nr == (order_nr).lower()) &
                 (Fa_order.activeflag == 0)
            )
            .order_by(Fa_order.fa_pos)
        )

        for fa_order, mathis in fa_order_data.yield_per(100):
            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True

            t_order = T_order()
            t_order_data.append(t_order)

            t_order.fa_nr = fa_order.fa_nr
            t_order.name = mathis.name
            t_order.asset = mathis.asset
            t_order.order_qty = fa_order.order_qty
            t_order.order_price = to_decimal(fa_order.order_price)
            t_order.order_amount = to_decimal(fa_order.order_amount)
            t_order.order_nr = fa_order.order_nr
            t_order.model = mathis.model

    return generate_output()
