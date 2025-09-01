#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 1/9/2025
# COA -> coa
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Fa_op, Fa_artikel, Mathis, Fa_ordheader, Fa_order

payload_list_data, Payload_list = create_model("Payload_list", {"from_date":date, "to_date":date})

def fa_budget_realization_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Queasy, Fa_op, Fa_artikel, Mathis, Fa_ordheader, Fa_order])

    fa_budget_realization_data = []
    count_i:int = 0
    period_qty:int = 0
    start_jan:date = None
    period_amount:Decimal = to_decimal("0.0")
    period_budget:Decimal = to_decimal("0.0")
    period_variance:Decimal = to_decimal("0.0")
    nr_budget:string = ""
    fa_artnr:int = 0
    grand_total_qty:int = 0
    grand_total_amount:Decimal = to_decimal("0.0")
    grand_total_budget:Decimal = to_decimal("0.0")
    grand_total_variance:Decimal = to_decimal("0.0")
    tot_qty_item:int = 0
    tot_price_item:Decimal = to_decimal("0.0")
    tot_amount_item:Decimal = to_decimal("0.0")
    queasy = fa_op = fa_artikel = mathis = fa_ordheader = fa_order = None

    fa_budget_realization = fix_asset_list = payload_list = None

    fa_budget_realization_data, Fa_budget_realization = create_model("Fa_budget_realization", {"asset":string, "asset_date":date, "descrip_str":string, "account_no":string, "price_str":string, "anzahl_str":string, "amount_str":string, "budget_str":string, "variance_str":string, "budget_date":date, "order_number":string, "budget_number":string, "tot_budget_item":string, "coa":string, "budget_amount":string, "asset_loc":string, "asset_name":string, "asset_qty":string, "asset_price":string, "asset_amount":string, "payment_date":date})
    fix_asset_list_data, Fix_asset_list = create_model("Fix_asset_list", {"nr_budget":int, "desc_budget":string, "date_budget":date, "amount_budget":Decimal, "is_active_budget":bool, "safe_to_del_or_mod":bool, "remain_budget":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_budget_realization_data, count_i, period_qty, start_jan, period_amount, period_budget, period_variance, nr_budget, fa_artnr, grand_total_qty, grand_total_amount, grand_total_budget, grand_total_variance, tot_qty_item, tot_price_item, tot_amount_item, queasy, fa_op, fa_artikel, mathis, fa_ordheader, fa_order


        nonlocal fa_budget_realization, fix_asset_list, payload_list
        nonlocal fa_budget_realization_data, fix_asset_list_data

        return {"fa-budget-realization": fa_budget_realization_data}

    def create_budget_realization():

        nonlocal fa_budget_realization_data, count_i, period_qty, start_jan, period_amount, period_budget, period_variance, nr_budget, fa_artnr, grand_total_qty, grand_total_amount, grand_total_budget, grand_total_variance, tot_qty_item, tot_price_item, tot_amount_item, queasy, fa_op, fa_artikel, mathis, fa_ordheader, fa_order


        nonlocal fa_budget_realization, fix_asset_list, payload_list
        nonlocal fa_budget_realization_data, fix_asset_list_data

        budget_date_last:date = None
        budget_nr_last:int = 0
        budget_desc_last:string = ""
        tmp_budget_number:string = ""
        tot_qty:int = 0
        tot_price:Decimal = to_decimal("0.0")
        tot_amount:Decimal = to_decimal("0.0")

        fa_order_obj_list = {}
        for fa_order, fa_op, fa_artikel, mathis, fa_ordheader in db_session.query(Fa_order, Fa_op, Fa_artikel, Mathis, Fa_ordheader).join(Fa_op,(Fa_op.loeschflag <= 1) & (Fa_op.opart == 1) & (Fa_op.anzahl > 0) & (Fa_op.docu_nr == Fa_order.order_nr) & (Fa_op.datum >= payload_list.from_date) & (Fa_op.datum <= payload_list.to_date)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).join(Fa_ordheader,(Fa_ordheader.order_nr == Fa_op.docu_nr)).filter(
                 (Fa_order.activereason != ("0").lower()) & (Fa_order.activereason != "") & (Fa_order.activereason != None)).order_by(Fa_order.activereason, Fa_op.nr, Fa_op.datum).all():
            fix_asset_list = query(fix_asset_list_data, (lambda fix_asset_list: to_string(fix_asset_list.nr_budget) == fa_order.activereason), first=True)
            if not fix_asset_list:
                continue

            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True


            count_i = count_i + 1

            if fa_order.activereason.lower()  != (nr_budget).lower() :

                if nr_budget != "":
                    fa_budget_realization = Fa_budget_realization()
                    fa_budget_realization_data.append(fa_budget_realization)

                    fa_budget_realization.anzahl_str = to_string(period_qty, "->>,>>>,>>9")
                    fa_budget_realization.amount_str = to_string(period_amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_realization.variance_str = to_string(period_variance, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_realization.descrip_str = "T O T A L"
                    fa_budget_realization.account_no = ""
                    fa_budget_realization.asset_qty = to_string(tot_qty_item)
                    fa_budget_realization.asset_price = to_string(tot_price_item, "->>,>>>,>>>,>>>,>>9.99")
                    fa_budget_realization.asset_amount = to_string(tot_amount_item, "->>,>>>,>>>,>>>,>>9.99")


                    grand_total_qty = grand_total_qty + period_qty
                    grand_total_amount =  to_decimal(grand_total_amount) + to_decimal(period_amount)
                    grand_total_budget =  to_decimal(grand_total_budget) + to_decimal(period_budget)
                    grand_total_variance =  to_decimal(grand_total_variance) + to_decimal(period_variance)
                    fa_budget_realization = Fa_budget_realization()
                    fa_budget_realization_data.append(fa_budget_realization)

                    period_budget =  to_decimal("0")
                    period_qty = 0
                    period_amount =  to_decimal("0")
                    period_variance =  to_decimal("0")
                    tot_qty_item = 0
                    tot_price_item =  to_decimal("0")
                    tot_amount_item =  to_decimal("0")
                period_budget =  to_decimal(fix_asset_list.amount_budget)
                fa_budget_realization = Fa_budget_realization()
                fa_budget_realization_data.append(fa_budget_realization)

                fa_budget_realization.descrip_str = to_string(fix_asset_list.nr_budget) + " - " + fix_asset_list.desc_budget
                fa_budget_realization.account_no = ""
                fa_budget_realization.budget_number = to_string(fix_asset_list.nr_budget, ">,>>9")
                fa_budget_realization.budget_date = fix_asset_list.date_budget
                fa_budget_realization.budget_str = to_string(period_budget, "->>>,>>>,>>>,>>>,>>9.99")


                nr_budget = fa_order.activereason
                budget_date_last = fix_asset_list.date_budget
                budget_nr_last = fix_asset_list.nr_budget

            if fa_artnr != fa_op.nr:
                fa_budget_realization = Fa_budget_realization()
                fa_budget_realization_data.append(fa_budget_realization)

                fa_budget_realization.asset = mathis.asset
                fa_budget_realization.account_no = fa_artikel.fibukonto
                fa_budget_realization.asset_date = fa_op.datum
                fa_budget_realization.price_str = to_string(fa_op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_realization.anzahl_str = to_string(fa_op.anzahl, "->>,>>>,>>9")
                fa_budget_realization.amount_str = to_string(fa_op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_realization.coa = fa_artikel.fibukonto
                fa_budget_realization.budget_amount = to_string(fix_asset_list.amount_budget)
                fa_budget_realization.order_number = fa_op.docu_nr
                fa_budget_realization.asset_loc = mathis.location
                fa_budget_realization.asset_name = mathis.name
                fa_budget_realization.asset_qty = to_string(fa_order.order_qty)
                fa_budget_realization.asset_price = to_string(fa_order.order_price, "->>,>>>,>>>,>>>,>>9.99")
                fa_budget_realization.asset_amount = to_string(fa_order.order_amount, "->>,>>>,>>>,>>>,>>9.99")
                fa_budget_realization.payment_date = fa_ordheader.paymentdate


                period_qty = period_qty + fa_op.anzahl
                period_amount =  to_decimal(period_amount) + to_decimal(fa_op.warenwert)
                period_variance = ( to_decimal(period_budget) - to_decimal(period_amount))
                tot_qty_item = tot_qty_item + fa_order.order_qty
                tot_price_item =  to_decimal(tot_price_item) + to_decimal(fa_order.order_price)
                tot_amount_item =  to_decimal(tot_amount_item) + to_decimal(fa_order.order_amount)
                fa_artnr = fa_op.nr

        if count_i > 0:
            fa_budget_realization = Fa_budget_realization()
            fa_budget_realization_data.append(fa_budget_realization)

            fa_budget_realization.anzahl_str = to_string(period_qty, "->>,>>>,>>9")
            fa_budget_realization.amount_str = to_string(period_amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_realization.variance_str = to_string(period_variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_realization.descrip_str = "T O T A L"
            fa_budget_realization.asset_qty = to_string(tot_qty_item)
            fa_budget_realization.asset_price = to_string(tot_price_item, "->>,>>>,>>>,>>>,>>9.99")
            fa_budget_realization.asset_amount = to_string(tot_amount_item, "->>,>>>,>>>,>>>,>>9.99")


            fa_budget_realization = Fa_budget_realization()
            fa_budget_realization_data.append(fa_budget_realization)

            grand_total_qty = grand_total_qty + period_qty
            grand_total_amount =  to_decimal(grand_total_amount) + to_decimal(period_amount)
            grand_total_budget =  to_decimal(grand_total_budget) + to_decimal(period_budget)
            grand_total_variance =  to_decimal(grand_total_variance) + to_decimal(period_variance)
            fa_budget_realization = Fa_budget_realization()
            fa_budget_realization_data.append(fa_budget_realization)

            fa_budget_realization.anzahl_str = to_string(grand_total_qty, "->>,>>>,>>9")
            fa_budget_realization.asset_amount = to_string(grand_total_amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_realization.variance_str = to_string(grand_total_variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_realization.budget_str = to_string(grand_total_budget, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_realization.descrip_str = "GRAND TOTAL"


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 324)).order_by(Queasy._recid).all():
        fix_asset_list = Fix_asset_list()
        fix_asset_list_data.append(fix_asset_list)

        fix_asset_list.nr_budget = queasy.number1
        fix_asset_list.desc_budget = queasy.char1
        fix_asset_list.date_budget = queasy.date1
        fix_asset_list.amount_budget =  to_decimal(queasy.deci1)
        fix_asset_list.is_active_budget = queasy.logi1

    payload_list = query(payload_list_data, first=True)
    create_budget_realization()

    return generate_output()