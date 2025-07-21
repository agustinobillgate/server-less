#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 21/7/2025
# name table bediener, sama dengan nama parameter output
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Queasy, Paramtext

def get_bediener_info_webbl(user_name:string, user_init:string):

    prepare_cache ([bediener, Queasy, Paramtext])

    epoch_signature = 0
    bediener = False
    bediener_info_data = []
    signature_list_data = []
    dept_name:string = ""
    bediener = queasy = paramtext = None

    bediener_info = value_list = signature_list = bediener_buff = buff_user = bdept = totpdata = None

    bediener_info_data, Bediener_info = create_model("Bediener_info", {"user_number":int, "user_init":string, "user_name":string, "dept_number":int, "dept_name":string, "email":string, "mobile":string, "pager":string, "totp_flag":bool, "totp_status":string})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    Bediener_buff = create_buffer("Bediener_buff",Bediener)
    Buff_user = create_buffer("Buff_user",Queasy)
    Bdept = create_buffer("Bdept",Queasy)
    Totpdata = create_buffer("Totpdata",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal epoch_signature, bediener, bediener_info_data, signature_list_data, dept_name, bediener, queasy, paramtext
        nonlocal user_name, user_init
        nonlocal bediener_buff, buff_user, bdept, totpdata


        nonlocal bediener_info, value_list, signature_list, bediener_buff, buff_user, bdept, totpdata
        nonlocal bediener_info_data, value_list_data, signature_list_data

        return {"epoch_signature": epoch_signature, "bediener": bediener, "bediener-info": bediener_info_data, "signature-list": signature_list_data}

    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal epoch_signature, bediener, bediener_info_data, signature_list_data, dept_name, bediener, queasy, paramtext
        nonlocal user_init
        nonlocal bediener_buff, buff_user, bdept, totpdata


        nonlocal bediener_info, value_list, signature_list, bediener_buff, buff_user, bdept, totpdata
        nonlocal bediener_info_data, signature_list_data

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_data)


        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_data):
            value_str = value_list.value_str.lower()

            if value_str == "yes":
                value_str = "true"
            elif value_str == "no":
                value_str = "false"
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_data.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal epoch_signature, bediener, bediener_info_data, signature_list_data, dept_name, bediener, queasy, paramtext
        nonlocal user_name, user_init
        nonlocal bediener_buff, buff_user, bdept, totpdata


        nonlocal bediener_info, value_list, signature_list, bediener_buff, buff_user, bdept, totpdata
        nonlocal bediener_info_data, value_list_data, signature_list_data

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


    bediener_buff = get_cache (bediener, {"userinit": [(eq, user_init)],"username": [(eq, user_name)]})

    if bediener_buff:

        buff_user = get_cache (Queasy, {"key": [(eq, 134)],"number1": [(eq, bediener_buff.nr)],"betriebsnr": [(eq, 0)],"deci1": [(eq, 0)],"logi1": [(eq, False)]})

        bdept = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, bediener.user_group)]})

        if bdept:
            dept_name = bdept.char3
        else:
            dept_name = ""
        bediener_info = Bediener_info()
        bediener_info_data.append(bediener_info)

        bediener_info.user_number = bediener_buff.nr
        bediener_info.user_init = bediener_buff.userinit
        bediener_info.user_name = bediener_buff.username
        bediener_info.dept_number = bediener_buff.user_group
        bediener_info.dept_name = dept_name
        bediener_info.email = buff_user.char2
        bediener_info.mobile = buff_user.char1
        bediener_info.pager = buff_user.char3

        totpdata = get_cache (Queasy, {"key": [(eq, 341)],"char1": [(eq, bediener.username)]})

        if totpdata:
            bediener_info.totp_flag = True

            if totpdata.logi1 :
                bediener_info.totp_status = "ACTIVE"
            else:
                bediener_info.totp_status = "INACTIVE"
        else:
            bediener_info.totp_flag = False
        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "totp-flag"
        value_list.value_str = to_string(bediener_info.totp_flag)


        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "totp-status"
        value_list.value_str = bediener_info.totp_status


        epoch_signature, signature_list_data = create_signature(bediener_buff.username, value_list_data)

    return generate_output()