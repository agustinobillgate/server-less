#using conversion tools version: 1.0.0.23
#------------------------------------------
# Rd, 3/12/2025, Locking Test
#------------------------------------------
from functions.additional_functions import *
import decimal
from models import Master

t_master_list, T_master = create_model_like(Master)

def i_update_masterbl(t_master_list:[T_master]):
    success_flag = False
    master = None

    t_master = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, master


        nonlocal t_master

        return {"success_flag": success_flag}

    t_master = query(t_master_list, first=True)

    master = db_session.query(Master).filter(
             (Master.resnr == t_master.resnr)).first()

    if not master:
        master = Master()
    db_session.add(master)

    buffer_copy(t_master, master)
    pass
    success_flag = True

    return generate_output()