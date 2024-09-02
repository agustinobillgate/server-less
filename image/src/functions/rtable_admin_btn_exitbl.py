from functions.additional_functions import *
import decimal
from models import Tisch

def rtable_admin_btn_exitbl(t_list:[T_list], case_type:int):
    tisch = None

    t_list = None

    t_list_list, T_list = create_model_like(Tisch)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tisch


        nonlocal t_list
        nonlocal t_list_list
        return {}

    def fill_new_tisch():

        nonlocal tisch


        nonlocal t_list
        nonlocal t_list_list


        buffer_copy(t_list, tisch)

        if tisch.roomcharge:
            tisch.normalbeleg = 1

    t_list = query(t_list_list, first=True)

    if case_type == 1:
        tisch = Tisch()
        db_session.add(tisch)

        fill_new_tisch()

    elif case_type == 2:

        tisch = db_session.query(Tisch).filter(
                (Tisch.departement == t_list.departement) &  (Tischnr == t_list.tischnr)).first()

        if tisch:

            tisch = db_session.query(Tisch).first()
            tisch.bezeich = t_list.bezeich
            tisch.normalbeleg = t_list.normalbeleg
            tisch.roomcharge = t_list.roomcharge

            if t_list.roomcharge:
                tisch.normalbeleg = 1

            tisch = db_session.query(Tisch).first()


    return generate_output()