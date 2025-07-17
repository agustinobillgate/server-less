#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_order, Mathis, Bediener

def fa_podetailbl(docu_nr:string):

    prepare_cache ([Fa_order, Mathis, Bediener])

    tmp_tbl_data_data = []
    temp_last:string = ""
    fa_order = mathis = bediener = None

    tmp_tbl_data = disclist = s_order = None

    tmp_tbl_data_data, Tmp_tbl_data = create_model("Tmp_tbl_data", {"fa_nr":int, "name":string, "asset":string, "order_qty":int, "order_price":Decimal, "order_amount":Decimal, "delivered_qty":int, "delivered_date":date, "last_user":string})
    disclist_data, Disclist = create_model("Disclist", {"fa_recid":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal})
    s_order_data, S_order = create_model_like(Fa_order, {"last_user":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_tbl_data_data, temp_last, fa_order, mathis, bediener
        nonlocal docu_nr


        nonlocal tmp_tbl_data, disclist, s_order
        nonlocal tmp_tbl_data_data, disclist_data, s_order_data

        return {"tmp-tbl-data": tmp_tbl_data_data}

    fa_order_obj_list = {}
    fa_order = Fa_order()
    mathis = Mathis()
    # for fa_order.last_id, fa_order.order_nr, fa_order.fa_nr, fa_order.order_qty, fa_order.activeflag, fa_order.order_price, fa_order.order_amount, fa_order.activereason, fa_order.delivered_qty, fa_order.delivered_date, fa_order.fa_pos, fa_order.discount1, fa_order._recid, mathis.nr, mathis.name, mathis.asset, mathis._recid in db_session.query(Fa_order.last_id, Fa_order.order_nr, Fa_order.fa_nr, Fa_order.order_qty, Fa_order.activeflag, Fa_order.order_price, Fa_order.order_amount, Fa_order.activereason, Fa_order.delivered_qty, Fa_order.delivered_date, Fa_order.fa_pos, Fa_order.discount1, Fa_order._recid, Mathis.nr, Mathis.name, Mathis.asset, Mathis._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).filter(
    #          (Fa_order.order_nr == (docu_nr).lower()) & (Fa_order.fa_pos > 0) & (Fa_order.activeflag == 0)).order_by(Fa_order.fa_pos).all():
    results = (
        db_session.query(Fa_order, Mathis)
        .join(Mathis, Fa_order.fa_nr == Mathis.nr)
        .filter(
            Fa_order.order_nr == docu_nr,
            Fa_order.fa_pos > 0,
            Fa_order.activeflag == 0
        )
        .order_by(Fa_order.fa_pos)
        .all()
    )
    # print("Results:", results)
    for fa_order, mathis in results:
        if fa_order_obj_list.get(fa_order._recid):
            continue
        else:
            fa_order_obj_list[fa_order._recid] = True

        bediener = get_cache (Bediener, {"userinit": [(eq, fa_order.last_id)]})

        if bediener:
            temp_last = bediener.username
        else:
            temp_last = ""
        s_order = S_order()
        s_order_data.append(s_order)

        s_order.order_nr = fa_order.order_nr
        s_order.statflag = fa_order._recid
        s_order.fa_nr = fa_order.fa_nr
        s_order.order_qty = fa_order.order_qty
        s_order.activeflag = fa_order.activeflag
        s_order.order_price =  to_decimal(fa_order.order_price)
        s_order.order_amount =  to_decimal(fa_order.order_amount)
        s_order.activereason = fa_order.activereason
        s_order.delivered_qty = fa_order.delivered_qty
        s_order.delivered_date = fa_order.delivered_date
        s_order.fa_pos = fa_order.fa_pos
        s_order.last_id = fa_order.last_id
        s_order.last_user = temp_last


        disclist = Disclist()
        disclist_data.append(disclist)

        disclist.fa_recid = s_order.fa_pos
        disclist.price0 =  to_decimal(fa_order.order_price) / to_decimal((1) - to_decimal(fa_order.discount1) * to_decimal(0.01)) /\
                (1 - to_decimal(fa_order.discount2) * to_decimal(0.01)) / to_decimal((1) + to_decimal(fa_order.vat) * to_decimal(0.01) )
        disclist.brutto =  to_decimal(disclist.price0) * to_decimal(fa_order.order_amount)

    mathis_obj_list = {}
    if disclist:
        results = (
            db_session.query(s_order, disclist, Mathis)
            .join(disclist, disclist.fa_recid == s_order.fa_pos)
            .join(Mathis, Mathis.nr == s_order.fa_nr)
            .filter(s_order.order_nr == docu_nr)
            .order_by(s_order.fa_pos)
            .all()
        )
        # print(disclist)
        for s_order, disclist, mathis in results:
            if mathis_obj_list.get(mathis._recid):
                continue
            else:
                mathis_obj_list[mathis._recid] = True

            s_order = query(s_order_data, (lambda s_order: (mathis.nr == s_order.fa_nr)), first=True)
            tmp_tbl_data = Tmp_tbl_data()
            tmp_tbl_data_data.append(tmp_tbl_data)

            tmp_tbl_data.fa_nr = s_order.fa_nr
            tmp_tbl_data.name = mathis.name
            tmp_tbl_data.asset = mathis.asset
            tmp_tbl_data.order_qty = s_order.order_qty
            tmp_tbl_data.order_price =  to_decimal(s_order.order_price)
            tmp_tbl_data.order_amount =  to_decimal(s_order.order_amount)
            tmp_tbl_data.delivered_qty = s_order.delivered_qty
            tmp_tbl_data.delivered_date = s_order.delivered_date
            tmp_tbl_data.last_user = s_order.last_user

    return generate_output()