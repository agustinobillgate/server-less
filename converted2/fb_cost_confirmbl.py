#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def fb_cost_confirmbl(price_list_artnr:int, price_list_deptnr:int, price_list_date1:date, price_list_date2:date, 
                      price_list_date3:date, price_list_deci1:Decimal, price_list_deci2:Decimal, tp_bediener_username:string):
    grid_list_data = []
    queasy = None

    grid_list = None

    grid_list_data, Grid_list = create_model("Grid_list", {"artnr":int, "subgroup":int, "bezeich":string, "artnrrezept":int, "unitprice":Decimal, "recipecost":Decimal, "cpercentage":Decimal, "recomcost":Decimal, "recomprice":Decimal, "next__unit__price":Decimal, "next__2nd__price":Decimal, "changeddate":date, "users":string})

    db_session = local_storage.db_session
    tp_bediener_username = tp_bediener_username.strip()

    def generate_output():
        nonlocal grid_list_data, queasy
        nonlocal price_list_artnr, price_list_deptnr, price_list_date1, price_list_date2, price_list_date3, price_list_deci1, price_list_deci2, tp_bediener_username


        nonlocal grid_list
        nonlocal grid_list_data

        return {"grid-list": grid_list_data}

    def fill_queasy():

        nonlocal grid_list_data, queasy
        nonlocal price_list_artnr, price_list_deptnr, price_list_date1, price_list_date2, price_list_date3, price_list_deci1, price_list_deci2, tp_bediener_username


        nonlocal grid_list
        nonlocal grid_list_data


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 142
        queasy.number1 = price_list_artnr
        queasy.number2 = price_list_deptnr
        queasy.deci1 =  to_decimal(price_list_deci1)
        queasy.deci2 =  to_decimal(price_list_deci2)
        queasy.date1 = price_list_date1
        queasy.date2 = price_list_date2
        queasy.date3 = price_list_date3
        queasy.char2 = tp_bediener_username


        grid_list = Grid_list()
        grid_list_data.append(grid_list)

        grid_list.next__unit__price =  to_decimal(queasy.deci1)
        grid_list.next__2nd__price =  to_decimal(queasy.deci2)
        grid_list.changeddate = queasy.date1
        grid_list.users = queasy.char2


    queasy = get_cache (Queasy, {"key": [(eq, 142)],"number1": [(eq, price_list_artnr)],"number2": [(eq, price_list_deptnr)],"date1": [(eq, price_list_date1)],"deci1": [(eq, price_list_deci1)],"deci2": [(eq, price_list_deci2)]})

    if queasy:

        return generate_output()

    # queasy = get_cache (Queasy, {"key": [(eq, 142)],"number1": [(eq, price_list_artnr)],"number2": [(eq, price_list_deptnr)],"date1": [(eq, price_list_date1)]})
    queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 142) &
                 (Queasy.number1 == price_list_artnr) &
                 (Queasy.number2 == price_list_deptnr) &
                 (Queasy.date1 == price_list_date1)).with_for_update().first()
    if queasy:
        db_session.delete(queasy)
        pass
    fill_queasy()
    grid_list = Grid_list()
    grid_list_data.append(grid_list)

    grid_list.next__unit__price =  to_decimal(price_list_deci1)
    grid_list.next__2nd__price =  to_decimal(price_list_deci2)
    grid_list.changeddate = price_list_date1

    return generate_output()