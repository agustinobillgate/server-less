#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def esign_select_usrbl():

    prepare_cache ([Bediener])

    user_list_data = []
    nr:int = 0
    bediener = None

    user_list = None

    user_list_data, User_list = create_model("User_list", {"usr_nr":int, "usr_name":string, "usr_init":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_list_data, nr, bediener


        nonlocal user_list
        nonlocal user_list_data

        return {"user-list": user_list_data}

    for bediener in db_session.query(Bediener).filter(
             (Bediener.flag == 0)).order_by(Bediener.username).all():
        nr = nr + 1
        user_list = User_list()
        user_list_data.append(user_list)

        user_list.usr_nr = nr
        user_list.usr_name = bediener.username
        user_list.usr_init = bediener.userinit

    return generate_output()