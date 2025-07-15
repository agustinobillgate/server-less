#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.check_htp_licensebl import check_htp_licensebl
from functions.read_bedienerlistbl import read_bedienerlistbl
from models import Bediener, Paramtext

def check_userkeybl(username:string, userkey:string):

    prepare_cache ([Paramtext])

    ok_flag = False
    licensenr:string = ""
    password:string = ""
    tmp_userkey:string = ""
    output_userkey:string = ""
    sha_userkey:string = ""
    stop_flag:bool = False
    has_license:bool = True
    nonce:string = ""
    timestamp:string = ""
    i:int = 0
    bediener = paramtext = None

    t_bediener = None

    t_bediener_data, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, nonce, timestamp, i, bediener, paramtext
        nonlocal username, userkey


        nonlocal t_bediener
        nonlocal t_bediener_data

        return {"ok_flag": ok_flag}

    def check_userkey(inp_username:string, inp_password:string, inp_license:string):

        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, nonce, timestamp, i, bediener, paramtext
        nonlocal username, userkey


        nonlocal t_bediener
        nonlocal t_bediener_data


        tmp_userkey = inp_license + inp_username + inp_password
        output_userkey = ""
        for i in range(1,length(tmp_userkey)  + 1) :
            output_userkey = output_userkey + "#" + substring(tmp_userkey, i - 1, 1)
        output_userkey = output_userkey + "#"
        sha_userkey = sha1(output_userkey).hexdigest()

        if sha_userkey.lower()  == (userkey).lower() :
            ok_flag = True
        else:
            pass


    def decode_string1(in_str:string):

        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, nonce, timestamp, i, bediener, paramtext
        nonlocal username, userkey


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


    def decode_string(in_str:string):

        nonlocal ok_flag, licensenr, password, tmp_userkey, output_userkey, sha_userkey, stop_flag, has_license, nonce, timestamp, i, bediener, paramtext
        nonlocal username, userkey


        nonlocal t_bediener
        nonlocal t_bediener_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    if num_entries(userkey, "|") > 1:
        nonce = entry(1, userkey, "|")
        timestamp = entry(2, userkey, "|")
        userkey = entry(0, userkey, "|")
    stop_flag = get_output(check_htp_licensebl())

    if stop_flag:

        if stop_flag:

            return generate_output()

    if has_license:
        t_bediener_data = get_output(read_bedienerlistbl(2, username))

        t_bediener = query(t_bediener_data, first=True)

        if not t_bediener:

            return generate_output()
        password = decode_string1(t_bediener.usercode)

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            licensenr = decode_string(paramtext.ptexte)
        else:

            return generate_output()
        username = username.upper()
        check_userkey(username, password.upper(), licensenr)

        if not ok_flag:
            check_userkey(username, password.lower(), licensenr)

    return generate_output()