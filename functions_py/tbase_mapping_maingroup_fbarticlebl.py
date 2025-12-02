#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix python indentation
            - add type ignore to avoid warning
            - deleted ' pass '
""" 
#-----------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

mgroup_list_data, Mgroup_list = create_model(
    "Mgroup_list", {
        "vhp_nr":int, 
        "vhp_bezeich":string, 
        "tbase_nr":int, 
        "tbase_bezeich":string, 
        "queasy_recid":int, 
        "resto_artikel":bool, 
        "bill_artikel":bool
        }
    )

def tbase_mapping_maingroup_fbarticlebl(mgroup_list_data:Mgroup_list):
    prepare_cache ([Queasy])

    queasy = None

    mgroup_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal mgroup_list

        return {}

    for mgroup_list in query(mgroup_list_data):  # type: ignore mgroup_list_data
        # queasy = get_cache (Queasy, {
        #     "key": [(eq, 369)],
        #     "char1": [(eq, "maingroup-fb")],
        #     "number2": [(eq, mgroup_list.vhp_nr)]})
        queasy = db_session.query(Queasy).filter(
            Queasy.key == 369,
            Queasy.char1 == "maingroup-fb",
            Queasy.number2 == mgroup_list.vhp_nr
        ).with_for_update().first()

        if not queasy:
            queasy = Queasy()

            queasy.key = 369
            queasy.char1 = "maingroup-fb"
            queasy.number2 = mgroup_list.vhp_nr
            queasy.char2 = mgroup_list.vhp_bezeich
            queasy.number3 = mgroup_list.tbase_nr
            queasy.char3 = mgroup_list.tbase_bezeich

            db_session.add(queasy)

            if mgroup_list.resto_artikel :
                queasy.logi1 = True

            elif mgroup_list.bill_artikel :
                queasy.logi2 = True

        else:
            queasy.char2 = mgroup_list.vhp_bezeich
            queasy.number3 = mgroup_list.tbase_nr
            queasy.char3 = mgroup_list.tbase_bezeich

    return generate_output()