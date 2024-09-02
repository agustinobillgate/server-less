from functions.additional_functions import *
import decimal
from models import Nation

def write_nationbl(case_type:int, t_nation:[T_nation]):
    success_flag = False
    nation = None

    t_nation = None

    t_nation_list, T_nation = create_model_like(Nation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nation


        nonlocal t_nation
        nonlocal t_nation_list
        return {"success_flag": success_flag}

    t_nation = query(t_nation_list, first=True)

    if not t_nation:

        return generate_output()

    if case_type == 1:
        nation = Nation()
        db_session.add(nation)

        buffer_copy(t_nation, nation)
        success_flag = True
    elif case_type == 2:

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == t_Nation.kurzbez) &  (Nation.untergruppe == t_Nation.untergruppe) &  (Nation.natcode == t_Nation.natcode)).first()

        if nation:
            buffer_copy(t_nation, nation)
            success_flag = True

    return generate_output()