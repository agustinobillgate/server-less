from functions.additional_functions import *
import decimal
from models import Nation

def gcf_nationbl(inp_natcode:int):
    nation_list_list = []
    nation = None

    nation_list = None

    nation_list_list, Nation_list = create_model("Nation_list", {"nationnr":int, "kurzbez":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal nation_list_list, nation
        nonlocal inp_natcode


        nonlocal nation_list
        nonlocal nation_list_list
        return {"nation-list": nation_list_list}

    if inp_natcode == 0:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation._recid).all():
            nation_list = Nation_list()
            nation_list_list.append(nation_list)

            buffer_copy(nation, nation_list)


    elif inp_natcode > 0:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == inp_natcode)).order_by(Nation._recid).all():
            nation_list = Nation_list()
            nation_list_list.append(nation_list)

            buffer_copy(nation, nation_list)


    elif inp_natcode < 0:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode > 0)).order_by(Nation._recid).all():
            nation_list = Nation_list()
            nation_list_list.append(nation_list)

            buffer_copy(nation, nation_list)


    return generate_output()