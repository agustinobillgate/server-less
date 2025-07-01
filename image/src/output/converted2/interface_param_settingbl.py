#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

hotel_config_list, Hotel_config = create_model("Hotel_config", {"keynr":int, "number1":int, "number2":int, "number3":int, "date1":date, "date2":date, "date3":date, "char1":string, "char2":string, "char3":string, "deci1":Decimal, "deci2":Decimal, "deci3":Decimal, "logi1":bool, "logi2":bool, "logi3":bool, "betriebsnr":int})

def interface_param_settingbl(case_type:int, hotel_config_list:[Hotel_config]):
    mess_result = ""
    queasy = None

    hotel_config = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, queasy
        nonlocal case_type


        nonlocal hotel_config

        return {"hotel-config": hotel_config_list, "mess_result": mess_result}

    if case_type == 1:

        hotel_config = query(hotel_config_list, first=True)

        if hotel_config:

            if hotel_config.keynr != 306:
                mess_result = "Invalid key, should be 306, key param is: " + to_string(hotel_config.keynr)

                return generate_output()
            else:
                queasy = Queasy()
                db_session.add(queasy)

                buffer_copy(hotel_config, queasy)
                queasy.key = hotel_config.keynr
                mess_result = "add success"
        else:
            mess_result = "hotel-config is empty!"

            return generate_output()

    elif case_type == 2:

        hotel_config = query(hotel_config_list, first=True)

        if hotel_config:

            if hotel_config.keynr != 306:
                mess_result = "Invalid key, should be 306, key param is: " + to_string(hotel_config.keynr)

                return generate_output()
            else:

                queasy = get_cache (Queasy, {"key": [(eq, hotel_config.keynr)]})

                if queasy:
                    buffer_copy(hotel_config, queasy)
                    mess_result = "modify success"
                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    buffer_copy(hotel_config, queasy)
                    queasy.key = hotel_config.keynr
                    mess_result = "add success"
        else:
            mess_result = "hotel-config is empty!"

            return generate_output()

    elif case_type == 3:

        hotel_config = query(hotel_config_list, first=True)

        if hotel_config:

            if hotel_config.keynr != 306:
                mess_result = "Invalid key, should be 306, key param is: " + to_string(hotel_config.keynr)

                return generate_output()
            else:

                queasy = get_cache (Queasy, {"key": [(eq, hotel_config.keynr)]})

                if queasy:
                    db_session.delete(queasy)
                    mess_result = "delete success"
        else:
            mess_result = "hotel-config is empty!"

            return generate_output()
    hotel_config_list.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 306)]})

    if queasy:
        hotel_config = Hotel_config()
        hotel_config_list.append(hotel_config)

        buffer_copy(queasy, hotel_config)
        hotel_config.keynr = queasy.key

    if case_type == 0:
        mess_result = "load data success"

    return generate_output()