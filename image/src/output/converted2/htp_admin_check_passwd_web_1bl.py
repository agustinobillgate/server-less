#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from models import Paramtext

def htp_admin_check_passwd_web_1bl(user_name:string, id_str:string, grp_no:int):

    prepare_cache ([Paramtext])

    passwd_ok = False
    epoch_signature = 0
    signature_list_list = []
    fchar:string = ""
    pswd_str:string = ""
    nanci:string = ""
    s:string = ""
    i:int = 0
    licensenr:string = ""
    paramtext = None

    value_list = signature_list = None

    value_list_list, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_list, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal passwd_ok, epoch_signature, signature_list_list, fchar, pswd_str, nanci, s, i, licensenr, paramtext
        nonlocal user_name, id_str, grp_no


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

        return {"passwd_ok": passwd_ok, "epoch_signature": epoch_signature, "signature-list": signature_list_list}

    def aufbau(i:int, ch:string):

        nonlocal passwd_ok, epoch_signature, signature_list_list, fchar, pswd_str, nanci, s, licensenr, paramtext
        nonlocal user_name, id_str, grp_no


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list

        def generate_inner_output():
            return (ch)


        if substring(proversion(), 0, 1) == ("1").lower() :

            if i == 1:
                ch = ch + "g"

            elif i == 2 or i == 4:
                ch = ch + "e"

            elif i == 3:
                ch = ch + "h"

            elif i == 5 or i == 8:
                ch = ch + "i"

            elif i == 6 or i == 7:
                ch = ch + "n"

            elif i == 9:
                ch = ch + "s"
        else:

            if i == 1:
                ch = ch + "g"

            elif i == 2 or i == 4:
                ch = ch + "e"

            elif i == 3:
                ch = ch + "h"

            elif i == 5 or i == 8:
                ch = ch + "i"

            elif i == 6 or i == 7:
                ch = ch + "m"

            elif i == 9:
                ch = ch + "s"

        return generate_inner_output()


    def gen_signature():

        nonlocal passwd_ok, epoch_signature, signature_list_list, fchar, pswd_str, nanci, s, i, licensenr, paramtext
        nonlocal user_name, id_str, grp_no


        nonlocal value_list, signature_list
        nonlocal value_list_list, signature_list_list


        value_list = Value_list()
        value_list_list.append(value_list)

        value_list.var_name = "passwdOk"
        value_list.value_str = to_string(passwd_ok)


        epoch_signature, signature_list_list = create_signature(user_name, value_list_list)


    def create_signature(user_name:string, value_list_list:[Value_list]):

        nonlocal passwd_ok, epoch_signature, signature_list_list, fchar, pswd_str, nanci, s, i, licensenr, paramtext
        nonlocal id_str, grp_no


        nonlocal value_list, signature_list
        nonlocal signature_list_list

        epoch = 0
        dtz1 = None
        dtz2 = None
        data:string = ""
        value_str:string = ""

        def generate_inner_output():
            return (epoch, signature_list_list)

        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_list):
            value_str = value_list.value_str.lower()

            if value_str == "yes":
                value_str = "true"
            elif value_str == "no":
                value_str = "false"
            data = value_str + "-" + to_string(epoch) + "-" + to_string(licensenr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_list.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:string):

        nonlocal passwd_ok, epoch_signature, signature_list_list, fchar, pswd_str, nanci, i, licensenr, paramtext
        nonlocal user_name, id_str, grp_no


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

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    if grp_no == 10:
        fchar = get_output(htpchar(1071))

        if trim(fchar) == "":
            passwd_ok = True
            gen_signature()

            return generate_output()
        pswd_str = fchar

    if grp_no == 10:
        nanci = pswd_str

    elif grp_no == 99:
        for i in range(1,9 + 1) :
            nanci = aufbau(i, nanci)
        s = s + substring(to_string(get_month(get_current_date()) , "99") , 1, 1) + substring(to_string(get_month(get_current_date()) , "99") , 0, 1) + substring(to_string(get_day(get_current_date()) , "99") , 1, 1) + substring(to_string(get_day(get_current_date()) , "99") , 0, 1)
        nanci = nanci + s

    if nanci.lower()  == (id_str).lower() :
        passwd_ok = True
    gen_signature()

    return generate_output()