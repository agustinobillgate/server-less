from functions.additional_functions import *
import decimal
from datetime import date
from functions.fb_cost_count_recipe_costbl import fb_cost_count_recipe_costbl
from models import H_artikel, Queasy

def fb_cost_fill_grid_listbl(double_currency:bool, sorttype:int, dept:int, exchg_rate:decimal, price_type:int):
    amount = 0
    grid_list_list = []
    h_artikel = queasy = None

    grid_list = None

    grid_list_list, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":str, "artnrrezept":int, "unitprice":decimal, "recipecost":decimal, "cpercentage":decimal, "recomcost":decimal, "recomprice":decimal, "next__unit__price":decimal, "next__2nd__price":decimal, "changeddate":date, "users":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, grid_list_list, h_artikel, queasy


        nonlocal grid_list
        nonlocal grid_list_list
        return {"amount": amount, "grid-list": grid_list_list}

    def count_recipe_cost():

        nonlocal amount, grid_list_list, h_artikel, queasy


        nonlocal grid_list
        nonlocal grid_list_list


        amount = get_output(fb_cost_count_recipe_costbl(grid_list.artnrrezept, price_type, amount))
        grid_list.recipecost = amount

    def count_cost_percentage():

        nonlocal amount, grid_list_list, h_artikel, queasy


        nonlocal grid_list
        nonlocal grid_list_list


        grid_list.cpercentage = grid_list.recipecost / grid_list.unitprice * 100

    if sorttype == 3:

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.departement == dept)).all():
            grid_list = Grid_list()
            grid_list_list.append(grid_list)

            grid_list.artnr = h_artikel.artnr
            grid_list.artnrrezept = h_artikel.artnrrezept
            grid_list.subgroup = h_artikel.zwkum
            grid_list.bezeich = h_artikel.bezeich
            grid_list.unitprice = h_artikel.epreis1
            grid_list.recipecost = 0

            if double_currency:
                grid_list.unitprice = grid_list.unitprice * exchg_rate
            amount = 0
            count_recipe_cost()
            count_cost_percentage()

            queasy = db_session.query(Queasy).filter(
                    (Queasy.KEY == 142) &  (grid_list.artnr == Queasy.number1) &  (Queasy.dept == Queasy.number2)).first()

            if queasy:
                grid_list.NEXT__unit__price = queasy.deci1
                grid_list.Next__2nd__price = queasy.deci2
                grid_list.changeddate = queasy.date1
                grid_list.USERs = queasy.char2

    elif sorttype == 2:

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.departement == dept) &  (H_artikel.artnrrezept != 0)).all():
            grid_list = Grid_list()
            grid_list_list.append(grid_list)

            grid_list.artnr = h_artikel.artnr
            grid_list.artnrrezept = h_artikel.artnrrezept
            grid_list.subgroup = h_artikel.zwkum
            grid_list.bezeich = h_artikel.bezeich
            grid_list.unitprice = h_artikel.epreis1
            grid_list.recipecost = 0

            if double_currency:
                grid_list.unitprice = grid_list.unitprice * exchg_rate
            amount = 0
            count_recipe_cost()
            count_cost_percentage()

            queasy = db_session.query(Queasy).filter(
                    (Queasy.KEY == 142) &  (grid_list.artnr == Queasy.number1) &  (Queasy.dept == Queasy.number2)).first()

            if queasy:
                grid_list.NEXT__unit__price = queasy.deci1
                grid_list.Next__2nd__price = queasy.deci2
                grid_list.changeddate = queasy.date1
                grid_list.USERs = queasy.char2


    else:

        for h_artikel in db_session.query(H_artikel).filter(
                (H_artikel.departement == dept) &  (H_artikel.artnrrezept == 0)).all():
            grid_list = Grid_list()
            grid_list_list.append(grid_list)

            grid_list.artnr = h_artikel.artnr
            grid_list.artnrrezept = h_artikel.artnrrezept
            grid_list.subgroup = h_artikel.zwkum
            grid_list.bezeich = h_artikel.bezeich
            grid_list.unitprice = h_artikel.epreis1
            grid_list.recipecost = 0
            grid_list.cpercentage = 0

            if double_currency:
                grid_list.unitprice = grid_list.unitprice * exchg_rate

            queasy = db_session.query(Queasy).filter(
                    (Queasy.KEY == 142) &  (grid_list.artnr == Queasy.number1) &  (Queasy.dept == Queasy.number2)).first()

            if queasy:
                grid_list.NEXT__unit__price = queasy.deci1
                grid_list.Next__2nd__price = queasy.deci2
                grid_list.changeddate = queasy.date1
                grid_list.USERs = queasy.char2

    return generate_output()