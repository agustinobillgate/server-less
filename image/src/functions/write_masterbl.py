from functions.additional_functions import *
import decimal
from models import Master

def write_masterbl(t_master:[T_master]):
    success_flag = False
    master = None

    t_master = None

    t_master_list, T_master = create_model_like(Master)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, master


        nonlocal t_master
        nonlocal t_master_list
        return {"success_flag": success_flag}

    t_master = query(t_master_list, first=True)

    master = db_session.query(Master).filter(
            (Master.resnr == t_Master.resnr)).first()

    if not master:
        master = Master()
    db_session.add(master)

    buffer_copy(t_master, master)

    success_flag = True

    return generate_output()