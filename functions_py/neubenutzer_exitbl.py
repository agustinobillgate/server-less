#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
import random
from models import Bediener

def neubenutzer_exitbl(pvilanguage:int, name_str:string, id_str:string, new_id:string, new_id1:string):
    user_init = ""
    user_name = ""
    msg_str = ""
    error_flag = True
    t_bediener_data = []
    nr:int = 0
    lvcarea:string = "neubenutzer"
    bediener = None

    t_bediener = None

    t_bediener_data, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session
    name_str = name_str.strip()
    id_str = id_str.strip()
    new_id = new_id.strip()
    new_id1 = new_id1.strip()

    def generate_output():
        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_data, nr, lvcarea, bediener
        nonlocal pvilanguage, name_str, id_str, new_id, new_id1


        nonlocal t_bediener
        nonlocal t_bediener_data

        return {"user_init": user_init, "user_name": user_name, "msg_str": msg_str, "error_flag": error_flag, "t-bediener": t_bediener_data}

    def decode_usercode():

        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_data, nr, lvcarea, bediener
        nonlocal pvilanguage, name_str, id_str, new_id, new_id1


        nonlocal t_bediener
        nonlocal t_bediener_data

        nr = -1
        found:bool = False
        passwd:string = ""
        usr = None

        def generate_inner_output():
            return (nr)

        Usr =  create_buffer("Usr",Bediener)

        usr = db_session.query(Usr).filter(
                 (Usr.username == (name_str).lower()) & (Usr.betriebsnr == 1) & (Usr.flag == 0)).first()
        while None != usr and not found:
            passwd = decode_string(usr.usercode)

            if passwd.lower()  == (id_str).lower() :
                nr = usr.nr
                found = True
            else:

                curr_recid = usr._recid
                usr = db_session.query(Usr).filter(
                         (Usr.username == (name_str).lower()) & (Usr.betriebsnr == 1) & (Usr.flag == 0) & (Usr._recid > curr_recid)).first()

        return generate_inner_output()


    def encode_string(in_str:string):

        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_data, nr, lvcarea, bediener
        nonlocal pvilanguage, name_str, id_str, new_id, new_id1


        nonlocal t_bediener
        nonlocal t_bediener_data

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


    def decode_string(in_str:string):

        nonlocal user_init, user_name, msg_str, error_flag, t_bediener_data, nr, lvcarea, bediener
        nonlocal pvilanguage, name_str, id_str, new_id, new_id1


        nonlocal t_bediener
        nonlocal t_bediener_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()


    bediener = get_cache (Bediener, {"username": [(eq, name_str)],"flag": [(eq, 0)]})

    if not bediener:
        msg_str = translateExtended ("Wrong User ID.", lvcarea, "")

        return generate_output()

    # bediener = get_cache (Bediener, {"username": [(eq, name_str)],"usercode": [(eq, id_str)],"betriebsnr": [(eq, 0)],"flag": [(eq, 0)]})
    bediener = db_session.query(Bediener).filter(Bediener.username == name_str, 
                                                 Bediener.usercode == encode_string(id_str),
                                                 Bediener.betriebsnr == 0,
                                                 Bediener.flag == 0).with_for_update().first()

    if not bediener:
        nr = decode_usercode()

        if nr > 0:

            bediener = get_cache (Bediener, {"nr": [(eq, nr)]})

    if not bediener:
        msg_str = translateExtended ("Wrong User ID.", lvcarea, "")

        return generate_output()
    error_flag = False
    user_init = bediener.userinit
    user_name = bediener.username

    if new_id.lower()  != (new_id1).lower() :
        msg_str = translateExtended ("Passwords do not match and will be ignored.", lvcarea, "")

    elif new_id != "":
        pass
        new_id1 = encode_string(new_id)
        bediener.usercode = new_id1
        bediener.betriebsnr = 1


        pass
        msg_str = translateExtended ("New password accepted.", lvcarea, "")
    t_bediener = T_bediener()
    t_bediener_data.append(t_bediener)

    buffer_copy(bediener, t_bediener)

    return generate_output()