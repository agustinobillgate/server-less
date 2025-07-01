#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Fa_order, Fa_op

def get_fix_asset_budget_webbl(search_by_desc:string, retrieve_for:string):

    prepare_cache ([Queasy, Fa_order, Fa_op])

    fix_asset_list_list = []
    queasy = fa_order = fa_op = None

    fix_asset_list = None

    fix_asset_list_list, Fix_asset_list = create_model("Fix_asset_list", {"nr_budget":int, "desc_budget":string, "date_budget":date, "amount_budget":Decimal, "is_active_budget":bool, "safe_to_del_or_mod":bool, "remain_budget":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fix_asset_list_list, queasy, fa_order, fa_op
        nonlocal search_by_desc, retrieve_for


        nonlocal fix_asset_list
        nonlocal fix_asset_list_list

        return {"fix-asset-list": fix_asset_list_list}

    def retrieve_it1a():

        nonlocal fix_asset_list_list, queasy, fa_order, fa_op
        nonlocal search_by_desc, retrieve_for


        nonlocal fix_asset_list
        nonlocal fix_asset_list_list

        t_warenwert:Decimal = 0.0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 324)).order_by(Queasy._recid).all():
            t_warenwert =  to_decimal(0.0)
            fix_asset_list = Fix_asset_list()
            fix_asset_list_list.append(fix_asset_list)

            fix_asset_list.nr_budget = queasy.number1
            fix_asset_list.desc_budget = queasy.char1
            fix_asset_list.date_budget = queasy.date1
            fix_asset_list.amount_budget =  to_decimal(queasy.deci1)
            fix_asset_list.is_active_budget = queasy.logi1

            fa_order = get_cache (Fa_order, {"activereason": [(eq, to_string(queasy.number1))]})

            if not fa_order:
                fix_asset_list.safe_to_del_or_mod = True

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.ActiveReason == to_string(queasy.number1))).order_by(Fa_order._recid).all():

                fa_op = get_cache (Fa_op, {"loeschflag": [(le, 1)],"opart": [(eq, 1)],"anzahl": [(gt, 0)],"docu_nr": [(eq, fa_order.order_nr)]})

                if fa_op:
                    t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
            fix_asset_list.remain_budget =  to_decimal(queasy.deci1) - to_decimal(t_warenwert)


    def retrieve_it1b():

        nonlocal fix_asset_list_list, queasy, fa_order, fa_op
        nonlocal search_by_desc, retrieve_for


        nonlocal fix_asset_list
        nonlocal fix_asset_list_list

        t_warenwert:Decimal = 0.0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 324) & (matches(Queasy.char1,"*" + search_by_desc + "*"))).order_by(Queasy._recid).all():
            t_warenwert =  to_decimal(0.0)
            fix_asset_list = Fix_asset_list()
            fix_asset_list_list.append(fix_asset_list)

            fix_asset_list.nr_budget = queasy.number1
            fix_asset_list.desc_budget = queasy.char1
            fix_asset_list.date_budget = queasy.date1
            fix_asset_list.amount_budget =  to_decimal(queasy.deci1)
            fix_asset_list.is_active_budget = queasy.logi1

            fa_order = get_cache (Fa_order, {"activereason": [(eq, to_string(queasy.number1))]})

            if not fa_order:
                fix_asset_list.safe_to_del_or_mod = True

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.ActiveReason == to_string(queasy.number1))).order_by(Fa_order._recid).all():

                fa_op = get_cache (Fa_op, {"loeschflag": [(le, 1)],"opart": [(eq, 1)],"anzahl": [(gt, 0)],"docu_nr": [(eq, fa_order.order_nr)]})

                if fa_op:
                    t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
            fix_asset_list.remain_budget =  to_decimal(queasy.deci1) - to_decimal(t_warenwert)


    def retrieve_it2a():

        nonlocal fix_asset_list_list, queasy, fa_order, fa_op
        nonlocal search_by_desc, retrieve_for


        nonlocal fix_asset_list
        nonlocal fix_asset_list_list

        t_warenwert:Decimal = 0.0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 324) & (Queasy.logi1)).order_by(Queasy._recid).all():
            t_warenwert =  to_decimal(0.0)
            fix_asset_list = Fix_asset_list()
            fix_asset_list_list.append(fix_asset_list)

            fix_asset_list.nr_budget = queasy.number1
            fix_asset_list.desc_budget = to_string(queasy.number1) + " - " + queasy.char1
            fix_asset_list.date_budget = queasy.date1
            fix_asset_list.amount_budget =  to_decimal(queasy.deci1)
            fix_asset_list.is_active_budget = queasy.logi1

            fa_order = get_cache (Fa_order, {"activereason": [(eq, to_string(queasy.number1))]})

            if not fa_order:
                fix_asset_list.safe_to_del_or_mod = True

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.ActiveReason == to_string(queasy.number1))).order_by(Fa_order._recid).all():

                fa_op = get_cache (Fa_op, {"loeschflag": [(le, 1)],"opart": [(eq, 1)],"anzahl": [(gt, 0)],"docu_nr": [(eq, fa_order.order_nr)]})

                if fa_op:
                    t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
            fix_asset_list.remain_budget =  to_decimal(queasy.deci1) - to_decimal(t_warenwert)


    def retrieve_it2b():

        nonlocal fix_asset_list_list, queasy, fa_order, fa_op
        nonlocal search_by_desc, retrieve_for


        nonlocal fix_asset_list
        nonlocal fix_asset_list_list

        t_warenwert:Decimal = 0.0

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 324) & (Queasy.logi1) & (matches(Queasy.char1,"*" + search_by_desc + "*"))).order_by(Queasy._recid).all():
            t_warenwert =  to_decimal(0.0)
            fix_asset_list = Fix_asset_list()
            fix_asset_list_list.append(fix_asset_list)

            fix_asset_list.nr_budget = queasy.number1
            fix_asset_list.desc_budget = to_string(queasy.number1) + " - " + queasy.char1
            fix_asset_list.date_budget = queasy.date1
            fix_asset_list.amount_budget =  to_decimal(queasy.deci1)
            fix_asset_list.is_active_budget = queasy.logi1

            fa_order = get_cache (Fa_order, {"activereason": [(eq, to_string(queasy.number1))]})

            if not fa_order:
                fix_asset_list.safe_to_del_or_mod = True

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.ActiveReason == to_string(queasy.number1))).order_by(Fa_order._recid).all():

                fa_op = get_cache (Fa_op, {"loeschflag": [(le, 1)],"opart": [(eq, 1)],"anzahl": [(gt, 0)],"docu_nr": [(eq, fa_order.order_nr)]})

                if fa_op:
                    t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
            fix_asset_list.remain_budget =  to_decimal(queasy.deci1) - to_decimal(t_warenwert)


    if retrieve_for.lower()  == ("setting").lower() :

        if search_by_desc == " ":
            retrieve_it1a()
        else:
            retrieve_it1b()

    elif retrieve_for.lower()  == ("purchase-order").lower() :

        if search_by_desc == " ":
            retrieve_it2a()
        else:
            retrieve_it2b()

    return generate_output()