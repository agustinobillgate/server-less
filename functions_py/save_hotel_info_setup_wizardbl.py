#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# Rd, 28/11/2025, with_for_update added
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Queasy

t_hotel_data_data, T_hotel_data = create_model("T_hotel_data", {"hotel_name":string, "hotel_city":string, "hotel_phone":string, "hotel_email":string})

def save_hotel_info_setup_wizardbl(t_hotel_data_data:[T_hotel_data]):

    prepare_cache ([Paramtext, Queasy])

    error_message = ""
    paramtext = queasy = None

    t_hotel_data = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_message, paramtext, queasy


        nonlocal t_hotel_data

        return {"error_message": error_message}

    def create_section():

        nonlocal error_message, paramtext, queasy


        nonlocal t_hotel_data

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 357) & (Queasy.number1 == 1) & (Queasy.char1 == ("HOTEL INFROMATION").lower()) & (Queasy.logi1)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 357
            queasy.number1 = 1
            queasy.char1 = "HOTEL INFROMATION"
            queasy.logi1 = True


    t_hotel_data = query(t_hotel_data_data, first=True)

    if not t_hotel_data:
        error_message = "No Data Available"

    # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 200).with_for_update().first()

    if paramtext:
        pass
        paramtext.ptexte = t_hotel_data.hotel_name
        pass

    # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
    paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 203).with_for_update().first()

    if paramtext:
        pass
        paramtext.ptexte = t_hotel_data.hotel_city
        pass

    # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 204).with_for_update().first()

    if paramtext:
        pass
        paramtext.ptexte = t_hotel_data.hotel_phone
        pass

    # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 206)]})
    paramtext = db_session.query(Paramtext).filter(Paramtext.txtnr == 206).with_for_update().first()

    if paramtext:
        pass
        paramtext.ptexte = t_hotel_data.hotel_email
        pass
    pass
    create_section()

    return generate_output()