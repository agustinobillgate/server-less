from functions.additional_functions import *
import decimal
from models import Nation

def read_nationbl(natno:int, natbez:str, natname:str):
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

    if natno > 0:

        nation = db_session.query(Nation).filter(
                (Nationnr == natno)).first()

    elif natbez != "":

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == natbez)).first()

    elif natbez != "" and natname.lower()  == "1":

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == natbez) &  (Nation.natcode > 0)).first()

    elif natbez == "" and natname != "":

        nation = db_session.query(Nation).filter(
                (Nation.bezeich == natname)).first()

    if nation:
        t_nation = T_nation()
        t_nation_list.append(t_nation)

        buffer_copy(nation, t_nation)

    return generate_output()