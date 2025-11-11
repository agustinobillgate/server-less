#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 11/11/2025
# 
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def read_nationbl(natno:int, natbez:string, natname:string):
    t_nation_data = []
    nation = None

    t_nation = None

    t_nation_data, T_nation = create_model_like(Nation)

    db_session = local_storage.db_session

    natbez = natbez.strip()
    natname = natname.strip()

    def generate_output():
        nonlocal t_nation_data, nation
        nonlocal natno, natbez, natname


        nonlocal t_nation
        nonlocal t_nation_data

        return {"t-nation": t_nation_data}

    if natno > 0:

        # nation = get_cache (Nation, {"nationnr": [(eq, natno)]})
        nation = db_session.query(Nation).filter(
                 (Nation.nationnr == natno)).first()

    elif natbez != "":

        # nation = get_cache (Nation, {"kurzbez": [(eq, natbez)]})
        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == natbez)).first()

    elif natbez != "" and natname  == ("1") :

        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == natbez) & (Nation.natcode > 0)).first()

    elif natbez == "" and natname != "":

        # nation = get_cache (Nation, {"bezeich": [(eq, natname)]})
        nation = db_session.query(Nation).filter(
                 (Nation.bezeich == natname)).first()   

    if nation:
        t_nation = T_nation()
        t_nation_data.append(t_nation)

        buffer_copy(nation, t_nation)

    return generate_output()