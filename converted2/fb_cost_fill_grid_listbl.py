#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import H_artikel, Queasy

def fb_cost_fill_grid_listbl(double_currency:bool, sorttype:int, dept:int, exchg_rate:Decimal, price_type:int):

    prepare_cache ([H_artikel, Queasy])

    amount = to_decimal("0.0")
    grid_list_data = []
    h_artikel = queasy = None

    grid_list = None

    grid_list_data, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":string, "artnrrezept":int, "unitprice":Decimal, "recipecost":Decimal, "cpercentage":Decimal, "recomcost":Decimal, "recomprice":Decimal, "next__unit__price":Decimal, "next__2nd__price":Decimal, "changeddate":date, "users":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, grid_list_data, h_artikel, queasy
        nonlocal double_currency, sorttype, dept, exchg_rate, price_type


        nonlocal grid_list
        nonlocal grid_list_data

        return {"amount": amount, "grid-list": grid_list_data}

    def count_recipe_cost():

        nonlocal amount, grid_list_data, h_artikel, queasy
        nonlocal double_currency, sorttype, dept, exchg_rate, price_type


        nonlocal grid_list
        nonlocal grid_list_data


        amount = get_output(fb_cost_count_recipe_costbl(grid_list.artnrrezept, price_type, amount))
        grid_list.recipecost =  to_decimal(amount)


    def count_cost_percentage():

        nonlocal amount, grid_list_data, h_artikel, queasy
        nonlocal double_currency, sorttype, dept, exchg_rate, price_type


        nonlocal grid_list
        nonlocal grid_list_data

        tmp_pct:Decimal = to_decimal("0.0")

        if grid_list.unitprice > 0:
            tmp_pct =  to_decimal(grid_list.recipecost) / to_decimal(grid_list.unitprice)
        grid_list.cpercentage =  to_decimal(tmp_pct) * to_decimal("100")


    if sorttype == 3:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept)).order_by(H_artikel.artnr).all():
            grid_list = Grid_list()
            grid_list_data.append(grid_list)

            grid_list.artnr = h_artikel.artnr
            grid_list.artnrrezept = h_artikel.artnrrezept
            grid_list.subgroup = h_artikel.zwkum
            grid_list.bezeich = h_artikel.bezeich
            grid_list.unitprice =  to_decimal(h_artikel.epreis1)
            grid_list.recipecost =  to_decimal("0")

            if double_currency:
                grid_list.unitprice =  to_decimal(grid_list.unitprice) * to_decimal(exchg_rate)
            amount =  to_decimal("0")
            count_recipe_cost()
            count_cost_percentage()

            queasy = get_cache (Queasy, {"key": [(eq, 142)],"number1": [(eq, grid_list.artnr)],"number2": [(eq, dept)]})

            if queasy:
                grid_list.next__unit__price =  to_decimal(queasy.deci1)
                grid_list.next__2nd__price =  to_decimal(queasy.deci2)
                grid_list.changeddate = queasy.date1
                grid_list.users = queasy.char2

    elif sorttype == 2:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artnrrezept != 0)).order_by(H_artikel.artnr).all():
            grid_list = Grid_list()
            grid_list_data.append(grid_list)

            grid_list.artnr = h_artikel.artnr
            grid_list.artnrrezept = h_artikel.artnrrezept
            grid_list.subgroup = h_artikel.zwkum
            grid_list.bezeich = h_artikel.bezeich
            grid_list.unitprice =  to_decimal(h_artikel.epreis1)
            grid_list.recipecost =  to_decimal("0")

            if double_currency:
                grid_list.unitprice =  to_decimal(grid_list.unitprice) * to_decimal(exchg_rate)
            amount =  to_decimal("0")
            count_recipe_cost()
            count_cost_percentage()

            queasy = get_cache (Queasy, {"key": [(eq, 142)],"number1": [(eq, grid_list.artnr)],"number2": [(eq, dept)]})

            if queasy:
                grid_list.next__unit__price =  to_decimal(queasy.deci1)
                grid_list.next__2nd__price =  to_decimal(queasy.deci2)
                grid_list.changeddate = queasy.date1
                grid_list.users = queasy.char2


    else:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artnrrezept == 0)).order_by(H_artikel.artnr).all():
            grid_list = Grid_list()
            grid_list_data.append(grid_list)

            grid_list.artnr = h_artikel.artnr
            grid_list.artnrrezept = h_artikel.artnrrezept
            grid_list.subgroup = h_artikel.zwkum
            grid_list.bezeich = h_artikel.bezeich
            grid_list.unitprice =  to_decimal(h_artikel.epreis1)
            grid_list.recipecost =  to_decimal("0")
            grid_list.cpercentage =  to_decimal("0")

            if double_currency:
                grid_list.unitprice =  to_decimal(grid_list.unitprice) * to_decimal(exchg_rate)

            queasy = get_cache (Queasy, {"key": [(eq, 142)],"number1": [(eq, grid_list.artnr)],"number2": [(eq, dept)]})

            if queasy:
                grid_list.next__unit__price =  to_decimal(queasy.deci1)
                grid_list.next__2nd__price =  to_decimal(queasy.deci2)
                grid_list.changeddate = queasy.date1
                grid_list.users = queasy.char2

    return generate_output()