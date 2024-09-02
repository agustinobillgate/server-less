from functions.additional_functions import *
import decimal
from sqlalchemy import func
import random
from models import Bediener

def neubenutzer_exitbl(pvilanguage:int, name_str:str, id_str:str, new_id:str, new_id1:str):
    user_init = ""
    user_name = ""
    msg_str = ""
    error_flag = False
    t_bediener_list = []
    nr:int = 0
    lvcarea:str = "neubenutzer"
    bediener = None

    t_bediener = usr = None

    t_bediener_list, T_bediener = create_model_like(Bediener)

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_list, nr, lvcarea, bediener
        nonlocal usr


        nonlocal t_bediener, usr
        nonlocal t_bediener_list
        return {"user_init": user_init, "user_name": user_name, "msg_str": msg_str, "error_flag": error_flag, "t-bediener": t_bediener_list}

    def decode_usercode():

        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_list, nr, lvcarea, bediener
        nonlocal usr


        nonlocal t_bediener, usr
        nonlocal t_bediener_list

        nr = 0
        found:bool = False
        passwd:str = ""

        def generate_inner_output():
            return nr
        Usr = Bediener

        usr = db_session.query(Usr).filter(
                (func.lower(Usr.username) == (name_str).lower()) &  (Usr.betriebsnr == 1) &  (Usr.flag == 0)).first()
        while None != usr and not found:
            passwd = decode_string(usr.usercode)

            if passwd.lower()  == (id_str).lower() :
                nr = usr.nr
                found = True
            else:

                usr = db_session.query(Usr).filter(
                        (func.lower(Usr.username) == (name_str).lower()) &  (Usr.betriebsnr == 1) &  (Usr.flag == 0)).first()


        return generate_inner_output()

    def encode_string(in_str:str):

        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_list, nr, lvcarea, bediener
        nonlocal usr


        nonlocal t_bediener, usr
        nonlocal t_bediener_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0
        ch:str = ""

        def generate_inner_output():
            return out_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        in_str = to_string(j) + in_str
        j = random.randint(1, 9)
        ch = chr(ord(to_string(j)) + 23)
        out_str = ch
        j = ord(ch) - 71
        for len_ in range(1,len(in_str)  + 1) :
            out_str = out_str + chr (ord(substring(in_str, len_ - 1, 1)) + j)


        return generate_inner_output()

    def decode_string(in_str:str):

        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_list, nr, lvcarea, bediener
        nonlocal usr


        nonlocal t_bediener, usr
        nonlocal t_bediener_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 71
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (len(out_str) - 4))


        return generate_inner_output()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.username) == (name_str).lower()) &  (Bediener.flag == 0)).first()

    if not bediener:
        msg_str = translateExtended ("Wrong User ID.", lvcarea, "")

        return generate_output()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.username) == (name_str).lower()) &  (func.lower(Bediener.usercode) == (id_str).lower()) &  (Bediener.betriebsnr == 0) &  (Bediener.flag == 0)).first()

    if not bediener:
        nr = decode_usercode()

        if nr > 0:

            bediener = db_session.query(Bediener).filter(
                    (Bediener.nr == nr)).first()

    if not bediener:
        msg_str = translateExtended ("Wrong User ID.", lvcarea, "")

        return generate_output()
    error_flag = False
    user_init = bediener.userinit
    user_name = bediener.username

    if new_id.lower()  != (new_id1).lower() :
        msg_str = translateExtended ("Passwords do not match and will be ignored.", lvcarea, "")

    elif new_id != "":

        bediener = db_session.query(Bediener).first()
        new_id1 = encode_string(new_id)
        bediener.usercode = new_id1
        bediener.betriebsnr = 1

        bediener = db_session.query(Bediener).first()
        msg_str = translateExtended ("New password accepted.", lvcarea, "")
    t_bediener = T_bediener()
    t_bediener_list.append(t_bediener)

    buffer_copy(bediener, t_bediener)

    return generate_output()