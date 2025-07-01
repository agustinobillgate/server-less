#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.write_queasybl import write_queasybl
from models import Queasy

g_list_list, G_list = create_model("G_list", {"rcode":string})
t_queasy_list, T_queasy = create_model_like(Queasy)

def ratecode_additional_ok_webbl(g_list_list:[G_list], t_queasy_list:[T_queasy]):
    success_flag:bool = False
    queasy = None

    t_queasy = g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, queasy


        nonlocal t_queasy, g_list

        return {}


    t_queasy = query(t_queasy_list, first=True)

    if matches(t_queasy.char3,r"*;*"):
        t_queasy.char3 = entry(0, t_queasy.char3, ";") + ";"


    else:
        t_queasy.char3 = ";"

    for g_list in query(g_list_list):
        t_queasy.char3 = t_queasy.char3 + g_list.rcode + ","
    t_queasy.char3 = t_queasy.char3 + ";"
    success_flag = get_output(write_queasybl(6, t_queasy_list, t_queasy_list))

    return generate_output()