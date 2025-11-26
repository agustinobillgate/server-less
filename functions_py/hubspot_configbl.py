#using conversion tools version: 1.0.0.117
#--------------------------------------------
# Rd, 26/11/2025, with_for_update
#--------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

hubspot_param_data, Hubspot_param = create_model("Hubspot_param", {"nr":int, "param_name":string, "param_value":string})

def hubspot_configbl(case_type:int, hubspot_param_data:[Hubspot_param]):

    prepare_cache ([Queasy])

    queasy = None

    hubspot_param = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal case_type


        nonlocal hubspot_param

        return {"hubspot-param": hubspot_param_data}

    def create_queasy():

        nonlocal queasy
        nonlocal case_type


        nonlocal hubspot_param

        paramnr:int = 0
        paramnr = 1

        queasy = get_cache (Queasy, {"key": [(eq, 319)],"number1": [(eq, paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = paramnr
            queasy.char1 = "Hubspot URL"
            queasy.char2 = ""


        paramnr = 2

        queasy = get_cache (Queasy, {"key": [(eq, 319)],"number1": [(eq, paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = paramnr
            queasy.char1 = "Hubspot Secret Key"
            queasy.char2 = ""

    create_queasy()

    if case_type == 1:

        for hubspot_param in query(hubspot_param_data):

            # queasy = get_cache (Queasy, {"key": [(eq, 319)],"number1": [(eq, hubspot_param.nr)]})
            queasy = db_session.query(Queasy).with_for_update().filter(
                (Queasy.key == 319) & (Queasy.number1 == hubspot_param.nr)).first()

            if queasy:
                pass
                queasy.char2 = hubspot_param.param_value

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 319)).order_by(Queasy._recid).all():
        hubspot_param = Hubspot_param()
        hubspot_param_data.append(hubspot_param)

        hubspot_param.nr = queasy.number1
        hubspot_param.param_name = queasy.char1
        hubspot_param.param_value = queasy.char2

    return generate_output()