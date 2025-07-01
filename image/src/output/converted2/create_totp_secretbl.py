#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
import random
from models import Bediener, Queasy, Res_history, Paramtext

def create_totp_secretbl(user_name:string, hotel_code:string):

    prepare_cache ([Bediener, Queasy, Res_history, Paramtext])

    totpuri = ""
    recoverycode = ""
    epoch_signature = 0
    signature_list_list = []
    base32chars:string = ""
    randombyte:int = 0
    i:int = 0
    issuer:string = "VHP"
    algorithm:string = ""
    digits:int = 0
    period:int = 0
    totpsecret:string = ""
    bediener = queasy = res_history = paramtext = None

    value_list = signature_list = None

    value_list_list, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_list, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal totpuri, recoverycode, epoch_signature, signature_list_list, base32chars, randombyte, i, issuer, algorithm, digits, period, totpsecret, bediener, queasy, res_history, paramtext
        nonlocal user_name, hotel_code


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

        return {"totpuri": totpuri, "recoverycode": recoverycode, "epoch_signature": epoch_signature, "signature-list": signature_list_list}

    def create_signature(user_name:string, value_list_list:[Value_list]):

        nonlocal totpuri, recoverycode, epoch_signature, signature_list_list, base32chars, randombyte, i, issuer, algorithm, digits, period, totpsecret, bediener, queasy, res_history, paramtext
        nonlocal hotel_code


        nonlocal value_list, signature_list
        nonlocal signature_list_list

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:string = ""
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_list)


        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_list):
            value_str = value_list.value_str.lower()

            if value_str == "yes":
                value_str = "true"
            elif value_str == "no":
                value_str = "false"
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_list.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal totpuri, recoverycode, epoch_signature, signature_list_list, base32chars, randombyte, i, issuer, algorithm, digits, period, totpsecret, bediener, queasy, res_history, paramtext
        nonlocal user_name, hotel_code


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

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


    base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    totpsecret = ""
    for i in range(1,16 + 1) :
        randombyte = random.randint(0, 31)
        totpsecret = totpsecret + substring(base32chars, randombyte + 1 - 1, 1)
    for i in range(1,16 + 1) :
        randombyte = random.randint(0, 31)
        recoverycode = recoverycode + substring(base32chars, randombyte + 1 - 1, 1)
    algorithm = "SHA1"
    digits = 6
    period = 30
    totpuri = "otpauth://totp/" + user_name + "@" + hotel_code + "?secret=" + totpsecret + "&issuer=" + issuer + "&algorithm=" + algorithm + "&digits=" + to_string(digits) + "&period=" + to_string(period)

    bediener = get_cache (Bediener, {"username": [(eq, user_name)]})

    if bediener:

        queasy = get_cache (Queasy, {"key": [(eq, 341)],"char1": [(eq, bediener.username)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 341
            queasy.char1 = bediener.username
            queasy.char2 = totpsecret
            queasy.char3 = ""
            queasy.logi1 = False
            queasy.number2 = get_current_time_in_seconds()
            queasy.date2 = get_current_date()


            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Create Two-Factor Authentication"
            res_history.action = "User"


        else:
            pass
            queasy.char2 = totpsecret
            queasy.logi1 = False
            pass
        pass
        value_list = Value_list()
        value_list_list.append(value_list)

        value_list.var_name = "totpuri"
        value_list.value_str = totpuri


        epoch_signature, signature_list_list = create_signature(bediener.username, value_list_list)

    return generate_output()