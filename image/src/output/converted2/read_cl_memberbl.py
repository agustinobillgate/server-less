#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Cl_member

def read_cl_memberbl(case_type:int, gastno:int):
    t_cl_member_list = []
    cl_member = None

    t_cl_member = None

    t_cl_member_list, T_cl_member = create_model_like(Cl_member)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_cl_member_list, cl_member
        nonlocal case_type, gastno


        nonlocal t_cl_member
        nonlocal t_cl_member_list

        return {"t-cl-member": t_cl_member_list}

    if case_type == 1:

        cl_member = get_cache (Cl_member, {"gastnr": [(eq, gastno)]})

        if cl_member:
            t_cl_member = T_cl_member()
            t_cl_member_list.append(t_cl_member)

            buffer_copy(cl_member, t_cl_member)

    return generate_output()