from functions.additional_functions import *
import decimal
from models import Telephone

t_telephone_list, T_telephone = create_model_like(Telephone)

def write_telephonebl(case_type:int, int1:int, t_telephone_list:[T_telephone]):
    success_flag = False
    telephone = None

    t_telephone = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, telephone
        nonlocal case_type, int1


        nonlocal t_telephone
        nonlocal t_telephone_list
        return {"success_flag": success_flag, "ver":8}

    if not t_telephone or not():
        t_telephone = query(t_telephone_list, first=True)

    if not t_telephone:

        return generate_output()

    if case_type == 1:
        if not telephone or not(telephone._recid == int1):
            telephone = db_session.query(Telephone).filter(
                (Telephone._recid == int1)).first()

        if telephone:
            print("Telephone:", telephone)
            buffer_copy(t_telephone, telephone)
            db_session.commit()
            success_flag = True
    elif case_type == 2:
        telephone = Telephone()
        db_session.add(telephone)

        buffer_copy(t_telephone, telephone)
        success_flag = True

    return generate_output()