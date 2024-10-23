from functions.additional_functions import *
import decimal
from models import Bediener, Queasy

t_bediener_list, T_bediener = create_model_like(Bediener)
t_queasy_list, T_queasy = create_model_like(Queasy)

def benutzer_adminbl(case_type:int, mphone:str, email:str, pager:str, t_bediener_list:[T_bediener], t_queasy_list:[T_queasy]):
    bediener = queasy = None

    t_bediener = t_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, queasy
        nonlocal case_type, mphone, email, pager


        nonlocal t_bediener, t_queasy
        nonlocal t_bediener_list, t_queasy_list
        return {}


    if case_type == 1:

        t_bediener = query(t_bediener_list, first=True)

        if t_bediener:
            bediener = Bediener()
            db_session.add(bediener)

            buffer_copy(t_bediener, bediener)

        t_queasy = query(t_queasy_list, first=True)

        if t_queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)
    else:

        t_bediener = query(t_bediener_list, first=True)

        if t_bediener:

            bediener = db_session.query(Bediener).filter(
                     (Bediener.nr == t_bediener.nr)).first()

            if bediener:
                buffer_copy(t_bediener, bediener)
                pass

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 134) & (Queasy.number1 == t_bediener.nr)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 134


        else:
            pass
        queasy.number1 = t_bediener.nr
        queasy.char1 = mphone
        queasy.char2 = email
        queasy.char3 = pager

    return generate_output()