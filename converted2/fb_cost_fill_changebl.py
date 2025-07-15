#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import Queasy, H_artikel

def fb_cost_fill_changebl(double_currency:bool, exchg_rate:Decimal, price_type:int, dept:int):

    prepare_cache ([Queasy, H_artikel])

    amount = to_decimal("0.0")
    grid_list_data = []
    queasy = h_artikel = None

    grid_list = None

    grid_list_data, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":string, "artnrrezept":int, "unitprice":Decimal, "recipecost":Decimal, "cpercentage":Decimal, "recomcost":Decimal, "recomprice":Decimal, "next__unit__price":Decimal, "next__2nd__price":Decimal, "changeddate":date, "users":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, grid_list_data, queasy, h_artikel
        nonlocal double_currency, exchg_rate, price_type, dept


        nonlocal grid_list
        nonlocal grid_list_data

        return {"amount": amount, "grid-list": grid_list_data}

    def count_recipe_cost():

        nonlocal amount, grid_list_data, queasy, h_artikel
        nonlocal double_currency, exchg_rate, price_type, dept


        nonlocal grid_list
        nonlocal grid_list_data

        portion:Decimal = 1
        amount = get_output(fb_cost_count_recipe_costbl(grid_list.artnrrezept, price_type, amount))
        grid_list.recipecost =  to_decimal(amount)


    def count_cost_percentage():

        nonlocal amount, grid_list_data, queasy, h_artikel
        nonlocal double_currency, exchg_rate, price_type, dept


        nonlocal grid_list
        nonlocal grid_list_data


        grid_list.cpercentage =  to_decimal(grid_list.recipecost) / to_decimal(grid_list.unitprice) * to_decimal("100")


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 142) & (Queasy.date1 != None) & (Queasy.number2 == dept)).order_by(Queasy.number1).all():

        h_artikel = get_cache (H_artikel, {"artnr": [(eq, queasy.number1)],"departement": [(eq, dept)]})
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

        grid_list = query(grid_list_data, filters=(lambda grid_list: grid_list.artnr == queasy.number1), first=True)

        if grid_list:
            grid_list.next__unit__price =  to_decimal(queasy.deci1)
            grid_list.next__2nd__price =  to_decimal(queasy.deci2)
            grid_list.changeddate = queasy.date1
            grid_list.users = queasy.char2

    return generate_output()