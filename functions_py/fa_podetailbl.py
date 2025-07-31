#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 25/7/2025
# if available docu_nr
#-----------------------------------------
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
    # --- Pre-fetch all Mathis and Bediener records ---
    mathis_map = {m.nr: m for m in db_session.query(Mathis).all()}
    bediener_map = {b.userinit: b.username for b in db_session.query(Bediener).all()}

    # --- Loop over fa_order ---
    for fa_order in db_session.query(Fa_order).filter(
        Fa_order.order_nr == docu_nr,
        Fa_order.fa_pos > 0,
        Fa_order.activeflag == 0
    ).order_by(Fa_order.fa_pos).all():

        mathis = mathis_map.get(fa_order.fa_nr)
        temp_last = bediener_map.get(fa_order.last_id, "")
        print("Order:", fa_order.order_nr)
        # Create s_order entry
        s_order = S_order()
        s_order.order_nr = fa_order.order_nr
        s_order.statflag = recid(fa_order)  # placeholder for actual RECID equivalent
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

        # Rd 30/7/2025
        # db_session.add(s_order)
        s_order_data.append(s_order)

        # Create disclist entry
        disclist = Disclist()
        disclist.fa_recid = fa_order.fa_pos
        try:
            # disclist.price0 = fa_order.order_price / (1 - fa_order.discount1 * 0.01) \
            #                 / (1 - fa_order.discount2 * 0.01) / (1 + fa_order.vat * 0.01)
            disclist.price0 = fa_order.order_price / (1 - fa_order.discount1 * Decimal("0.01")) \
                                  / (1 - fa_order.discount2 * Decimal("0.01")) \
                                  / (1 + fa_order.vat * Decimal("0.01"))
        except ZeroDivisionError:
            disclist.price0 = 0
        disclist.brutto = disclist.price0 * fa_order.order_amount

        # db_session.add(disclist)
        disclist_data.append(disclist)

    # --- Second loop over s_order ---
    # Pre-fetch mathis and disclist again
    mathis_map = {m.nr: m for m in db_session.query(Mathis).all()}
    disclist_map = {d.fa_recid: d for d in db_session.query(Disclist).all()}

    for s_order in db_session.query(S_order).filter(S_order.order_nr == docu_nr).order_by(S_order.fa_pos).all():
        mathis = mathis_map.get(s_order.fa_nr)
        disclist = disclist_map.get(s_order.fa_pos)

        if mathis and disclist:
            tmp = Tmp_tbl_data()
            tmp.fa_nr = s_order.fa_nr
            tmp.NAME = mathis.NAME
            tmp.asset = mathis.asset
            tmp.order_qty = s_order.order_qty
            tmp.order_price = s_order.order_price
            tmp.order_amount = s_order.order_amount
            tmp.delivered_qty = s_order.delivered_qty
            tmp.delivered_date = s_order.delivered_date
            tmp.last_user = s_order.last_user
            # db_session.add(tmp)
            tmp_tbl_data.append(tmp)

    # Finally commit all changes
    db_session.commit()

    return generate_output()