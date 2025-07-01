#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, Queasy

def prepare_select_szwkumbl(main_nr:int):

    prepare_cache ([Queasy])

    szwkum_list_list = []
    l_untergrup = queasy = None

    szwkum_list = None

    szwkum_list_list, Szwkum_list = create_model("Szwkum_list", {"zwkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal szwkum_list_list, l_untergrup, queasy
        nonlocal main_nr


        nonlocal szwkum_list
        nonlocal szwkum_list_list

        return {"szwkum-list": szwkum_list_list}

    if main_nr == 0:

        for l_untergrup in db_session.query(L_untergrup).order_by(L_untergrup._recid).all():
            szwkum_list = Szwkum_list()
            szwkum_list_list.append(szwkum_list)

            buffer_copy(l_untergrup, szwkum_list)
    else:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 29) & (Queasy.number1 == main_nr)).order_by(Queasy.number2).all():

            l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, queasy.number2)]})

            if l_untergrup:

                szwkum_list = query(szwkum_list_list, filters=(lambda szwkum_list: szwkum_list.zwkum == l_untergrup.zwkum), first=True)

                if not szwkum_list:
                    szwkum_list = Szwkum_list()
                    szwkum_list_list.append(szwkum_list)

                    buffer_copy(l_untergrup, szwkum_list)

        for l_untergrup in db_session.query(L_untergrup).order_by(L_untergrup.zwkum).all():

            queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_untergrup.zwkum)]})

            if not queasy:
                szwkum_list = Szwkum_list()
                szwkum_list_list.append(szwkum_list)

                buffer_copy(l_untergrup, szwkum_list)

    return generate_output()