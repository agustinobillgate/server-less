#using conversion tools version: 1.0.0.118
#-----------------------------------------
# Rd, 4/8/2025
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Queasy, Res_history, Paramtext

def disable_totpbl(user_init:string, user_init_will_disable:string, userotp:string, reason:string):

    prepare_cache ([Bediener, Res_history, Paramtext])

    result_message = ""
    # totpok = FALSE
    totpok = False
    epoch_signature = 0
    signature_list_data = []
    secretkey:string = ""
    generatedotp:string = ""
    cmd:string = ""
    result:string = ""
    returnstatus:int = 0
    foldername:string = ""
    filename:string = ""
    bediener = queasy = res_history = paramtext = None

    value_list = signature_list = opr_bediener = terminate_totp = None

    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    Opr_bediener = create_buffer("Opr_bediener",Bediener)
    Terminate_totp = create_buffer("Terminate_totp",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, totpok, epoch_signature, signature_list_data, secretkey, generatedotp, cmd, result, returnstatus, foldername, filename, bediener, queasy, res_history, paramtext
        nonlocal user_init, user_init_will_disable, userotp, reason
        nonlocal opr_bediener, terminate_totp


        nonlocal value_list, signature_list, opr_bediener, terminate_totp
        nonlocal value_list_data, signature_list_data

        return {"result_message": result_message, "totpok": totpok, "epoch_signature": epoch_signature, "signature-list": signature_list_data}

    def create_signature(user_name:string, value_list_data:[Value_list]):

        nonlocal result_message, totpok, epoch_signature, signature_list_data, secretkey, generatedotp, cmd, result, returnstatus, foldername, filename, bediener, queasy, res_history, paramtext
        nonlocal user_init, user_init_will_disable, userotp, reason
        nonlocal opr_bediener, terminate_totp


        nonlocal value_list, signature_list, opr_bediener, terminate_totp
        nonlocal signature_list_data

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

        nonlocal result_message, totpok, epoch_signature, signature_list_data, secretkey, generatedotp, cmd, result, returnstatus, foldername, filename, bediener, queasy, res_history, paramtext
        nonlocal user_init, user_init_will_disable, userotp, reason
        nonlocal opr_bediener, terminate_totp


        nonlocal value_list, signature_list, opr_bediener, terminate_totp
        nonlocal value_list_data, signature_list_data

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

    if (reason == "" or reason == None):
        result_message = "reason Is Mandatory!"

        return generate_output()

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init_will_disable)]})

    if bediener:

        if matches(bediener.username,r"*sindata*"):
            totpok = False
            value_list = Value_list()
            value_list_data.append(value_list)

            value_list.var_name = "totpok"
            value_list.value_str = to_string(totpok)


            epoch_signature, signature_list_data = create_signature(bediener.username, value_list_data)
            result_message = "Not Allowed Procedure"

            return generate_output()
    pass

    opr_bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if opr_bediener:

        if matches(opr_bediener.username,r"*sindata*"):
            totpok = True

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init_will_disable)]})

            if bediener:

                queasy = get_cache (Queasy, {"key": [(eq, 341)],"char1": [(eq, bediener.username)]})

                if queasy:
                    pass
                    db_session.delete(queasy)
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = opr_bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Disable TOTP For User: " + bediener.username + " reason: " + reason
                    res_history.action = "User"


                    result_message = "TOTP Disable Succesfull"
                else:
                    result_message = "TOTP Already Disabled"
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "totpok"
                value_list.value_str = to_string(totpok)


                epoch_signature, signature_list_data = create_signature(opr_bediener.username, value_list_data)
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 341)],"char1": [(eq, opr_bediener.username)]})

            if not queasy:
                totpok = False
                value_list = Value_list()
                value_list_data.append(value_list)

                value_list.var_name = "totpok"
                value_list.value_str = to_string(totpok)


                epoch_signature, signature_list_data = create_signature(opr_bediener.username, value_list_data)
                result_message = "TOTP Not Configured"

                return generate_output()
            else:
                secretkey = queasy.char2
                # filename = "check_totp_" + userotp + ".txt"

                # if OPSYS.lower()  == ("WIN32").lower() :
                #     cmd = "wsl oathtool --totp -b " + secretkey + " > " + filename
                #     OS_COMMAND SILENT VALUE (cmd)
                # else:
                #     foldername = "/usr1/vhp/tmp/totp/"
                #     UNIX SILENT VALUE ("mkdir /usr1/vhp")
                #     UNIX SILENT VALUE ("mkdir /usr1/vhp/tmp")
                #     UNIX SILENT VALUE ("mkdir " + foldername)
                #     filename = foldername + filename
                #     cmd = "oathtool --totp -b " + secretkey + " > " + filename
                #     UNIX SILENT VALUE (cmd)
                #     INPUT FROM VALUE (filename)
                #     IMPORT UNFORMATTED result
                #     INPUT CLOSE
                #     OS_DELETE VALUE (filename)
                #     result = trim(result)
                result = check_otp(secretkey)

                    if userotp.lower()  == (result).lower() :
                        totpok = True

                        bediener = get_cache (Bediener, {"userinit": [(eq, user_init_will_disable)]})

                        if bediener:

                            queasy = get_cache (Queasy, {"key": [(eq, 341)],"char1": [(eq, bediener.username)]})

                            if queasy:
                                pass
                                db_session.delete(queasy)
                                res_history = Res_history()
                                db_session.add(res_history)

                                res_history.nr = opr_bediener.nr
                                res_history.datum = get_current_date()
                                res_history.zeit = get_current_time_in_seconds()
                                res_history.aenderung = "Disable TOTP For User: " + bediener.username + " reason: " + reason
                                res_history.action = "User"


                                result_message = "TOTP Disable Succesfull"
                            else:
                                result_message = "TOTP Already Disabled"
                    else:
                        result_message = "TOTP Not Match"
                    value_list = Value_list()
                    value_list_data.append(value_list)

                    value_list.var_name = "totpok"
                    value_list.value_str = to_string(totpok)


                    epoch_signature, signature_list_data = create_signature(opr_bediener.username, value_list_data)
    else:
        totpok = False
        result_message = "User Not Found!"
        value_list = Value_list()
        value_list_data.append(value_list)

        value_list.var_name = "totpok"
        value_list.value_str = to_string(totpok)


        epoch_signature, signature_list_data = create_signature("", value_list_data)

        return generate_output()

    return generate_output()