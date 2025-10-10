#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

t_payload_list_data, T_payload_list = create_model("T_payload_list", {"user_init":string})

def prepare_hotel_info_setup_wizardbl(t_payload_list_data:[T_payload_list]):

    prepare_cache ([Paramtext])

    t_hotel_list_data = []
    paramtext = None

    t_payload_list = t_hotel_list = None

    t_hotel_list_data, T_hotel_list = create_model("T_hotel_list", {"hotel_name":string, "hotel_city":string, "hotel_phone":string, "hotel_email":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_hotel_list_data, paramtext


        nonlocal t_payload_list, t_hotel_list
        nonlocal t_hotel_list_data

        return {"t-hotel-list": t_hotel_list_data}


    t_payload_list = query(t_payload_list_data, first=True)

    if not t_payload_list:

        return generate_output()
    t_hotel_list = T_hotel_list()
    t_hotel_list_data.append(t_hotel_list)


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        t_hotel_list.hotel_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})

    if paramtext:
        t_hotel_list.hotel_city = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})

    if paramtext:
        t_hotel_list.hotel_phone = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 206)]})

    if paramtext:
        t_hotel_list.hotel_email = paramtext.ptexte

    return generate_output()