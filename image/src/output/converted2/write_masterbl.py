#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Master

t_master_list, T_master = create_model_like(Master)

def write_masterbl(t_master_list:[T_master]):
    success_flag = False
    master = None

    t_master = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, master


        nonlocal t_master

        return {"success_flag": success_flag}

    t_master = query(t_master_list, first=True)

    master = get_cache (Master, {"resnr": [(eq, t_master.resnr)]})

    if not master:
        master = Master()
        db_session.add(master)

    buffer_copy(t_master, master)
    pass
    success_flag = True

    return generate_output()