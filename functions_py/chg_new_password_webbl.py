#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
import random
from models import Bediener, Res_history

def chg_new_password_webbl(uname:string, new_pwd:string):

    prepare_cache ([Bediener, Res_history])

    pswd:string = ""
    bediener = res_history = None

    db_session = local_storage.db_session
    uname = uname.strip()
    new_pwd = new_pwd.strip()

    def generate_output():
        nonlocal pswd, bediener, res_history
        nonlocal uname, new_pwd

        return {}

    def encode_string(in_str:string):

        nonlocal pswd, bediener, res_history
        nonlocal uname, new_pwd

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0
        ch:string = ""

        def generate_inner_output():
            return (out_str)

        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        ch = chr_unicode(asc(to_string(j)) + 23)
        out_str = ch
        j = asc(ch) - 71
        for len_ in range(1,length(in_str)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(in_str, len_ - 1, 1)) + j)

        return generate_inner_output()


    pswd = encode_string(new_pwd)

    # bediener = get_cache (Bediener, {"username": [(eq, uname)]})
    bediener = db_session.query(Bediener).filter(
             (Bediener.username == uname)).with_for_update().first()

    if bediener:
        pass
        bediener.usercode = pswd
        bediener.kassenbest =  to_decimal("0")


        pass
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Change Password"
        res_history.action = "User"


        pass
        pass

    return generate_output()