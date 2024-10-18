from functions.additional_functions import *
import decimal
from models import Telephone

def read_telephonebl(case_type:int, int1:int, int2:int, char1:str, char2:str, char3:str, char4:str):
    t_telephone_list = []
    telephone = None

    t_telephone = None

    t_telephone_list, T_telephone = create_model_like(Telephone)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_telephone_list, telephone
        nonlocal case_type, int1, int2, char1, char2, char3, char4


        nonlocal t_telephone
        nonlocal t_telephone_list
        return {"t-telephone": t_telephone_list}

    if case_type == 1:

        telephone = db_session.query(Telephone).filter(
                 (Telephone._recid == int1)).first()

        if telephone:
            t_telephone = T_telephone()
            t_telephone_list.append(t_telephone)

            buffer_copy(telephone, t_telephone)
    elif case_type == 99:

        telephone = db_session.query(Telephone).filter(
                 (Telephone._recid == int1)).first()

        if telephone:
            t_telephone = T_telephone()
            t_telephone_list.append(t_telephone)

            buffer_copy(telephone, t_telephone)

    return generate_output()