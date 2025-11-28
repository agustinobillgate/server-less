#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Telephone

def delete_telephonebl(case_type:int, int1:int, char1:string, char2:string):
    success_flag = False
    telephone = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, telephone
        nonlocal case_type, int1, char1, char2

        return {"success_flag": success_flag}


    if case_type == 1:

        # telephone = get_cache (Telephone, {"telephone": [(eq, char1)],"name": [(eq, char2)]})
        telephone = db_session.query(Telephone).filter(
                 (Telephone.telephone == char1) & (Telephone.name == char2)).with_for_update().first()

        if telephone:
            db_session.delete(telephone)
            pass
            success_flag = True

    return generate_output()