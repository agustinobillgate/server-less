#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#----------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_func
from sqlalchemy.orm.attributes import flag_modified

meal_list_data, Meal_list = create_model("Meal_list", {"nr":int, "meals":string, "times":string, "venue":string, "pax":int, "setup":string})

def banquet_meals_btngobl(meal_list_data:[Meal_list], resno:int, reslinno:int):

    prepare_cache ([Bk_func])

    str:string = ""
    bk_func = None

    meal_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, bk_func
        nonlocal resno, reslinno


        nonlocal meal_list

        return {}

    for meal_list in query(meal_list_data):
        str = str + "|" + to_string(meal_list.nr) + ";" +\
                to_string(meal_list.meals) + ";" +\
                to_string(meal_list.times) + ";" +\
                to_string(meal_list.venue) + ";" +\
                to_string(meal_list.pax) + ";" +\
                to_string(meal_list.setup)

    # bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resno)],"veran_seite": [(eq, reslinno)]})
    bk_func = db_session.query(Bk_func).filter(
             (Bk_func.veran_nr == resno) &
             (Bk_func.veran_seite == reslinno)).with_for_update().first()

    if bk_func:

        if num_entries(bk_func.f_menu[0], "$") > 1:
            bk_func.f_menu[0] = entry(1, bk_func.f_menu[0], "$", "")
            bk_func.f_menu[0] = entry(1, bk_func.f_menu[0], "$", str)


        else:
            bk_func.f_menu[0] = bk_func.f_menu[0] + "$" + str
    
    flag_modified(bk_func, "f_menu")


    return generate_output()