#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def gcf_nationbl(inp_natcode:int):
    nation_list_data = []
    nation = None

    nation_list = None

    nation_list_data, Nation_list = create_model("Nation_list", {"nationnr":int, "kurzbez":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal nation_list_data, nation
        nonlocal inp_natcode


        nonlocal nation_list
        nonlocal nation_list_data

        return {"nation-list": nation_list_data}

    if inp_natcode == 0:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == 0)).order_by(Nation._recid).all():
            nation_list = Nation_list()
            nation_list_data.append(nation_list)

            buffer_copy(nation, nation_list)


    elif inp_natcode > 0:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode == inp_natcode)).order_by(Nation._recid).all():
            nation_list = Nation_list()
            nation_list_data.append(nation_list)

            buffer_copy(nation, nation_list)


    elif inp_natcode < 0:

        for nation in db_session.query(Nation).filter(
                 (Nation.natcode > 0)).order_by(Nation._recid).all():
            nation_list = Nation_list()
            nation_list_data.append(nation_list)

            buffer_copy(nation, nation_list)


    return generate_output()