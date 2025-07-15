from functions.additional_functions import *
import decimal, traceback
from pprint import pprint
from models import Telephone

def display_content(variable):
    """
    Display the content of any type of variable.
    Uses pprint for better readability of complex structures.
    """
    if isinstance(variable, (dict, list, tuple, set)):
        pprint(variable)
    else:
        print(variable)

error_message = ""
t_telephone_list, T_telephone = create_model_like(Telephone)
print("T_Telephone:", T_telephone)
local_storage.debugging = "2506.Masuk writeTlp"
def write_telephonebl(case_type:int, int1:int, t_telephone_list:[T_telephone], **kwargs):
    """
    Handle arbitrary keyword arguments.
    """
    # Print all received parameters
    # print("Received parameters:")
    # for key, value in kwargs.items():
    #     print(f"{key}: {value}")

    global error_message
    print("11")
    try:
        print("12, Case:", case_type, t_telephone_list)
        # pprint(tTelephone)
        if t_telephone_list:
            for aa in t_telephone_list:
                print("->", aa['name'])

        success_flag = False
        telephone = None
        t_telephone = None

        db_session = local_storage.db_session

        def generate_output():
            nonlocal success_flag, telephone
            nonlocal t_telephone
            global t_telephone_list
            return {"success_flag": success_flag, "error_message": error_message, "ver": 7}

        if not t_telephone_list or not():
            t_telephone = query(t_telephone_list, first=True)
    
        if not t_telephone or not():
            print("29. No telephone")
            local_storage.debugging = local_storage.debugging + ", NoTelephone"
            return generate_output()

        if case_type == 1:
            local_storage.debugging = local_storage.debugging + ",1"
            telephone = db_session.query(Telephone).filter(
                    (Telephone._recid == int1)).first()
            if telephone:
                buffer_copy(t_telephone, telephone)
                telephone = db_session.query(Telephone).first()
                success_flag = True

        elif case_type == 2:
            print("Step 2")
            telephone = Telephone()
            print("Step2 telephone:", telephone)
            db_session.add(telephone)
            buffer_copy(t_telephone, telephone)
            success_flag = True

    except Exception as e:
        # Log the error to database
        error_message = traceback.format_exc()
        print("error:", error_message)
        local_storage.debugging = local_storage.debugging + ", " + error_message
        

    local_storage.debugging = local_storage.debugging + ", Lolos writeTlp"
    return generate_output()