#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nation

def stock_originbl():
    origin_list_list = []
    nation = None

    origin_list = None

    origin_list_list, Origin_list = create_model("Origin_list", {"kurzbez":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal origin_list_list, nation


        nonlocal origin_list
        nonlocal origin_list_list

        return {"origin-list": origin_list_list}

    for nation in db_session.query(Nation).filter(
             (Nation.natcode == 0)).order_by(Nation._recid).all():
        origin_list = Origin_list()
        origin_list_list.append(origin_list)

        buffer_copy(nation, origin_list)

    return generate_output()