#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

kds_param_data, Kds_param = create_model("Kds_param", {"nr":int, "param_name":string, "param_value":string})

def kitchen_display_configbl(case_type:int, kds_param_data:[Kds_param]):

    prepare_cache ([Queasy])

    queasy = None

    kds_param = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal case_type


        nonlocal kds_param

        return {"kds-param": kds_param_data}

    def create_queasy():

        nonlocal queasy
        nonlocal case_type


        nonlocal kds_param

        t_paramnr:int = 0
        t_paramnr = 1

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, t_paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = t_paramnr
            queasy.char1 = "KDS Refresh Interval (In Second)"
            queasy.char2 = ""


        t_paramnr = 2

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, t_paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = t_paramnr
            queasy.char1 = "KDS Timeout Refresh Interval (In Second)"
            queasy.char2 = ""


        t_paramnr = 3

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, t_paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = t_paramnr
            queasy.char1 = "Interval Cooking Time 1 [Green](In Minute)"
            queasy.char2 = ""


        t_paramnr = 4

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, t_paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = t_paramnr
            queasy.char1 = "Interval Cooking Time 2 [Yellow](In Minute)"
            queasy.char2 = ""


        t_paramnr = 5

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, t_paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = t_paramnr
            queasy.char1 = "Interval Cooking Time 3 [Red](In Minute)"
            queasy.char2 = ""


        t_paramnr = 6

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, t_paramnr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 320
            queasy.number1 = t_paramnr
            queasy.char1 = "Sound Notification (Max 200kb)"
            queasy.char2 = ""

    create_queasy()

    if case_type == 1:

        for kds_param in query(kds_param_data):

            queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, kds_param.nr)]})

            if queasy:
                pass
                queasy.char2 = kds_param.param_value


                pass

    if case_type == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 320)],"number1": [(eq, 1)]})

        if queasy.char2 == "":
            kds_param = Kds_param()
            kds_param_data.append(kds_param)

            kds_param.nr = 0
            kds_param.param_name = "error"
            kds_param.param_value = "KDS not configured yet, please setting up first."

            return generate_output()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 320)).order_by(Queasy._recid).all():
        kds_param = Kds_param()
        kds_param_data.append(kds_param)

        kds_param.nr = queasy.number1
        kds_param.param_name = queasy.char1
        kds_param.param_value = queasy.char2

    return generate_output()