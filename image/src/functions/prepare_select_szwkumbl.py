from functions.additional_functions import *
import decimal
from models import L_untergrup, Queasy

def prepare_select_szwkumbl(main_nr:int):
    szwkum_list_list = []
    l_untergrup = queasy = None

    szwkum_list = None

    szwkum_list_list, Szwkum_list = create_model("Szwkum_list", {"zwkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal szwkum_list_list, l_untergrup, queasy


        nonlocal szwkum_list
        nonlocal szwkum_list_list
        return {"szwkum-list": szwkum_list_list}

    if main_nr == 0:

        for l_untergrup in db_session.query(L_untergrup).all():
            szwkum_list = Szwkum_list()
            szwkum_list_list.append(szwkum_list)

            buffer_copy(l_untergrup, szwkum_list)
    else:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 29) &  (Queasy.number1 == main_nr)).all():

            l_untergrup = db_session.query(L_untergrup).filter(
                    (L_untergrup.zwkum == queasy.number2)).first()

            if l_untergrup:

                szwkum_list = query(szwkum_list_list, filters=(lambda szwkum_list :szwkum_list.zwkum == l_untergrup.zwkum), first=True)

                if not szwkum_list:
                    szwkum_list = Szwkum_list()
                    szwkum_list_list.append(szwkum_list)

                    buffer_copy(l_untergrup, szwkum_list)

        for l_untergrup in db_session.query(L_untergrup).all():

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 29) &  (Queasy.number2 == l_untergrup.zwkum)).first()

            if not queasy:
                szwkum_list = Szwkum_list()
                szwkum_list_list.append(szwkum_list)

                buffer_copy(l_untergrup, szwkum_list)

    return generate_output()