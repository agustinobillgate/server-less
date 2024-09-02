from functions.additional_functions import *
import decimal
from models import Eg_action

def eg_action_btn_exitbl(action:[Action], case_type:int, rec_id:int, user_init:str, a:int):
    fl_code = 0
    eg_action = None

    action = queri = None

    action_list, Action = create_model_like(Eg_action)

    Queri = Eg_action

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_action
        nonlocal queri


        nonlocal action, queri
        nonlocal action_list
        return {"fl_code": fl_code}

    action = query(action_list, first=True)

    if case_type == 1:
        eg_action = Eg_action()
        db_session.add(eg_action)

        buffer_copy(action, eg_action)

    elif case_type == 2:

        eg_action = db_session.query(Eg_action).filter(
                (Eg_action._recid == rec_id)).first()

        queri = db_session.query(Queri).filter(
                (Queri.actionnr == action.actionnr) &  (Queri._recid != eg_action._recid)).first()

        if queri:
            fl_code = 1

            return generate_output()
        else:

            queri = db_session.query(Queri).filter(
                    (Queri.bezeich == action.bezeich) &  (Queri.maintask == action.maintask) &  (Queri._recid != eg_action._recid)).first()

            if queri:
                fl_code = 2

                return generate_output()
            else:

                eg_action = db_session.query(Eg_action).first()
                buffer_copy(action, eg_action)
                eg_action.usefor = a

                eg_action = db_session.query(Eg_action).first()
                fl_code = 3

    return generate_output()