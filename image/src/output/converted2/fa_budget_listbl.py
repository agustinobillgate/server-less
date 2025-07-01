#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Fa_op, Fa_artikel, Mathis, Fa_order

def fa_budget_listbl(ytd_flag:bool, from_date:date, to_date:date, ytd_date:date, detailed:bool):

    prepare_cache ([Queasy, Fa_op, Fa_artikel, Mathis, Fa_order])

    fa_budget_ytd_list = []
    fa_budget_period_list = []
    curr_fibu:string = ""
    fibu_formated:string = ""
    count_i:int = 0
    t_mtd_qty:int = 0
    t_ytd_qty:int = 0
    period_qty:int = 0
    start_jan:date = None
    mtd_budget:Decimal = to_decimal("0.0")
    mtd_variance:Decimal = to_decimal("0.0")
    ytd_budget:Decimal = to_decimal("0.0")
    ytd_variance:Decimal = to_decimal("0.0")
    t_mtd_amount:Decimal = to_decimal("0.0")
    t_ytd_amount:Decimal = to_decimal("0.0")
    period_amount:Decimal = to_decimal("0.0")
    period_budget:Decimal = to_decimal("0.0")
    period_variance:Decimal = to_decimal("0.0")
    it_exist:bool = False
    nr_budget:string = ""
    fa_artnr:int = 0
    grand_total_qty:int = 0
    grand_total_amount:Decimal = to_decimal("0.0")
    grand_total_budget:Decimal = to_decimal("0.0")
    grand_total_variance:Decimal = to_decimal("0.0")
    queasy = fa_op = fa_artikel = mathis = fa_order = None

    fa_budget_ytd = fa_budget_period = fix_asset_list = None

    fa_budget_ytd_list, Fa_budget_ytd = create_model("Fa_budget_ytd", {"asset":string, "descrip_str":string, "account_no":string, "anzahl_str":string, "amount_str":string, "mtd_budget_str":string, "mtd_variance_str":string, "anzahlytd_str":string, "amountytd_str":string, "ytd_budget_str":string, "ytd_variance_str":string})
    fa_budget_period_list, Fa_budget_period = create_model("Fa_budget_period", {"asset":string, "asset_date":date, "descrip_str":string, "account_no":string, "price_str":string, "anzahl_str":string, "amount_str":string, "budget_str":string, "variance_str":string, "budget_date":date})
    fix_asset_list_list, Fix_asset_list = create_model("Fix_asset_list", {"nr_budget":int, "desc_budget":string, "date_budget":date, "amount_budget":Decimal, "is_active_budget":bool, "safe_to_del_or_mod":bool, "remain_budget":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_budget_ytd_list, fa_budget_period_list, curr_fibu, fibu_formated, count_i, t_mtd_qty, t_ytd_qty, period_qty, start_jan, mtd_budget, mtd_variance, ytd_budget, ytd_variance, t_mtd_amount, t_ytd_amount, period_amount, period_budget, period_variance, it_exist, nr_budget, fa_artnr, grand_total_qty, grand_total_amount, grand_total_budget, grand_total_variance, queasy, fa_op, fa_artikel, mathis, fa_order
        nonlocal ytd_flag, from_date, to_date, ytd_date, detailed


        nonlocal fa_budget_ytd, fa_budget_period, fix_asset_list
        nonlocal fa_budget_ytd_list, fa_budget_period_list, fix_asset_list_list

        return {"fa-budget-ytd": fa_budget_ytd_list, "fa-budget-period": fa_budget_period_list}

    def create_budget_ytd():

        nonlocal fa_budget_ytd_list, fa_budget_period_list, curr_fibu, fibu_formated, count_i, t_mtd_qty, t_ytd_qty, period_qty, start_jan, mtd_budget, mtd_variance, ytd_budget, ytd_variance, t_mtd_amount, t_ytd_amount, period_amount, period_budget, period_variance, it_exist, nr_budget, fa_artnr, grand_total_qty, grand_total_amount, grand_total_budget, grand_total_variance, queasy, fa_op, fa_artikel, mathis, fa_order
        nonlocal ytd_flag, from_date, to_date, ytd_date, detailed


        nonlocal fa_budget_ytd, fa_budget_period, fix_asset_list
        nonlocal fa_budget_ytd_list, fa_budget_period_list, fix_asset_list_list

        budget_date_last:date = None
        budget_nr_last:int = 0
        budget_desc_last:string = ""
        start_jan = date_mdy(1, 1, get_year(ytd_date))

        fa_order_obj_list = {}
        for fa_order, fa_op, fa_artikel, mathis in db_session.query(Fa_order, Fa_op, Fa_artikel, Mathis).join(Fa_op,(Fa_op.loeschflag <= 1) & (Fa_op.opart == 1) & (Fa_op.anzahl > 0) & (Fa_op.docu_nr == Fa_order.Order_Nr) & (Fa_op.datum >= start_jan) & (Fa_op.datum <= ytd_date)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                 (Fa_order.ActiveReason != ("0").lower()) & (Fa_order.ActiveReason != "") & (Fa_order.ActiveReason != None)).order_by(Fa_order.activereason, Fa_op.nr, Fa_op.datum).yield_per(100):
            fix_asset_list = query(fix_asset_list_list, (lambda fix_asset_list: to_string(fix_asset_list.nr_budget) == fa_order.ActiveReason), first=True)
            if not fix_asset_list:
                continue

            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True

            if fa_order.ActiveReason.lower()  != (nr_budget).lower() :

                if nr_budget != "":
                    fa_budget_ytd = Fa_budget_ytd()
                    fa_budget_ytd_list.append(fa_budget_ytd)

                    fa_budget_ytd.anzahl_str = to_string(t_mtd_qty, "->>,>>>,>>9")
                    fa_budget_ytd.amount_str = to_string(t_mtd_amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_ytd.mtd_variance_str = to_string(mtd_variance, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_ytd.anzahlytd_str = to_string(t_ytd_qty, "->>,>>>,>>9")
                    fa_budget_ytd.amountytd_str = to_string(t_ytd_amount, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_ytd.ytd_variance_str = to_string(ytd_variance, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_ytd.descrip_str = to_string(nr_budget) + " - " + budget_desc_last
                    fa_budget_ytd.account_no = to_string(nr_budget, ">,>>9")
                    fa_budget_ytd.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_ytd.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")


                    mtd_budget =  to_decimal("0")
                    ytd_budget =  to_decimal("0")
                    t_mtd_qty = 0
                    t_mtd_amount =  to_decimal("0")
                    mtd_variance =  to_decimal("0")
                    t_ytd_qty = 0
                    t_ytd_amount =  to_decimal("0")
                    ytd_variance =  to_decimal("0")
                mtd_budget =  to_decimal(fix_asset_list.amount_budget)
                ytd_budget =  to_decimal(fix_asset_list.amount_budget)
                nr_budget = fa_order.ActiveReason
                budget_date_last = fix_asset_list.date_budget
                budget_nr_last = fix_asset_list.nr_budget
                budget_desc_last = fix_asset_list.desc_budget
            count_i = count_i + 1

            if fa_artnr != fa_op.nr:

                if get_month(fa_op.datum) == get_month(ytd_date):
                    t_mtd_qty = t_mtd_qty + fa_op.anzahl
                    t_mtd_amount =  to_decimal(t_mtd_amount) + to_decimal(fa_op.warenwert)
                    mtd_variance = ( to_decimal(mtd_budget) - to_decimal(t_mtd_amount) )


                t_ytd_qty = t_ytd_qty + fa_op.anzahl
                t_ytd_amount =  to_decimal(t_ytd_amount) + to_decimal(fa_op.warenwert)
                ytd_variance = ( to_decimal(ytd_budget) - to_decimal(t_ytd_amount))
                fa_artnr = fa_op.nr

        if count_i > 0:
            fa_budget_ytd = Fa_budget_ytd()
            fa_budget_ytd_list.append(fa_budget_ytd)

            fa_budget_ytd.anzahl_str = to_string(t_mtd_qty, "->>,>>>,>>9")
            fa_budget_ytd.amount_str = to_string(t_mtd_amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_ytd.mtd_variance_str = to_string(mtd_variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_ytd.anzahlytd_str = to_string(t_ytd_qty, "->>,>>>,>>9")
            fa_budget_ytd.amountytd_str = to_string(t_ytd_amount, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_ytd.ytd_variance_str = to_string(ytd_variance, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_ytd.descrip_str = to_string(nr_budget) + " - " + budget_desc_last
            fa_budget_ytd.account_no = to_string(nr_budget, ">,>>9")
            fa_budget_ytd.mtd_budget_str = to_string(mtd_budget, "->>>,>>>,>>>,>>>,>>9.99")
            fa_budget_ytd.ytd_budget_str = to_string(ytd_budget, "->>>,>>>,>>>,>>>,>>9.99")


    def create_budget_period():

        nonlocal fa_budget_ytd_list, fa_budget_period_list, curr_fibu, fibu_formated, count_i, t_mtd_qty, t_ytd_qty, period_qty, start_jan, mtd_budget, mtd_variance, ytd_budget, ytd_variance, t_mtd_amount, t_ytd_amount, period_amount, period_budget, period_variance, it_exist, nr_budget, fa_artnr, grand_total_qty, grand_total_amount, grand_total_budget, grand_total_variance, queasy, fa_op, fa_artikel, mathis, fa_order
        nonlocal ytd_flag, from_date, to_date, ytd_date, detailed


        nonlocal fa_budget_ytd, fa_budget_period, fix_asset_list
        nonlocal fa_budget_ytd_list, fa_budget_period_list, fix_asset_list_list

        budget_date_last:date = None
        budget_nr_last:int = 0
        budget_desc_last:string = ""

        if detailed:

            fa_order_obj_list = {}
            for fa_order, fa_op, fa_artikel, mathis in db_session.query(Fa_order, Fa_op, Fa_artikel, Mathis).join(Fa_op,(Fa_op.loeschflag <= 1) & (Fa_op.opart == 1) & (Fa_op.anzahl > 0) & (Fa_op.docu_nr == Fa_order.Order_Nr) & (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                     (Fa_order.ActiveReason != ("0").lower()) & (Fa_order.ActiveReason != "") & (Fa_order.ActiveReason != None)).order_by(Fa_order.activereason, Fa_op.nr, Fa_op.datum).yield_per(100):
                fix_asset_list = query(fix_asset_list_list, (lambda fix_asset_list: to_string(fix_asset_list.nr_budget) == fa_order.ActiveReason), first=True)
                if not fix_asset_list:
                    continue

                if fa_order_obj_list.get(fa_order._recid):
                    continue
                else:
                    fa_order_obj_list[fa_order._recid] = True


                count_i = count_i + 1

                if fa_order.ActiveReason.lower()  != (nr_budget).lower() :

                    if nr_budget != "":
                        fa_budget_period = Fa_budget_period()
                        fa_budget_period_list.append(fa_budget_period)

                        fa_budget_period.anzahl_str = to_string(period_qty, "->>,>>>,>>9")
                        fa_budget_period.amount_str = to_string(period_amount, "->>>,>>>,>>>,>>>,>>9.99")
                        fa_budget_period.variance_str = to_string(period_variance, "->>>,>>>,>>>,>>>,>>9.99")
                        fa_budget_period.budget_str = to_string(period_budget, "->>>,>>>,>>>,>>>,>>9.99")
                        fa_budget_period.budget_date = fix_asset_list.date_budget
                        fa_budget_period.descrip_str = "T O T A L"
                        fa_budget_period.account_no = to_string(fix_asset_list.nr_budget, ">,>>9")


                        grand_total_qty = grand_total_qty + period_qty
                        grand_total_amount =  to_decimal(grand_total_amount) + to_decimal(period_amount)
                        grand_total_budget =  to_decimal(grand_total_budget) + to_decimal(period_budget)
                        grand_total_variance =  to_decimal(grand_total_variance) + to_decimal(period_variance)
                        fa_budget_period = Fa_budget_period()
                        fa_budget_period_list.append(fa_budget_period)

                        period_budget =  to_decimal("0")
                        period_qty = 0
                        period_amount =  to_decimal("0")
                        period_variance =  to_decimal("0")
                    period_budget =  to_decimal(fix_asset_list.amount_budget)
                    fa_budget_period = Fa_budget_period()
                    fa_budget_period_list.append(fa_budget_period)

                    fa_budget_period.descrip_str = to_string(fix_asset_list.nr_budget) + " - " + fix_asset_list.desc_budget
                    fa_budget_period.account_no = to_string(fix_asset_list.nr_budget, ">,>>9")


                    nr_budget = fa_order.ActiveReason
                    budget_date_last = fix_asset_list.date_budget
                    budget_nr_last = fix_asset_list.nr_budget

                if fa_artnr != fa_op.nr:
                    fa_budget_period = Fa_budget_period()
                    fa_budget_period_list.append(fa_budget_period)

                    fa_budget_period.descrip_str = mathis.name
                    fa_budget_period.asset = mathis.asset
                    fa_budget_period.account_no = fa_artikel.fibukonto
                    fa_budget_period.asset_date = fa_op.datum
                    fa_budget_period.price_str = to_string(fa_op.einzelpreis, "->>>,>>>,>>>,>>>,>>9.99")
                    fa_budget_period.anzahl_str = to_string(fa_op.anzahl, "->>,>>>,>>9")
                    fa_budget_period.amount_str = to_string(fa_op.warenwert, "->>>,>>>,>>>,>>>,>>9.99")


                    period_qty = period_qty + fa_op.anzahl
                    period_amount =  to_decimal(period_amount) + to_decimal(fa_op.warenwert)
                    period_variance = ( to_decimal(period_budget) - to_decimal(period_amount))
                    fa_artnr = fa_op.nr

            if count_i > 0:
                fa_budget_period = Fa_budget_period()
                fa_budget_period_list.append(fa_budget_period)

                fa_budget_period.anzahl_str = to_string(period_qty, "->>,>>>,>>9")
                fa_budget_period.amount_str = to_string(period_amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.variance_str = to_string(period_variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.budget_str = to_string(period_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.budget_date = budget_date_last
                fa_budget_period.descrip_str = "T O T A L"


                fa_budget_period = Fa_budget_period()
                fa_budget_period_list.append(fa_budget_period)

                grand_total_qty = grand_total_qty + period_qty
                grand_total_amount =  to_decimal(grand_total_amount) + to_decimal(period_amount)
                grand_total_budget =  to_decimal(grand_total_budget) + to_decimal(period_budget)
                grand_total_variance =  to_decimal(grand_total_variance) + to_decimal(period_variance)
                fa_budget_period = Fa_budget_period()
                fa_budget_period_list.append(fa_budget_period)

                fa_budget_period.anzahl_str = to_string(grand_total_qty, "->>,>>>,>>9")
                fa_budget_period.amount_str = to_string(grand_total_amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.variance_str = to_string(grand_total_variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.budget_str = to_string(grand_total_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.descrip_str = "GRAND TOTAL"


        else:

            fa_order_obj_list = {}
            for fa_order, fa_op, fa_artikel, mathis in db_session.query(Fa_order, Fa_op, Fa_artikel, Mathis).join(Fa_op,(Fa_op.loeschflag <= 1) & (Fa_op.opart == 1) & (Fa_op.anzahl > 0) & (Fa_op.docu_nr == Fa_order.Order_Nr) & (Fa_op.datum >= from_date) & (Fa_op.datum <= to_date)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
                     (Fa_order.ActiveReason != ("0").lower()) & (Fa_order.ActiveReason != "") & (Fa_order.ActiveReason != None)).order_by(Fa_order.activereason, Fa_op.nr, Fa_op.datum).yield_per(100):
                fix_asset_list = query(fix_asset_list_list, (lambda fix_asset_list: to_string(fix_asset_list.nr_budget) == fa_order.ActiveReason), first=True)
                if not fix_asset_list:
                    continue

                if fa_order_obj_list.get(fa_order._recid):
                    continue
                else:
                    fa_order_obj_list[fa_order._recid] = True


                count_i = count_i + 1

                if fa_order.ActiveReason.lower()  != (nr_budget).lower() :

                    if nr_budget != "":
                        fa_budget_period = Fa_budget_period()
                        fa_budget_period_list.append(fa_budget_period)

                        fa_budget_period.budget_str = to_string(period_budget, "->>>,>>>,>>>,>>>,>>9.99")
                        fa_budget_period.budget_date = budget_date_last
                        fa_budget_period.descrip_str = to_string(budget_nr_last) + " - " + budget_desc_last
                        fa_budget_period.account_no = to_string(budget_nr_last, ">,>>9")
                        fa_budget_period.anzahl_str = to_string(period_qty, "->>,>>>,>>9")
                        fa_budget_period.amount_str = to_string(period_amount, "->>>,>>>,>>>,>>>,>>9.99")
                        fa_budget_period.variance_str = to_string(period_variance, "->>>,>>>,>>>,>>>,>>9.99")


                        grand_total_qty = grand_total_qty + period_qty
                        grand_total_amount =  to_decimal(grand_total_amount) + to_decimal(period_amount)
                        grand_total_budget =  to_decimal(grand_total_budget) + to_decimal(period_budget)
                        grand_total_variance =  to_decimal(grand_total_variance) + to_decimal(period_variance)
                        period_budget =  to_decimal("0")
                        period_qty = 0
                        period_amount =  to_decimal("0")
                        period_variance =  to_decimal("0")
                    period_budget =  to_decimal(fix_asset_list.amount_budget)
                    nr_budget = fa_order.ActiveReason
                    budget_date_last = fix_asset_list.date_budget
                    budget_nr_last = fix_asset_list.nr_budget
                    budget_desc_last = fix_asset_list.desc_budget

                if fa_artnr != fa_op.nr:
                    period_qty = period_qty + fa_op.anzahl
                    period_amount =  to_decimal(period_amount) + to_decimal(fa_op.warenwert)
                    period_variance = ( to_decimal(period_budget) - to_decimal(period_amount))
                    fa_artnr = fa_op.nr

            if count_i > 0:
                fa_budget_period = Fa_budget_period()
                fa_budget_period_list.append(fa_budget_period)

                fa_budget_period.budget_str = to_string(period_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.budget_date = budget_date_last
                fa_budget_period.descrip_str = to_string(budget_nr_last) + " - " + budget_desc_last
                fa_budget_period.account_no = to_string(budget_nr_last, ">,>>9")
                fa_budget_period.anzahl_str = to_string(period_qty, "->>,>>>,>>9")
                fa_budget_period.amount_str = to_string(period_amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.variance_str = to_string(period_variance, "->>>,>>>,>>>,>>>,>>9.99")


                fa_budget_period = Fa_budget_period()
                fa_budget_period_list.append(fa_budget_period)

                grand_total_qty = grand_total_qty + period_qty
                grand_total_amount =  to_decimal(grand_total_amount) + to_decimal(period_amount)
                grand_total_budget =  to_decimal(grand_total_budget) + to_decimal(period_budget)
                grand_total_variance =  to_decimal(grand_total_variance) + to_decimal(period_variance)
                fa_budget_period = Fa_budget_period()
                fa_budget_period_list.append(fa_budget_period)

                fa_budget_period.anzahl_str = to_string(grand_total_qty, "->>,>>>,>>9")
                fa_budget_period.amount_str = to_string(grand_total_amount, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.variance_str = to_string(grand_total_variance, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.budget_str = to_string(grand_total_budget, "->>>,>>>,>>>,>>>,>>9.99")
                fa_budget_period.descrip_str = "T O T A L"


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 324)).order_by(Queasy._recid).all():
        fix_asset_list = Fix_asset_list()
        fix_asset_list_list.append(fix_asset_list)

        fix_asset_list.nr_budget = queasy.number1
        fix_asset_list.desc_budget = queasy.char1
        fix_asset_list.date_budget = queasy.date1
        fix_asset_list.amount_budget =  to_decimal(queasy.deci1)
        fix_asset_list.is_active_budget = queasy.logi1

    fa_order_obj_list = {}
    for fa_order, fa_op, fa_artikel, mathis in db_session.query(Fa_order, Fa_op, Fa_artikel, Mathis).join(Fa_op,(Fa_op.loeschflag <= 1) & (Fa_op.opart == 1) & (Fa_op.anzahl > 0) & (Fa_op.docu_nr == Fa_order.Order_Nr) & (Fa_op.datum >= start_jan) & (Fa_op.datum <= ytd_date)).join(Fa_artikel,(Fa_artikel.nr == Fa_op.nr)).join(Mathis,(Mathis.nr == Fa_op.nr)).filter(
             (Fa_order.ActiveReason != ("0").lower()) & (Fa_order.ActiveReason != "") & (Fa_order.ActiveReason != None)).order_by(Fa_order.activereason, Fa_op.nr, Fa_op.datum).yield_per(100):
        fix_asset_list = query(fix_asset_list_list, (lambda fix_asset_list: to_string(fix_asset_list.nr_budget) == fa_order.ActiveReason), first=True)
        if not fix_asset_list:
            continue

        if fa_order_obj_list.get(fa_order._recid):
            continue
        else:
            fa_order_obj_list[fa_order._recid] = True


        fa_artnr = fa_op.nr
        break

    if ytd_flag:
        create_budget_ytd()
    else:
        create_budget_period()

    return generate_output()