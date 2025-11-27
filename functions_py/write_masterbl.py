#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Master

t_master_data, T_master = create_model_like(Master)

def write_masterbl(t_master_data:[T_master]):

    prepare_cache ([Master])

    success_flag = False
    master = None

    t_master = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, master


        nonlocal t_master

        return {"success_flag": success_flag}

    t_master = query(t_master_data, first=True)

    master = db_session.query(Master).filter(Master.resnr == t_master.resnr).with_for_update().first()

    if not master:
        master = Master()
        db_session.add(master)


    if t_master.active != master.active:
        pass

    buffer_copy(t_master, master)

    success_flag = True

    return generate_output()