from functions.additional_functions import *
import decimal
from models import Nation

def stock_originbl():
    origin_list_list = []
    nation = None

    origin_list = None

    origin_list_list, Origin_list = create_model("Origin_list", {"kurzbez":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal origin_list_list, nation


        nonlocal origin_list
        nonlocal origin_list_list
        return {"origin-list": origin_list_list}

    for nation in db_session.query(Nation).filter(
            (Nation.natcode == 0)).all():
        origin_list = Origin_list()
        origin_list_list.append(origin_list)

        buffer_copy(nation, origin_list)

    return generate_output()