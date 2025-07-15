from functions.additional_functions import *
import decimal
from functions.check_htp_licensebl import check_htp_licensebl
from functions.read_bedienerlistbl import read_bedienerlistbl
from models import Bediener, Paramtext

def check_userkeybl(username:str, userkey:str):
    ok_flag = False
    licensenr:str = ""
    password:str = ""
    tmp_userkey:str = ""
    output_userkey:str = ""
    sha_userkey:str = ""
    stop_flag:bool = False
    has_license:bool = True
    i:int = 0
    bediener = paramtext = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, i, bediener, paramtext


        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"ok_flag": ok_flag}

    def check_userkey(inp_username:str, inp_password:str, inp_license:str):
        # print("User/Pass/License:", inp_username, inp_password, inp_license)
        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, i, bediener, paramtext

        nonlocal t_bediener
        nonlocal t_bediener_list

        tmp_userkey = inp_license + inp_username + inp_password
        output_userkey = ""
        for i in range(1,len(tmp_userkey)  + 1) :
            output_userkey = output_userkey + "#" + substring(tmp_userkey, i - 1, 1)
        output_userkey = output_userkey + "#"
        sha_userkey = sha1(output_userkey).hexdigest()
        # print("Sha Userkey <=> userkey:", sha_userkey.lower(), (userkey).lower())
        if sha_userkey.lower()  == (userkey).lower() :
            ok_flag = True

    def decode_string1(in_str:str):

        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, i, bediener, paramtext


        nonlocal t_bediener
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

    def decode_string(in_str:str):

        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, i, bediener, paramtext

        nonlocal t_bediener
        nonlocal t_bediener_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()

    stop_flag = get_output(check_htp_licensebl())

    if stop_flag:

        if stop_flag:

            return generate_output()
    if has_license:
        t_bediener_list = get_output(read_bedienerlistbl(2, username))
        t_bediener = query(t_bediener_list, first=True)

        if not t_bediener:

            return generate_output()
        password = decode_string1(t_bediener.usercode)
        # print("Bediener Password:", password)
        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            licensenr = decode_string(paramtext.ptexte)
        else:

            return generate_output()
        username = username.upper()
        check_userkey(username, password.upper(), licensenr)
        print("SHA Userkey1:", sha_userkey)
        if not ok_flag:
            check_userkey(username, password.lower(), licensenr)
            print("SHA Userkey2:", sha_userkey)

    return generate_output()