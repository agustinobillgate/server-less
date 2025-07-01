#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_list, T_queasy = create_model_like(Queasy)
g_list_list, G_list = create_model_like(Queasy)

def glsubdepart_admin_update_queasy_webbl(curr_mode:string, t_gl_depart_nr:int, t_queasy_list:[T_queasy], g_list_list:[G_list]):
    new_number:int = 1
    queasy = None

    g_list = t_queasy = queasy1 = None

    Queasy1 = T_queasy
    queasy1_list = t_queasy_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_number, queasy
        nonlocal curr_mode, t_gl_depart_nr
        nonlocal queasy1


        nonlocal g_list, t_queasy, queasy1

        return {"t-queasy": t_queasy_list, "g-list": g_list_list}


    g_list = query(g_list_list, first=True)

    if curr_mode.lower()  == ("add").lower() :

        for g_list in query(g_list_list):
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(g_list, t_queasy)

        for queasy1 in query(queasy1_list, sort_by=[("number1",True)]):
            new_number = queasy1.number1 + 1
            break
        t_queasy.number1 = new_number
        t_queasy.number2 = t_gl_depart_nr

        for t_queasy in query(t_queasy_list):

            g_list = query(g_list_list, filters=(lambda g_list: g_list.key == t_queasy.key and g_list.char1 == t_queasy.char1), first=True)

            if g_list:
                buffer_copy(t_queasy, g_list)
                pass
                pass

    elif curr_mode.lower()  == ("chg").lower() :

        for g_list in query(g_list_list):

            t_queasy = query(t_queasy_list, filters=(lambda t_queasy: t_queasy.key == g_list.key and t_queasy.char1 == g_list.char1), first=True)

            if t_queasy:
                buffer_copy(g_list, t_queasy)
                t_queasy.number2 = t_gl_depart_nr


                pass
                pass

    return generate_output()