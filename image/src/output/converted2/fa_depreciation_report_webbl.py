#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_ordheader, Mathis, Fa_artikel, Fa_order

payload_list_list, Payload_list = create_model("Payload_list", {"from_date":date, "to_date":date})

def fa_depreciation_report_webbl(payload_list_list:[Payload_list]):

    prepare_cache ([Fa_ordheader, Mathis, Fa_artikel, Fa_order])

    depreciation_asset_list = []
    tot_amount:Decimal = to_decimal("0.0")
    tot_depn_value:Decimal = to_decimal("0.0")
    tot_book_value:Decimal = to_decimal("0.0")
    tot_acc_depn:int = 0
    fa_ordheader = mathis = fa_artikel = fa_order = None

    depreciation_asset = payload_list = None

    depreciation_asset_list, Depreciation_asset = create_model("Depreciation_asset", {"coa":string, "order_date":date, "order_number":string, "desc1":string, "qty":string, "price":string, "amount":string, "depn_value":string, "book_value":string, "acc_depn":string, "date_rcv":date, "first_depn":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal depreciation_asset_list, tot_amount, tot_depn_value, tot_book_value, tot_acc_depn, fa_ordheader, mathis, fa_artikel, fa_order


        nonlocal depreciation_asset, payload_list
        nonlocal depreciation_asset_list

        return {"depreciation-asset": depreciation_asset_list}


    payload_list = query(payload_list_list, first=True)

    for fa_ordheader in db_session.query(Fa_ordheader).filter(
             (Fa_ordheader.order_date >= payload_list.from_date) & (Fa_ordheader.order_date <= payload_list.to_date) & (Fa_ordheader.activeflag == 1)).order_by(Fa_ordheader._recid).all():

        fa_order_obj_list = {}
        fa_order = Fa_order()
        mathis = Mathis()
        fa_artikel = Fa_artikel()
        for fa_order.order_qty, fa_order.order_price, fa_order.order_amount, fa_order._recid, mathis.name, mathis._recid, fa_artikel.fibukonto, fa_artikel.depn_wert, fa_artikel.book_wert, fa_artikel.anz_depn, fa_artikel.first_depn, fa_artikel._recid in db_session.query(Fa_order.order_qty, Fa_order.order_price, Fa_order.order_amount, Fa_order._recid, Mathis.name, Mathis._recid, Fa_artikel.fibukonto, Fa_artikel.depn_wert, Fa_artikel.book_wert, Fa_artikel.anz_depn, Fa_artikel.first_depn, Fa_artikel._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).join(Fa_artikel,(Fa_artikel.nr == Mathis.nr)).filter(
                 (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order._recid).all():
            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True


            depreciation_asset = Depreciation_asset()
            depreciation_asset_list.append(depreciation_asset)

            depreciation_asset.coa = fa_artikel.fibukonto
            depreciation_asset.order_date = fa_ordheader.Order_Date
            depreciation_asset.order_number = fa_ordheader.Order_Nr
            depreciation_asset.desc1 = mathis.name
            depreciation_asset.qty = to_string(fa_order.order_qty, "->,>>>,>>9")
            depreciation_asset.price = to_string(fa_order.order_price, "->>,>>>,>>>,>>>,>>9.99")
            depreciation_asset.amount = to_string(fa_order.order_amount, "->>,>>>,>>>,>>>,>>9.99")
            depreciation_asset.depn_value = to_string(fa_artikel.depn_wert, ">>,>>>,>>>,>>9.99")
            depreciation_asset.book_value = to_string(fa_artikel.book_wert, ">>,>>>,>>>,>>9.99")
            depreciation_asset.acc_depn = to_string(fa_artikel.anz_depn, ">>9")
            depreciation_asset.date_rcv = fa_ordheader.close_date
            depreciation_asset.first_depn = fa_artikel.first_depn


            tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
            tot_depn_value =  to_decimal(tot_depn_value) + to_decimal(fa_artikel.depn_wert)
            tot_book_value =  to_decimal(tot_book_value) + to_decimal(fa_artikel.book_wert)
            tot_acc_depn = tot_acc_depn + fa_artikel.anz_depn

    depreciation_asset = query(depreciation_asset_list, first=True)

    if depreciation_asset:
        depreciation_asset = Depreciation_asset()
        depreciation_asset_list.append(depreciation_asset)

        depreciation_asset.desc1 = "T O T A L"
        depreciation_asset.amount = to_string(tot_amount, "->>,>>>,>>>,>>>,>>9.99")
        depreciation_asset.depn_value = to_string(tot_depn_value, ">>,>>>,>>>,>>9.99")
        depreciation_asset.book_value = to_string(tot_book_value, ">>,>>>,>>>,>>9.99")
        depreciation_asset.acc_depn = to_string(tot_acc_depn, ">>9")

    return generate_output()