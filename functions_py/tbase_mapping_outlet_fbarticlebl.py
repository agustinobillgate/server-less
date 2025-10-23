#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix python indentation
            - add type ignore to avoid warning
            - deleted ' pass '
""" 

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

outlet_list_data, Outlet_list = create_model(
    "Outlet_list", {
        "vhp_nr":int, 
        "vhp_bezeich":string, 
        "tbase_nr":int, 
        "tbase_bezeich":string, 
        "queasy_recid":int
        }
    )

def tbase_mapping_outlet_fbarticlebl(outlet_list_data:Outlet_list):
    prepare_cache ([Queasy])

    queasy = None

    outlet_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal outlet_list

        return {}

    for outlet_list in query(outlet_list_data):  # type: ignore outlet_list_data
        queasy = get_cache (Queasy, {
            "key": [(eq, 369)],
            "char1": [(eq, "outlet-fb")],
            "number2": [(eq, outlet_list.vhp_nr)]})

        if not queasy:
            queasy = Queasy()

            queasy.key = 369
            queasy.char1 = "outlet-fb"
            queasy.number2 = outlet_list.vhp_nr
            queasy.char2 = outlet_list.vhp_bezeich
            queasy.number3 = outlet_list.tbase_nr
            queasy.char3 = outlet_list.tbase_bezeich

            db_session.add(queasy)

        else:
            queasy.char2 = outlet_list.vhp_bezeich
            queasy.number3 = outlet_list.tbase_nr
            queasy.char3 = outlet_list.tbase_bezeich

    return generate_output()