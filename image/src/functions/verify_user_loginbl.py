from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.get_user_tokenbl import get_user_tokenbl
from functions.prepare_main01bl import prepare_main01bl
from models import Bediener, Paramtext, Guest_queasy

def verify_user_loginbl(user_name:str, user_pswd:str):
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
    tmp_userkey:str = ""
    output_userkey:str = ""
    licensenr:str = ""
    i:int = 0
    dd:str = ""
    mm:str = ""
    passwd:str = ""
    masterkey:str = ""
    bediener = paramtext = guest_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, tmp_userkey, output_userkey, licensenr, i, dd, mm, passwd, masterkey, bediener, paramtext, guest_queasy


        return {"user_found": user_found, "user_token": user_token, "user_key": user_key, "userinit": userinit, "usercode": usercode, "permissions": permissions, "error_code": error_code, "lic_nr": lic_nr, "htl_name": htl_name, "htl_city": htl_city, "htl_adr": htl_adr, "htl_tel": htl_tel, "price_decimal": price_decimal, "coa_format": coa_format, "vhp_licensedate": vhp_licensedate, "vhp_newdb": vhp_newdb}

    def decode_string1(in_str:str):

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, tmp_userkey, output_userkey, licensenr, i, dd, mm, passwd, masterkey, bediener, paramtext, guest_queasy

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

        nonlocal user_found, user_token, user_key, userinit, usercode, permissions, error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb, tmp_userkey, output_userkey, licensenr, i, dd, mm, passwd, masterkey, bediener, paramtext, guest_queasy

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


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.username) == (user_name).lower()) &  (Bediener.flag == 0)).first()

    if not bediener and user_name.lower()  == "sindata":

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (user_name).lower()) &  (Bediener.betriebsnr == 1)).first()

        if not bediener:
            user_found = False

            return generate_output()

    if user_name.lower()  == "sindata" and bediener.flag == 1:
        dd = to_string(get_day(get_current_date() + 1) , "99")
        dd = substring(dd, 1, 1) + substring(dd, 0, 1)
        mm = to_string(get_month(get_current_date() + 1) , "99")
        mm = substring(mm, 1, 1) + substring(mm, 0, 1)
        user_found = (user_pswd == ("SystemAdmin@" + dd + mm) and ord(substring(user_pswd, 0, 1)) == 83 and ord(substring(user_pswd, 6, 1)) == 65)


    else:
        passwd = decode_string1(bediener.usercode)
        user_found = (passwd == user_pswd)

    if user_found:
        userinit = bediener.userinit
        usercode = bediener.usercode
        permissions = bediener.permissions


    else:

        return generate_output()

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    guest_queasy = db_session.query(Guest_queasy).filter(
            (func.lower(Guest_queasy.key) == "userToken".lower()) &  (Guest_queasy.char1 == userinit)).first()

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
                (func.lower(Guest_queasy.key) == "userToken".lower()) &  (Guest_queasy.char1 == userinit)).all():
            masterkey = entry(0, guest_queasy.char3, "|")
            break
    user_token = get_output(get_user_tokenbl(bediener.userinit, "", "", masterkey))
    tmp_userkey = licensenr + user_name.upper() + user_pswd.upper()
    output_userkey = ""
    for i in range(1,len(tmp_userkey)  + 1) :
        output_userkey = output_userkey + "#" + substring(tmp_userkey, i - 1, 1)
    output_userkey = output_userkey + "#"
    user_key = sha1(output_userkey).hexdigest()
    user_key = user_key.upper()
    error_code, lic_nr, htl_name, htl_city, htl_adr, htl_tel, price_decimal, coa_format, vhp_licensedate, vhp_newdb = get_output(prepare_main01bl())

    return generate_output()