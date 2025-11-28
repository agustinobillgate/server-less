#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Telephone

def read_telephonebl(case_type:int, int1:int, int2:int, char1:string, char2:string, char3:string, char4:string):
    t_telephone_data = []
    telephone = None

    t_telephone = None

    t_telephone_data, T_telephone = create_model_like(Telephone)

    db_session = local_storage.db_session
    char1 = char1.strip()
    char2 = char2.strip()
    char3 = char3.strip()
    char4 = char4.strip()

    def generate_output():
        nonlocal t_telephone_data, telephone
        nonlocal case_type, int1, int2, char1, char2, char3, char4


        nonlocal t_telephone
        nonlocal t_telephone_data

        return {"t-telephone": t_telephone_data}

    if case_type == 1:

        telephone = get_cache (Telephone, {"_recid": [(eq, int1)]})

        if telephone:
            t_telephone = T_telephone()
            t_telephone_data.append(t_telephone)

            buffer_copy(telephone, t_telephone)
    elif case_type == 99:

        telephone = get_cache (Telephone, {"_recid": [(eq, int1)]})

        if telephone:
            t_telephone = T_telephone()
            t_telephone_data.append(t_telephone)

            buffer_copy(telephone, t_telephone)

    return generate_output()