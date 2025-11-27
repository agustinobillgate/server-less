#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix python indentation
            - add type ignore to avoid warning
            - deleted ' pass '
""" 
#-------------------------------------------
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

sgroup_list_data, Sgroup_list = create_model(
    "Sgroup_list", {
        "vhp_deptnr":int, 
        "vhp_dept":string, 
        "vhp_nr":int, 
        "vhp_bezeich":string, 
        "tbase_nr":int, 
        "tbase_bezeich":string, 
        "queasy_recid":int
        }
    )

def tbase_mapping_subgroup_fbarticlebl(sgroup_list_data:Sgroup_list):
    prepare_cache ([Queasy])

    queasy = None

    sgroup_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal sgroup_list

        return {}

    for sgroup_list in query(sgroup_list_data):  # type: ignore sgroup_list_data
        # queasy = get_cache (Queasy, {
        #     "key": [(eq, 369)],
        #     "char1": [(eq, "subgroup-fb")],
        #     "number2": [(eq, sgroup_list.vhp_nr)]})
        queasy = db_session.query(Queasy).filter(
            Queasy.key == 369,
            Queasy.char1 == "subgroup-fb",
            Queasy.number2 == sgroup_list.vhp_nr
        ).with_for_update().first()
        
        if not queasy:
            queasy = Queasy()

            queasy.key = 369
            queasy.char1 = "subgroup-fb"
            queasy.number2 = sgroup_list.vhp_nr
            queasy.char2 = sgroup_list.vhp_bezeich
            queasy.number3 = sgroup_list.tbase_nr
            queasy.char3 = sgroup_list.tbase_bezeich
            queasy.number1 = sgroup_list.vhp_deptnr

            db_session.add(queasy)

        else:
            queasy.char2 = sgroup_list.vhp_bezeich
            queasy.number3 = sgroup_list.tbase_nr
            queasy.char3 = sgroup_list.tbase_bezeich

    return generate_output()