from functions.additional_functions import *
import decimal
from models import Nation, Queasy

def prepare_bookengine_mapping_nationbl(bookengid:int):
    t_mapping_nation_list = []
    nation = queasy = None

    t_mapping_nation = None

    t_mapping_nation_list, T_mapping_nation = create_model("T_mapping_nation", {"nationvhp":str, "nationbe":str, "descr":str, "nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mapping_nation_list, nation, queasy


        nonlocal t_mapping_nation
        nonlocal t_mapping_nation_list
        return {"t-mapping-nation": t_mapping_nation_list}

    for nation in db_session.query(Nation).filter(
            (Nation.natcode == 0)).all():
        t_mapping_nation = T_mapping_nation()
        t_mapping_nation_list.append(t_mapping_nation)

        t_mapping_nationVHP = nation.kurzbez
        t_mapping_nation.descr = entry(0, nation.bezeich, ";")
        t_mapping_nation.nr = nationnr

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 165) &  (Queasy.number1 == bookengid) &  (Queasy.number2 == nationnr)).first()

        if queasy:
            t_mapping_nationBE = queasy.char2
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 165
            queasy.number1 = bookengid
            queasy.number2 = nationnr
            queasy.char1 = nation.kurzbez

    return generate_output()