#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Telephone

t_telephone_data, T_telephone = create_model_like(Telephone)

def write_telephonebl(case_type:int, int1:int, t_telephone_data:[T_telephone]):
    success_flag = False
    telephone = None

    t_telephone = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, telephone
        nonlocal case_type, int1


        nonlocal t_telephone

        return {"success_flag": success_flag}

    t_telephone = query(t_telephone_data, first=True)

    if not t_telephone:

        return generate_output()

    if case_type == 1:

        # telephone = get_cache (Telephone, {"_recid": [(eq, int1)]})
        telephone = db_session.query(Telephone).filter(
                 (Telephone._recid == int1)).with_for_update().first()

        if telephone:
            buffer_copy(t_telephone, telephone)
            pass
            success_flag = True
    elif case_type == 2:
        telephone = Telephone()
        db_session.add(telephone)

        buffer_copy(t_telephone, telephone)
        success_flag = True

    return generate_output()