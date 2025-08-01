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

    for fa_order in db_session.query(Fa_order).filter(
             (Fa_order.order_nr == (docu_nr).lower()) & (Fa_order.fa_pos > 0) & (Fa_order.activeflag == 0)).order_by(Fa_order.fa_pos).all():

        mathis = get_cache (Mathis, {"nr": [(eq, fa_order.fa_nr)]})

        bediener = get_cache (Bediener, {"userinit": [(eq, fa_order.last_id)]})

        if bediener:
            temp_last = bediener.username
        else:
            temp_last = ""
        s_order = S_order()
        s_order_data.append(s_order)

        s_order.order_nr = fa_order.order_nr
        s_order.statflag = l_order._recid
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
        disclist.price0 =  to_decimal(fa_order.order_price) /\
                (1 - to_decimal(fa_order.discount1) * to_decimal(0.01)) /\
                (1 - to_decimal(fa_order.discount2) * to_decimal(0.01)) /\
                (1 + to_decimal(fa_order.vat) * to_decimal(0.01) )
        disclist.brutto =  to_decimal(disclist.price0) * to_decimal(fa_order.order_amount)
        disclist.disc =  to_decimal(fa_order.discount1)
        disclist.disc2 =  to_decimal(fa_order.discount2)
        disclist.vat =  to_decimal(fa_order.vat)

    for s_order in query(s_order_data, filters=(lambda s_order: s_order.order_nr.lower()  == (docu_nr).lower())):

        disclist = query(disclist_data, filters=(lambda disclist: disclist.fa_recid == s_order.fa_pos), first=True)

        mathis = get_cache (Mathis, {"nr": [(eq, s_order.fa_nr)]})

        if disclist and mathis:
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