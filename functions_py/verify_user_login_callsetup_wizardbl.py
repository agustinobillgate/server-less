#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 10-10-2025
# Tiket ID : 8CF423 | Recompile Program
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_main01bl import prepare_main01bl
from models import Bediener, Res_history, Paramtext

def verify_user_login_callsetup_wizardbl(user_name:string, user_pswd:string, headers:string):

    prepare_cache ([Bediener, Res_history, Paramtext])

    user_found = False
    user_token = ""
    user_key = ""
    userinit = ""
    usercode = ""
    permissions = ""
    error_code = 0
    lic_nr = ""
    htl_name = ""
    htl_city = ""
    tmp_userkey:string = ""
    output_userkey:string = ""
    licensenr:string = ""
    i:int = 0
    htl_adr:string = ""
    htl_tel:string = ""
    price_decimal:int = 0
    coa_format:string = ""
    vhp_licensedate:date = None
    vhp_newdb:bool = False
    bediener_pass:string = ""
    bediener_sha1:string = ""
    dd:string = ""
    mm:string = ""
    passwd:string = ""
    ip_address:string = ""
    bediener = res_history = paramtext = None

    shabediener = None

    Shabediener = create_buffer("Shabediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, tmp_userkey, output_userkey, licensenr, i, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, bediener_pass, bediener_sha1, dd, mm, passwd, ip_address, bediener, res_history, paramtext
        nonlocal user_name, user_pswd, headers
        nonlocal shabediener


        nonlocal shabediener

        return {"user_found": user_found, "user_token": user_token, "user_key": user_key, "userinit": userinit, "usercode": usercode, "permissions": permissions, "error_code": error_code, "lic_nr": lic_nr, "htl_name": htl_name, "htl_city": htl_city}

    def decode_string1(in_str:string):

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, tmp_userkey, output_userkey, licensenr, i, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, bediener_pass, bediener_sha1, dd, mm, passwd, ip_address, bediener, res_history, paramtext
        nonlocal user_name, user_pswd, headers
        nonlocal shabediener


        nonlocal shabediener

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

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, tmp_userkey, output_userkey, licensenr, i, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, bediener_pass, bediener_sha1, dd, mm, passwd, ip_address, bediener, res_history, paramtext
        nonlocal user_name, user_pswd, headers
        nonlocal shabediener


        nonlocal shabediener

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


    def get_header_value(input_key:string):

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, tmp_userkey, output_userkey, licensenr, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, bediener_pass, bediener_sha1, dd, mm, passwd, ip_address, bediener, res_history, paramtext
        nonlocal user_name, user_pswd, headers
        nonlocal shabediener


        nonlocal shabediener

        output_value = ""
        vkey:string = ""
        i:int = 0
        key_value:string = ""

        def generate_inner_output():
            return (output_value)

        for i in range(1,num_entries(headers, ",")  + 1) :
            key_value = entry(i - 1, headers, ",")
            vkey = trim(entry(0, key_value, "="))

            if input_key == vkey:
                output_value = trim(entry(1, key_value, "="))

        return generate_inner_output()

    bediener = get_cache (Bediener, {"username": [(eq, user_name)],"flag": [(eq, 1)]})

    if bediener:
        user_found = False
        error_code = 101

        return generate_output()

    if length(user_pswd) >= 40:

        shabediener = get_cache (Bediener, {"username": [(eq, user_name)]})

        if shabediener:
            bediener_pass = decode_string1(shabediener.usercode)
            bediener_sha1 = sha1(bediener_pass).hexdigest()

            if bediener_sha1.lower()  != (user_pswd).lower() :
                user_found = False
                error_code = 99

                return generate_output()
            else:
                user_pswd = bediener_pass

    bediener = get_cache (Bediener, {"username": [(eq, user_name)],"flag": [(eq, 0)]})

    if not bediener and user_name.lower()  == ("sindata").lower() :

        bediener = get_cache (Bediener, {"username": [(eq, user_name)],"betriebsnr": [(eq, 1)]})

        if not bediener:
            user_found = False

            return generate_output()

    if user_name.lower()  == ("sindata").lower()  and bediener.flag == 1:
        dd = to_string(get_day(get_current_date() + 1) , "99")
        dd = substring(dd, 1, 1) + substring(dd, 0, 1)
        mm = to_string(get_month(get_current_date() + 1) , "99")
        mm = substring(mm, 1, 1) + substring(mm, 0, 1)
        user_found = (user_pswd == ("SystemAdmin@" + dd + mm) and asc(substring(user_pswd, 0, 1)) == 83 and asc(substring(user_pswd, 6, 1)) == 65)


    else:
        passwd = decode_string1(bediener.usercode)
        user_found = (passwd == user_pswd)

    if user_found:
        userinit = bediener.userinit
        usercode = bediener.usercode
        permissions = bediener.permissions

        if headers != "":
            headers = replace_str(replace_str(headers, "{", "") , "}", "")
            headers = replace_str(replace_str(headers, "[", "") , "]", "")
            ip_address = get_header_value("x-forwarded-for")

            if ip_address == "":
                ip_address = get_header_value("host")
            ip_address = entry(0, ip_address, ":")
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Login Setup Wizard"


        res_history.aenderung = "User Login with Username: " + bediener.username + " IP: " + ip_address
    else:

        return generate_output()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)
    tmp_userkey = licensenr + user_name.upper() + user_pswd.upper()
    output_userkey = ""
    for i in range(1,length(tmp_userkey)  + 1) :
        output_userkey = output_userkey + "#" + substring(tmp_userkey, i - 1, 1)
    output_userkey = output_userkey + "#"
    user_key = sha1(output_userkey).hexdigest()
    user_key = user_key.upper()
    error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb = get_output(prepare_main01bl())

    return generate_output()