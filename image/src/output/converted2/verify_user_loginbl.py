#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_main01bl import prepare_main01bl
from models import Bediener, Res_history, Paramtext, Guest_queasy

def verify_user_loginbl(user_name:string, user_pswd:string):

    prepare_cache ([Bediener, Res_history, Paramtext, Guest_queasy])

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
    htl_adr = ""
    htl_tel = ""
    price_decimal = 0
    coa_format = ""
    vhp_licensedate = None
    vhp_newdb = False
    tmp_userkey:string = ""
    output_userkey:string = ""
    licensenr:string = ""
    i:int = 0
    bediener_pass:string = ""
    bediener_sha1:string = ""
    dd:string = ""
    mm:string = ""
    passwd:string = ""
    masterkey:string = ""
    bediener = res_history = paramtext = guest_queasy = None

    shabediener = None

    Shabediener = create_buffer("Shabediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, tmp_userkey, output_userkey, licensenr, i, bediener_pass, bediener_sha1, dd, mm, passwd, masterkey, bediener, res_history, paramtext, guest_queasy
        nonlocal user_name, user_pswd
        nonlocal shabediener


        nonlocal shabediener

        return {"user_found": user_found, "user_token": user_token, "user_key": user_key, "userinit": userinit, "usercode": usercode, "permissions": permissions, "error_code": error_code, "lic_nr": lic_nr, "htl_name": htl_name, "htl_city": htl_city, "htl_adr": htl_adr, "htl_tel": htl_tel, "price_decimal": price_decimal, "coa_format": coa_format, "vhp_licensedate": vhp_licensedate, "vhp_newdb": vhp_newdb}

    def decode_string1(in_str:string):

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, tmp_userkey, output_userkey, licensenr, i, bediener_pass, bediener_sha1, dd, mm, passwd, masterkey, bediener, res_history, paramtext, guest_queasy
        nonlocal user_name, user_pswd
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

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, tmp_userkey, output_userkey, licensenr, i, bediener_pass, bediener_sha1, dd, mm, passwd, masterkey, bediener, res_history, paramtext, guest_queasy
        nonlocal user_name, user_pswd
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


        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Login"


        res_history.aenderung = "User Login with Username: " + bediener.username
    else:

        return generate_output()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    guest_queasy = get_cache (Guest_queasy, {"key": [(eq, "usertoken")],"char1": [(eq, userinit)]})

    if not guest_queasy:
        guest_queasy = Guest_queasy()
        db_session.add(guest_queasy)

        guest_queasy.key = "userToken"
        guest_queasy.date1 = get_current_date()
        guest_queasy.number1 = get_current_time_in_seconds()
        guest_queasy.number3 = 1
        guest_queasy.char3 = licensenr + bediener.username.upper() + user_pswd.upper() + "|" + to_string(get_current_date()) + to_string(get_current_time_in_seconds())
        guest_queasy.char1 = userinit


    else:

        for guest_queasy in db_session.query(Guest_queasy).filter(
                 (Guest_queasy.key == ("userToken").lower()) & (Guest_queasy.char1 == (userinit).lower())).order_by(Guest_queasy.number3.desc()).yield_per(100):
            masterkey = entry(0, guest_queasy.char3, "|")
            break
    tmp_userkey = licensenr + user_name.upper() + user_pswd.upper()
    output_userkey = ""
    for i in range(1,length(tmp_userkey)  + 1) :
        output_userkey = output_userkey + "#" + substring(tmp_userkey, i - 1, 1)
    output_userkey = output_userkey + "#"
    user_key = sha1(output_userkey).hexdigest()
    user_key = user_key.upper()
    error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb = get_output(prepare_main01bl())

    return generate_output()