from functions.additional_functions import *
import decimal
from models import Bk_func

def banquet_meals_btndelbl(resnr:int, reslinno:int, meal_list:[Meal_list]):
    str1:str = ""
    str:str = ""
    tokcounter:int = 0
    gpdelimiter:str = ";"
    mestoken:str = ""
    mesvalue:str = ""
    stringcount:int = 0
    getstring:str = ""
    bk_func = None

    meal_list = None

    meal_list_list, Meal_list = create_model("Meal_list", {"nr":int, "meals":str, "times":str, "venue":str, "pax":int, "setup":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str1, str, tokcounter, gpdelimiter, mestoken, mesvalue, stringcount, getstring, bk_func


        nonlocal meal_list
        nonlocal meal_list_list
        return {}

    for meal_list in query(meal_list_list):
        str1 = str1 + "|" + to_string(meal_list.nr) + ";" +\
                to_string(meal_list.meals) + ";" +\
                to_string(meal_list.times) + ";" +\
                to_string(meal_list.venue) + ";" +\
                to_string(meal_list.pax) + ";" +\
                to_string(meal_list.setup)

    bk_func = db_session.query(Bk_func).filter(
            (Bk_func.veran_nr == resnr) &  (Bk_func.veran_seite == reslinno)).first()

    if bk_func:

        if num_entries(bk_func.f_menu[0], "$") > 1:
            bk_func.f_menu[0] = entry(1, bk_func.f_menu[0], "$", "")


            bk_func.f_menu[0] = entry(1, bk_func.f_menu[0], "$", str1)


            str = entry(1, bk_func.f_menu[0], "$")


        else:
            bk_func.f_menu[0] = bk_func.f_menu[0] + "$" + str1


    for tokcounter in range(1,num_entries(str, "|")  + 1) :
        mestoken = entry(tokcounter - 1, str, "|")
        meal_list = Meal_list()
        meal_list_list.append(meal_list)


        if mestoken != "":
            for stringcount in range(1,num_entries(mestoken, gpdelimiter)  + 1) :
                getstring = entry(stringcount - 1, mestoken, gpdelimiter)

                if getstring == "":
                    break

                if stringcount == 1:
                    meal_list.nr = to_int(getstring)
                elif stringcount == 2:
                    meal_list.meals = getstring
                elif stringcount == 3:
                    meal_list.times = getstring
                elif stringcount == 4:
                    meal_list.venue = getstring
                elif stringcount == 5:
                    meal_list.pax = to_int(getstring)
                elif stringcount == 6:
                    meal_list.setup = getstring

    return generate_output()