#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

akt_code_list_data, Akt_code_list = create_model_like(Akt_code)

def aktcode_admin_btn_exitbl(akt_code_list_data:[Akt_code_list], case_type:int, recid_akt_code:int):

    prepare_cache ([Akt_code])

    akt_code = None

    akt_code_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal akt_code
        nonlocal case_type, recid_akt_code


        nonlocal akt_code_list

        return {}

    def fill_akt_code():

        nonlocal akt_code
        nonlocal case_type, recid_akt_code


        nonlocal akt_code_list


        akt_code.aktiongrup = 1
        akt_code.aktionscode = akt_code_list.aktionscode
        akt_code.bezeich = akt_code_list.bezeich
        akt_code.bemerkung = akt_code_list.bemerkung


    akt_code_list = query(akt_code_list_data, first=True)

    if case_type == 1:
        akt_code = Akt_code()
        db_session.add(akt_code)

        akt_code.aktiongrup = 1
        akt_code.aktionscode = akt_code_list.aktionscode
        akt_code.bezeich = akt_code_list.bezeich
        akt_code.bemerkung = akt_code_list.bemerkung
    else:

        # akt_code = get_cache (Akt_code, {"_recid": [(eq, recid_akt_code)]})
        akt_code = db_session.query(Akt_code).filter(
                 (Akt_code._recid == recid_akt_code)).with_for_update().first()

        if not akt_code:

            return generate_output()
        else:
            pass
            akt_code.aktiongrup = 1
            akt_code.aktionscode = akt_code_list.aktionscode
            akt_code.bezeich = akt_code_list.bezeich
            akt_code.bemerkung = akt_code_list.bemerkung
            pass
            pass

    return generate_output()