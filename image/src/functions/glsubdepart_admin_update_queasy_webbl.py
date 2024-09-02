from functions.additional_functions import *
import decimal
from models import Queasy

def glsubdepart_admin_update_queasy_webbl(curr_mode:str, t_gl_depart_nr:int, t_queasy:[T_queasy], g_list:[G_list]):
    new_number:int = 1
    queasy = None

    g_list = t_queasy = queasy1 = None

    g_list_list, G_list = create_model_like(Queasy)
    t_queasy_list, T_queasy = create_model_like(Queasy)

    Queasy1 = T_queasy
    queasy1_list = t_queasy_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal new_number, queasy
        nonlocal queasy1


        nonlocal g_list, t_queasy, queasy1
        nonlocal g_list_list, t_queasy_list
        return {}


    g_list = query(g_list_list, first=True)

    if curr_mode.lower()  == "add":

        for g_list in query(g_list_list):
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(g_list, t_queasy)

        for queasy1 in query(queasy1_list):
            new_number = queasy1.number1 + 1
            break
        t_queasy.number1 = new_number
        t_queasy.number2 = t_gl_depart_nr

        for t_queasy in query(t_queasy_list):

            g_list = query(g_list_list, filters=(lambda g_list :g_list.key == t_queasy.key and g_list.char1 == t_queasy.char1), first=True)

            if g_list:
                buffer_copy(t_queasy, g_list)

                g_list = query(g_list_list, current=True)


    elif curr_mode.lower()  == "chg":

        for g_list in query(g_list_list):

            t_queasy = query(t_queasy_list, filters=(lambda t_queasy :t_queasy.key == g_list.key and t_queasy.char1 == g_list.char1), first=True)

            if t_queasy:
                buffer_copy(g_list, t_queasy)
                t_queasy.number2 = t_gl_depart_nr

                t_queasy = query(t_queasy_list, current=True)


    return generate_output()