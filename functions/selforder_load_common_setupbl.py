#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def selforder_load_common_setupbl(outlet_number:int):

    prepare_cache ([Queasy])

    setup_list_data = []
    queasy = None

    setup_list = None

    setup_list_data, Setup_list = create_model("Setup_list", {"setup_number":int, "setup_param":string, "setup_value":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal setup_list_data, queasy
        nonlocal outlet_number


        nonlocal setup_list
        nonlocal setup_list_data

        return {"setup-list": setup_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 222) & (Queasy.number1 == 1) & (Queasy.betriebsnr == outlet_number)).order_by(Queasy.number2).all():

        if (queasy.number2 == 1 or queasy.number2 == 2 or queasy.number2 == 3 or queasy.number2 == 4 or queasy.number2 == 18 or queasy.number2 == 19):
            setup_list = Setup_list()
            setup_list_data.append(setup_list)

            setup_list.setup_number = queasy.number2
            setup_list.setup_param = queasy.char1
            setup_list.setup_value = queasy.char2

    return generate_output()