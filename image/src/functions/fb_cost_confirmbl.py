from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy

def fb_cost_confirmbl(price_list_artnr:int, price_list_deptnr:int, price_list_date1:date, price_list_date2:date, price_list_date3:date, price_list_deci1:decimal, price_list_deci2:decimal, tp_bediener_username:str):
    grid_list_list = []
    queasy = None

    grid_list = None

    grid_list_list, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":str, "artnrrezept":int, "unitprice":decimal, "recipecost":decimal, "cpercentage":decimal, "recomcost":decimal, "recomprice":decimal, "next__unit__price":decimal, "next__2nd__price":decimal, "changeddate":date, "users":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal grid_list_list, queasy


        nonlocal grid_list
        nonlocal grid_list_list
        return {"grid-list": grid_list_list}

    def fill_queasy():

        nonlocal grid_list_list, queasy


        nonlocal grid_list
        nonlocal grid_list_list


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 142
        queasy.number1 = price_list_artnr
        queasy.number2 = price_list_deptnr
        queasy.deci1 = price_list_deci1
        queasy.deci2 = price_list_deci2
        queasy.date1 = price_list_date1
        queasy.date2 = price_list_date2
        queasy.date3 = price_list_date3
        queasy.char2 = tp_bediener_username


        grid_list = Grid_list()
        grid_list_list.append(grid_list)

        grid_list.NEXT__unit__price = queasy.deci1
        grid_list.Next__2nd__price = queasy.deci2
        grid_list.changeddate = queasy.date1
        grid_list.users = queasy.char2

    queasy = db_session.query(Queasy).filter(
            (Queasy.KEY == 142) &  (Queasy.number1 == price_list_artnr) &  (Queasy.number2 == price_list_deptnr) &  (Queasy.date1 == price_list_date1) &  (Queasy.deci1 == price_list_deci1) &  (Queasy.deci2 == price_list_deci2)).first()

    if queasy:

        return generate_output()

    queasy = db_session.query(Queasy).filter(
                (Queasy.KEY == 142) &  (Queasy.number1 == price_list_artnr) &  (Queasy.number2 == price_list_deptnr) &  (Queasy.date1 == price_list_date1)).first()

    if queasy:
        db_session.delete(queasy)

    fill_queasy()
    grid_list = Grid_list()
    grid_list_list.append(grid_list)

    grid_list.NEXT__unit__price = price_list_deci1
    grid_list.NEXT__2nd__price = price_list_deci2
    grid_list.changeddate = price_list_date1

    return generate_output()