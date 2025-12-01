#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Tisch

t_list_data, T_list = create_model_like(Tisch)

def rtable_admin_btn_exitbl(t_list_data:[T_list], case_type:int):

    prepare_cache ([Tisch])

    tisch = None

    t_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tisch
        nonlocal case_type


        nonlocal t_list

        return {}

    def fill_new_tisch():

        nonlocal tisch
        nonlocal case_type


        nonlocal t_list


        buffer_copy(t_list, tisch)

        if tisch.roomcharge:
            tisch.normalbeleg = 1


    t_list = query(t_list_data, first=True)

    if case_type == 1:
        tisch = Tisch()
        db_session.add(tisch)

        fill_new_tisch()

    elif case_type == 2:

        # tisch = get_cache (Tisch, {"departement": [(eq, t_list.departement)],"tischnr": [(eq, t_list.tischnr)]})
        tisch = db_session.query(Tisch).filter(
                 (Tisch.departement == t_list.departement) &
                 (Tisch.tischnr == t_list.tischnr)).with_for_update().first()

        if tisch:
            pass
            tisch.bezeich = t_list.bezeich
            tisch.normalbeleg = t_list.normalbeleg
            tisch.roomcharge = t_list.roomcharge

            if t_list.roomcharge:
                tisch.normalbeleg = 1
            pass
            pass

    return generate_output()