from functions.additional_functions import *
import decimal
import re
from functions.write_queasybl import write_queasybl
from models import Queasy

def ratecode_additional_ok_webbl(g_list:[G_list], t_queasy:[T_queasy]):
    success_flag:bool = False
    queasy = None

    t_queasy = g_list = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    g_list_list, G_list = create_model("G_list", {"rcode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy


        nonlocal t_queasy, g_list
        nonlocal t_queasy_list, g_list_list
        return {}


    t_queasy = query(t_queasy_list, first=True)

    if re.match(".*;.*",t_queasy.char3):
        t_queasy.char3 = entry(0, t_queasy.char3, ";") + ";"


    else:
        t_queasy.char3 = ";"

    for g_list in query(g_list_list):
        t_queasy.char3 = t_queasy.char3 + g_list.rcode + ","
    t_queasy.char3 = t_queasy.char3 + ";"
    success_flag = get_output(write_queasybl(6, t_queasy, t_queasy))

    return generate_output()