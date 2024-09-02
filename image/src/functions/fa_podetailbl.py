from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_order, Mathis, Bediener

def fa_podetailbl(docu_nr:str):
    tmp_tbl_data_list = []
    temp_last:str = ""
    fa_order = mathis = bediener = None

    tmp_tbl_data = disclist = s_order = None

    tmp_tbl_data_list, Tmp_tbl_data = create_model("Tmp_tbl_data", {"fa_nr":int, "name":str, "asset":str, "order_qty":int, "order_price":decimal, "order_amount":decimal, "delivered_qty":int, "delivered_date":date, "last_user":str})
    disclist_list, Disclist = create_model("Disclist", {"fa_recid":int, "price0":decimal, "brutto":decimal, "disc":decimal, "disc2":decimal, "vat":decimal})
    s_order_list, S_order = create_model_like(Fa_order, {"last_user":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_tbl_data_list, temp_last, fa_order, mathis, bediener


        nonlocal tmp_tbl_data, disclist, s_order
        nonlocal tmp_tbl_data_list, disclist_list, s_order_list
        return {"tmp-tbl-data": tmp_tbl_data_list}

    fa_order_obj_list = []
    for fa_order, mathis in db_session.query(Fa_order, Mathis).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).filter(
            (func.lower(Fa_order.order_nr) == (docu_nr).lower()) &  (Fa_order.fa_pos > 0) &  (Fa_order.activeflag == 0)).all():
        if fa_order._recid in fa_order_obj_list:
            continue
        else:
            fa_order_obj_list.append(fa_order._recid)

        bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == fa_order.last_id)).first()

        if bediener:
            temp_last = bediener.username
        else:
            temp_last = ""
        s_order = S_order()
        s_order_list.append(s_order)

        s_order.order_nr = fa_order.order_nr
        s_order.statflag = l_order._recid
        s_order.fa_nr = fa_order.fa_nr
        s_order.order_qty = fa_order.order_qty
        s_order.activeflag = fa_order.activeflag
        s_order.order_price = fa_order.order_price
        s_order.order_amount = fa_order.order_amount
        s_order.activereason = fa_order.activereason
        s_order.delivered_qty = fa_order.delivered_qty
        s_order.delivered_date = fa_order.delivered_date
        s_order.fa_pos = fa_order.fa_pos
        s_order.last_id = fa_order.last_id
        s_order.last_user = temp_last


        disclist = Disclist()
        disclist_list.append(disclist)

        disclist.fa_recid = s_order.fa_pos
        disclist.price0 = fa_order.order_price / (1 - fa_order.discount1 * 0.01) /\
                (1 - fa_order.discount2 * 0.01) / (1 + fa_order.vat * 0.01)
        disclist.brutto = disclist.price0 * fa_order.order_amount

    for s_order in query(s_order_list, filters=(lambda s_order :s_order.order_nr.lower()  == (docu_nr).lower())):
        disclist = db_session.query(Disclist).filter((Disclist.fa_recid == s_order.fa_pos)).first()
        if not disclist:
            continue

        mathis = db_session.query(Mathis).filter((Mathis.nr == s_order.fa_nr)).first()
        if not mathis:
            continue

        tmp_tbl_data = Tmp_tbl_data()
        tmp_tbl_data_list.append(tmp_tbl_data)

        tmp_tbl_data.fa_nr = s_order.fa_nr
        tmp_tbl_data.name = mathis.name
        tmp_tbl_data.asset = mathis.asset
        tmp_tbl_data.order_qty = s_order.order_qty
        tmp_tbl_data.order_price = s_order.order_price
        tmp_tbl_data.order_amount = s_order.order_amount
        tmp_tbl_data.delivered_qty = s_order.delivered_qty
        tmp_tbl_data.delivered_date = s_order.delivered_date
        tmp_tbl_data.last_user = s_order.last_user

    return generate_output()