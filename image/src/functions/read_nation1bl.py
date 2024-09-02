from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation

def read_nation1bl(case_type:int, int1:int, int2:int, int3:int, char1:str, char2:str, logic1:bool):
    t_nation_list = []
    nation = None

    t_nation = None

    t_nation_list, T_nation = create_model_like(Nation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nation_list, nation


        nonlocal t_nation
        nonlocal t_nation_list
        return {"t-nation": t_nation_list}

    if case_type == 1:

        nation = db_session.query(Nation).filter(
                (Nation.untergruppe == int1) &  (Nation.natcode == int2)).first()

        if nation:
            t_nation = T_nation()
            t_nation_list.append(t_nation)

            buffer_copy(nation, t_nation)
    elif case_type == 2:

        for nation in db_session.query(Nation).filter(
                (Nation.natcode == int1)).all():
            t_nation = T_nation()
            t_nation_list.append(t_nation)

            buffer_copy(nation, t_nation)
    elif case_type == 3:

        nation = db_session.query(Nation).filter(
                (func.lower(Nation.kurzbez) == (char1).lower()) &  (Nation.natcode == int1)).first()

        if nation:
            t_nation = T_nation()
            t_nation_list.append(t_nation)

            buffer_copy(nation, t_nation)

    return generate_output()