#using conversion tools version: 1.0.0.117

# ================================================
# Rulita, 13-10-2025 
# Tiket ID : 8CF423
# Issue table countries-lang, hotels,
#    Whitelist_ip, logs belum ada di db serverless
# ================================================

from functions.additional_functions import *
from decimal import Decimal
from functions.verify_user_login_callsetup_wizardbl import verify_user_login_callsetup_wizardbl
from functions.get_bediener_info_callsetup_wizardbl import get_bediener_info_callsetup_wizardbl

def logsrv_auth_setup_wizardbl(country_id:string, user_name:string, user_pswd:string, headers:string):
    languages_list_data = []
    t_output_list_data = []
    bediener_info_data = []
    signature_list_data = []
    hotel_code:string = ""
    hotel_ip:string = ""
    hotel_port:string = ""
    lreturn:bool = False
    htlappparam:string = ""
    vhost:string = ""
    vservice:string = ""
    user_found:bool = False
    whitelist_pass:bool = False
    user_code:string = ""
    hotel_grp:int = 0
    ip_address:string = ""

    languages_list = t_output_list = bediener_info = signature_list = value_list = None

    languages_list_data, Languages_list = create_model("Languages_list", {"lang_id":string, "lang_variable":string, "lang_value":string})
    t_output_list_data, T_output_list = create_model("T_output_list", {"i_result":int, "user_token":string, "user_key":string, "user_init":string, "permissions":string, "htl_url":string, "err_message":string, "error_code":int, "lic_nr":string, "htl_name":string, "htl_city":string, "epoch_signature":int, "hotel_schema":string}, {"user_token": "", "user_key": "", "user_init": "", "permissions": "", "htl_url": "", "err_message": "", "lic_nr": "", "htl_name": "", "htl_city": "", "hotel_schema": ""})
    bediener_info_data, Bediener_info = create_model("Bediener_info", {"user_number":int, "user_init":string, "user_name":string, "dept_number":int, "dept_name":string, "email":string, "mobile":string, "pager":string, "totp_flag":bool, "totp_status":string, "found_user":bool})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal languages_list_data, t_output_list_data, bediener_info_data, signature_list_data, hotel_code, hotel_ip, hotel_port, lreturn, htlappparam, vhost, vservice, user_found, whitelist_pass, user_code, hotel_grp, ip_address
        nonlocal country_id, user_name, user_pswd, headers


        nonlocal languages_list, t_output_list, bediener_info, signature_list, value_list
        nonlocal languages_list_data, t_output_list_data, bediener_info_data, signature_list_data, value_list_data

        return {"languages-list": languages_list_data, "t-output-list": t_output_list_data, "bediener-info": bediener_info_data, "signature-list": signature_list_data}

    def get_header_value(input_key:string):

        nonlocal languages_list_data, t_output_list_data, bediener_info_data, signature_list_data, hotel_code, hotel_ip, hotel_port, lreturn, htlappparam, vhost, vservice, user_found, whitelist_pass, user_code, hotel_grp, ip_address
        nonlocal country_id, user_name, user_pswd, headers


        nonlocal languages_list, t_output_list, bediener_info, signature_list, value_list
        nonlocal languages_list_data, t_output_list_data, bediener_info_data, signature_list_data, value_list_data

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


    def check_whitelist_ip(ip_address:string, hotel_code:string, group_number:int):

        nonlocal languages_list_data, t_output_list_data, bediener_info_data, signature_list_data, hotel_ip, hotel_port, lreturn, htlappparam, vhost, vservice, user_found, whitelist_pass, user_code, hotel_grp, country_id, user_name, user_pswd, headers


        nonlocal languages_list, t_output_list, bediener_info, signature_list, value_list
        nonlocal languages_list_data, t_output_list_data, bediener_info_data, signature_list_data, value_list_data

        ok_flag = False

        def generate_inner_output():
            return (ok_flag)


        whitelist_ip = db_session.query(Whitelist_ip).filter(# type:ignore
                 (Whitelist_ip.htl_code == (hotel_code).lower()) & (Whitelist_ip.group_number == group_number) & (Whitelist_ip.ip == (ip_address).lower())).first()# type:ignore

        if whitelist_ip:
            ok_flag = True

        return generate_inner_output()

    t_output_list = T_output_list()
    t_output_list_data.append(t_output_list)


    if num_entries(user_name, "@") != 2:
        t_output_list.i_result = 1
        t_output_list.err_message = "Incorrect username or password. Please try again."

        return generate_output()
    hotel_code = entry(1, user_name, "@")
    user_name = entry(0, user_name, "@")

    hotels = db_session.query(Hotels).filter(# type:ignore
             (Hotels.htl_code == (hotel_code).lower())).first()# type:ignore

    if not hotels:
        t_output_list.i_result = 2
        t_output_list.err_message = "Invalid hotel code."

        return generate_output()
    else:

        if headers != "":
            headers = replace_str(replace_str(headers, "{", "") , "}", "")
            headers = replace_str(replace_str(headers, "[", "") , "]", "")
            ip_address = get_header_value("x-forwarded-for")

            if ip_address == "":
                ip_address = get_header_value("x-real-ip")

            if ip_address == "":
                ip_address = get_header_value("host")
            ip_address = entry(0, ip_address, ":")

        whitelist_ip = db_session.query(Whitelist_ip).filter(# type:ignore
                 (Whitelist_ip.htl_code == hotels.htl_code) & (Whitelist_ip.group_number == 0) & (Whitelist_ip.ip == ("active").lower())).first()# type:ignore

        if whitelist_ip:
            whitelist_pass = check_whitelist_ip(ip_address, hotels.htl_code, 0)

            if not whitelist_pass and hotels.htl_grpnr != 0:

                hotel_group = db_session.query(Hotel_group).filter(# type:ignore
                         (Hotel_group.group_number == hotels.htl_grpnr)).first()# type:ignore

                if hotel_group:
                    whitelist_pass = check_whitelist_ip(ip_address, "", hotels.htl_grpnr)

            if not whitelist_pass:
                whitelist_pass = check_whitelist_ip(ip_address, "", 0)
        else:
            whitelist_pass = True

    if not whitelist_pass:
        t_output_list.i_result = 401
        t_output_list.err_message = "Unauthorized Network"
        logs = Logs()# type:ignore
        logs_data.append(logs)# type:ignore

        logs.key = "Login Setup Wizard"
        logs.value_str = "Login Attempt Failed: Username=" + user_name + " Hotelcode=" + hotel_code + " IP=" + ip_address
        logs.datum = get_current_date()
        logs.zeit = get_current_time_in_seconds()

        return generate_output()
    vhost = hotels.htl_ip
    vservice = to_string(hotels.htl_port)
    htlappparam = " -H " + vhost + " -S " + vservice + " -DirectConnect -sessionModel Session-free"


    lreturn = set_combo_session(htlappparam, None , None , None)

    if not lreturn:
        t_output_list.i_result = 3
        t_output_list.err_message = "Unable to connect to the hotel server."
        lreturn = reset_combo_session()


        return generate_output()
    t_output_list.hotel_schema = hotel_code
    local_storage.combo_flag = True
    user_found, t_output_list.user_token, t_output_list.user_key, t_output_list.user_init, user_code, t_output_list.permissions, t_output_list.error_code, t_output_list.lic_nr, t_output_list.htl_name, t_output_list.htl_city = get_output(verify_user_login_callsetup_wizardbl(user_name, user_pswd, headers))
    local_storage.combo_flag = False


    if error_code == 0 and user_found:# type:ignore
        local_storage.combo_flag = True
        t_output_list.epoch_signature, bediener_info_data, signature_list_data = get_output(get_bediener_info_callsetup_wizardbl(user_found, user_name, t_output_list.user_init))
        local_storage.combo_flag = False

    lreturn = reset_combo_session()
    lreturn = False


    if not user_found:

        if t_output_list.error_code == 101:
            t_output_list_data.clear()
            t_output_list = T_output_list()
            t_output_list_data.append(t_output_list)

            t_output_list.i_result = 101
            t_output_list.err_message = "Login failed. Your account is inactive."
            user_code = ""
            t_output_list.error_code = 101


        else:
            t_output_list_data.clear()
            t_output_list = T_output_list()
            t_output_list_data.append(t_output_list)

            t_output_list.i_result = 1
            t_output_list.err_message = "Incorrect username or password. Please try again."
            user_code = ""
            t_output_list.error_code = 1

        return generate_output()

    elif t_output_list.error_code == 1001:
        t_output_list_data.clear()
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.i_result = 1001
        t_output_list.err_message = "GenParam Group 99 Was Manually Changed"
        user_code = ""
        t_output_list.error_code = 1001

        return generate_output()

    elif t_output_list.error_code == 1002:
        t_output_list_data.clear()
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.i_result = 1002
        t_output_list.err_message = "Hotel Name / City / LicenseNo Not Defined"
        user_code = ""
        t_output_list.error_code = 1002

        return generate_output()

    elif t_output_list.error_code == 1003:
        t_output_list_data.clear()
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.i_result = 1003
        t_output_list.err_message = "Room License = 0"
        user_code = ""
        t_output_list.error_code = 1003

        return generate_output()

    elif t_output_list.error_code == 1004:
        t_output_list_data.clear()
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.i_result = 1004
        t_output_list.err_message = "Invalid Room License"
        user_code = ""
        t_output_list.error_code = 1004

        return generate_output()

    elif t_output_list.error_code == 1005:
        t_output_list_data.clear()
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.i_result = 1005
        t_output_list.err_message = "Invalid POS License"
        user_code = ""
        t_output_list.error_code = 1005

        return generate_output()

    elif t_output_list.error_code == 1006:
        t_output_list_data.clear()
        t_output_list = T_output_list()
        t_output_list_data.append(t_output_list)

        t_output_list.i_result = 1006
        t_output_list.err_message = "Serial Number Incorrect"
        user_code = ""
        t_output_list.error_code = 1006

        return generate_output()

    if num_entries(hotels.htl_url, "|") >= 2:
        t_output_list.htl_url = entry(0, hotels.htl_url, "|")
    else:
        t_output_list.htl_url = hotels.htl_url
    t_output_list.err_message = "Login Success"

    return generate_output()