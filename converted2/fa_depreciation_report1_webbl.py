#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mathis, Queasy, Fa_artikel, Fa_order, Fa_ordheader, Fa_op

payload_list_data, Payload_list = create_model("Payload_list", {"depn_month":string, "sorttype":int, "last_nr":int, "num_data":int, "mode":int})

def fa_depreciation_report1_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Mathis, Queasy, Fa_artikel, Fa_order, Fa_ordheader, Fa_op])

    depreciation_asset_data = []
    output_list_data = []
    tot_amount:Decimal = to_decimal("0.0")
    tot_depn_value:Decimal = to_decimal("0.0")
    tot_book_value:Decimal = to_decimal("0.0")
    tot_acc_depn:int = 0
    datum:date = None
    qty:int = 0
    price:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    counter:int = 0
    counter_num_data:int = 0
    mm:int = 0
    yy:int = 0
    mathis = queasy = fa_artikel = fa_order = fa_ordheader = fa_op = None

    depreciation_asset = payload_list = output_list = None

    depreciation_asset_data, Depreciation_asset = create_model("Depreciation_asset", {"COA":string, "order_date":date, "order_number":string, "desc1":string, "qty":string, "price":string, "amount":string, "depn_value":string, "book_value":string, "acc_depn":string, "date_rcv":date, "first_depn":date})
    output_list_data, Output_list = create_model("Output_list", {"curr_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal depreciation_asset_data, output_list_data, tot_amount, tot_depn_value, tot_book_value, tot_acc_depn, datum, qty, price, amount, counter, counter_num_data, mm, yy, mathis, queasy, fa_artikel, fa_order, fa_ordheader, fa_op


        nonlocal depreciation_asset, payload_list, output_list
        nonlocal depreciation_asset_data, output_list_data

        return {"depreciation-asset": depreciation_asset_data, "output-list": output_list_data}

    def create_list():

        nonlocal depreciation_asset_data, output_list_data, tot_amount, tot_depn_value, tot_book_value, tot_acc_depn, datum, qty, price, amount, counter, counter_num_data, mm, yy, mathis, queasy, fa_artikel, fa_order, fa_ordheader, fa_op


        nonlocal depreciation_asset, payload_list, output_list
        nonlocal depreciation_asset_data, output_list_data

        fa_order = get_cache (Fa_order, {"fa_nr": [(eq, fa_artikel.nr)]})

        if fa_order:

            fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, fa_order.order_nr)]})

            if fa_ordheader:
                depreciation_asset = Depreciation_asset()
                depreciation_asset_data.append(depreciation_asset)

                depreciation_asset.coa = fa_artikel.fibukonto
                depreciation_asset.order_date = fa_ordheader.Order_Date
                depreciation_asset.order_number = fa_ordheader.Order_Nr
                depreciation_asset.desc1 = mathis.name
                depreciation_asset.qty = to_string(fa_order.order_qty, "->,>>>,>>9")
                depreciation_asset.price = to_string(fa_order.order_price, "->>,>>>,>>>,>>>,>>9.99")
                depreciation_asset.amount = to_string(fa_order.order_amount, "->>,>>>,>>>,>>>,>>9.99")
                depreciation_asset.depn_value = to_string(queasy.deci1, ">>,>>>,>>>,>>9.99")
                depreciation_asset.book_value = to_string(queasy.deci2, ">>,>>>,>>>,>>9.99")
                depreciation_asset.acc_depn = to_string(queasy.number3, ">>9")
                depreciation_asset.date_rcv = fa_ordheader.close_date
                depreciation_asset.first_depn = fa_artikel.first_depn


                tot_amount =  to_decimal(tot_amount) + to_decimal(fa_order.order_amount)
                tot_depn_value =  to_decimal(tot_depn_value) + to_decimal(queasy.deci1)
                tot_book_value =  to_decimal(tot_book_value) + to_decimal(queasy.deci2)
                tot_acc_depn = tot_acc_depn + queasy.number3
        else:

            fa_op = get_cache (Fa_op, {"nr": [(eq, fa_artikel.nr)]})

            if fa_op:
                depreciation_asset = Depreciation_asset()
                depreciation_asset_data.append(depreciation_asset)

                depreciation_asset.coa = fa_artikel.fibukonto
                depreciation_asset.order_number = fa_op.docu_nr
                depreciation_asset.desc1 = mathis.name
                depreciation_asset.qty = to_string(fa_op.anzahl, "->,>>>,>>9")
                depreciation_asset.price = to_string(fa_op.einzelpreis, "->>,>>>,>>>,>>>,>>9.99")
                depreciation_asset.amount = to_string(fa_op.warenwert, "->>,>>>,>>>,>>>,>>9.99")
                depreciation_asset.depn_value = to_string(queasy.deci1, ">>,>>>,>>>,>>9.99")
                depreciation_asset.book_value = to_string(queasy.deci2, ">>,>>>,>>>,>>9.99")
                depreciation_asset.acc_depn = to_string(queasy.number3, ">>9")
                depreciation_asset.date_rcv = fa_op.datum
                depreciation_asset.first_depn = fa_artikel.first_depn


                tot_amount =  to_decimal(tot_amount) + to_decimal(fa_op.warenwert)
                tot_depn_value =  to_decimal(tot_depn_value) + to_decimal(queasy.deci1)
                tot_book_value =  to_decimal(tot_book_value) + to_decimal(queasy.deci2)
                tot_acc_depn = tot_acc_depn + queasy.number3
            else:
                depreciation_asset = Depreciation_asset()
                depreciation_asset_data.append(depreciation_asset)

                depreciation_asset.coa = fa_artikel.fibukonto
                depreciation_asset.desc1 = mathis.name
                depreciation_asset.depn_value = to_string(queasy.deci1, ">>,>>>,>>>,>>9.99")
                depreciation_asset.book_value = to_string(queasy.deci2, ">>,>>>,>>>,>>9.99")
                depreciation_asset.acc_depn = to_string(queasy.number3, ">>9")
                depreciation_asset.first_depn = fa_artikel.first_depn


                tot_depn_value =  to_decimal(tot_depn_value) + to_decimal(queasy.deci1)
                tot_book_value =  to_decimal(tot_book_value) + to_decimal(queasy.deci2)
                tot_acc_depn = tot_acc_depn + queasy.number3


    payload_list = query(payload_list_data, first=True)
    output_list = Output_list()
    output_list_data.append(output_list)

    mm = to_int(substring(payload_list.depn_month, 0, 2))
    yy = to_int(substring(payload_list.depn_month, 2, 4))
    datum = date_mdy(mm, 1, yy)
    mm = mm + 1

    if mm == 13:
        mm = 1
        yy = yy + 1
    datum = date_mdy(mm, 1, yy) - timedelta(days=1)
    counter_num_data = payload_list.num_data

    if payload_list.mode == 1:

        if payload_list.sorttype == 1:

            fa_artikel_obj_list = {}
            fa_artikel = Fa_artikel()
            mathis = Mathis()
            queasy = Queasy()
            for fa_artikel.nr, fa_artikel.fibukonto, fa_artikel.first_depn, fa_artikel._recid, mathis.name, mathis.nr, mathis._recid, queasy.deci1, queasy.deci2, queasy.number3, queasy._recid in db_session.query(Fa_artikel.nr, Fa_artikel.fibukonto, Fa_artikel.first_depn, Fa_artikel._recid, Mathis.name, Mathis.nr, Mathis._recid, Queasy.deci1, Queasy.deci2, Queasy.number3, Queasy._recid).join(Mathis,(Mathis.nr == Fa_artikel.nr)).join(Queasy,(Queasy.key == 348) & (Queasy.date1 == datum) & (Queasy.number1 == Fa_artikel.nr)).order_by(Fa_artikel.nr).all():
                if fa_artikel_obj_list.get(fa_artikel._recid):
                    continue
                else:
                    fa_artikel_obj_list[fa_artikel._recid] = True

                if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                    break
                create_list()
                counter = counter + 1
                output_list.curr_nr = mathis.nr
        else:

            if payload_list.last_nr != None and payload_list.last_nr != 0:

                fa_artikel_obj_list = {}
                fa_artikel = Fa_artikel()
                mathis = Mathis()
                queasy = Queasy()
                for fa_artikel.nr, fa_artikel.fibukonto, fa_artikel.first_depn, fa_artikel._recid, mathis.name, mathis.nr, mathis._recid, queasy.deci1, queasy.deci2, queasy.number3, queasy._recid in db_session.query(Fa_artikel.nr, Fa_artikel.fibukonto, Fa_artikel.first_depn, Fa_artikel._recid, Mathis.name, Mathis.nr, Mathis._recid, Queasy.deci1, Queasy.deci2, Queasy.number3, Queasy._recid).join(Mathis,(Mathis.nr == Fa_artikel.nr)).join(Queasy,(Queasy.key == 348) & (Queasy.date1 == datum) & (Queasy.number1 == Fa_artikel.nr)).filter(
                         (Fa_artikel.nr > payload_list.last_nr)).order_by(Fa_artikel.nr).all():
                    if fa_artikel_obj_list.get(fa_artikel._recid):
                        continue
                    else:
                        fa_artikel_obj_list[fa_artikel._recid] = True

                    if (counter >= counter_num_data) and (output_list.curr_nr != mathis.nr):
                        break
                    create_list()
                    counter = counter + 1
                    output_list.curr_nr = mathis.nr
    else:

        fa_artikel_obj_list = {}
        fa_artikel = Fa_artikel()
        mathis = Mathis()
        queasy = Queasy()
        for fa_artikel.nr, fa_artikel.fibukonto, fa_artikel.first_depn, fa_artikel._recid, mathis.name, mathis.nr, mathis._recid, queasy.deci1, queasy.deci2, queasy.number3, queasy._recid in db_session.query(Fa_artikel.nr, Fa_artikel.fibukonto, Fa_artikel.first_depn, Fa_artikel._recid, Mathis.name, Mathis.nr, Mathis._recid, Queasy.deci1, Queasy.deci2, Queasy.number3, Queasy._recid).join(Mathis,(Mathis.nr == Fa_artikel.nr)).join(Queasy,(Queasy.key == 348) & (Queasy.date1 == datum) & (Queasy.number1 == Fa_artikel.nr)).order_by(Fa_artikel.nr).all():
            if fa_artikel_obj_list.get(fa_artikel._recid):
                continue
            else:
                fa_artikel_obj_list[fa_artikel._recid] = True


            create_list()

    depreciation_asset = query(depreciation_asset_data, first=True)

    if depreciation_asset:
        depreciation_asset = Depreciation_asset()
        depreciation_asset_data.append(depreciation_asset)

        depreciation_asset.desc1 = "T O T A L"
        depreciation_asset.amount = to_string(tot_amount, "->>,>>>,>>>,>>>,>>9.99")
        depreciation_asset.depn_value = to_string(tot_depn_value, ">>,>>>,>>>,>>9.99")
        depreciation_asset.book_value = to_string(tot_book_value, ">>,>>>,>>>,>>9.99")
        depreciation_asset.acc_depn = to_string(tot_acc_depn, ">>9")

    return generate_output()