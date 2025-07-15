#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def select_rcode_elementbl():

    prepare_cache ([Queasy])

    rcode_list_data = []
    queasy = None

    rcode_list = None

    rcode_list_data, Rcode_list = create_model("Rcode_list", {"code":int, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rcode_list_data, queasy


        nonlocal rcode_list
        nonlocal rcode_list_data

        return {"rcode-list": rcode_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 287)).order_by(Queasy.number1).all():
        rcode_list = Rcode_list()
        rcode_list_data.append(rcode_list)

        rcode_list.code = queasy.number1
        rcode_list.name = queasy.char1

    return generate_output()