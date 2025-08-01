#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 1/8/2025
# if available
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Eg_action

action_data, Action = create_model_like(Eg_action)

def eg_action_btn_exitbl(action_data:[Action], case_type:int, rec_id:int, user_init:string, a:int):

    prepare_cache ([Eg_action])

    fl_code = 0
    eg_action = None

    action = queri = None

    Queri = create_buffer("Queri",Eg_action)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_action
        nonlocal case_type, rec_id, user_init, a
        nonlocal queri


        nonlocal action, queri

        return {"fl_code": fl_code}

    action = query(action_data, first=True)

    if case_type == 1:
        eg_action = Eg_action()
        db_session.add(eg_action)

        buffer_copy(action, eg_action)

    elif case_type == 2:

        eg_action = get_cache (Eg_action, {"_recid": [(eq, rec_id)]})

        # Rd, 1/8/2025
        if eg_action:
            queri = get_cache (Eg_action, {"actionnr": [(eq, action.actionnr)],"_recid": [(ne, eg_action._recid)]})

            if queri:
                fl_code = 1

                return generate_output()
            else:

                queri = get_cache (Eg_action, {"bezeich": [(eq, action.bezeich)],"maintask": [(eq, action.maintask)],"_recid": [(ne, eg_action._recid)]})

                if queri:
                    fl_code = 2

                    return generate_output()
                else:
                    pass
                    buffer_copy(action, eg_action)
                    eg_action.usefor = a


                    pass
                    fl_code = 3

    return generate_output()