#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Htparam

payload_list_list, Payload_list = create_model("Payload_list", {"hashed_pass":string, "int_input":int, "vmode":string})

def check_password_webbl(user_name:string, payload_list_list:[Payload_list]):

    prepare_cache ([Paramtext, Htparam])

    response_list_list = []
    epoch_signature = 0
    signature_list_list = []
    hashed_pass:string = ""
    int_input:int = 0
    vmode:string = ""
    success_status:bool = False
    msg_str:string = ""
    err_no:int = 0
    hashed_from_be:string = ""
    licensenr:string = ""
    paramtext = htparam = None

    payload_list = response_list = value_list = signature_list = None

    response_list_list, Response_list = create_model("Response_list", {"success_status":bool, "msg_str":string, "err_no":int})
    value_list_list, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_list, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal response_list_list, epoch_signature, signature_list_list, hashed_pass, int_input, vmode, success_status, msg_str, err_no, hashed_from_be, licensenr, paramtext, htparam
        nonlocal user_name


        nonlocal payload_list, response_list, value_list, signature_list
        nonlocal response_list_list, value_list_list, signature_list_list

        return {"response-list": response_list_list, "epoch_signature": epoch_signature, "signature-list": signature_list_list}

    def checker_hash():

        nonlocal response_list_list, epoch_signature, signature_list_list, hashed_pass, int_input, vmode, success_status, msg_str, err_no, hashed_from_be, licensenr, paramtext, htparam
        nonlocal user_name


        nonlocal payload_list, response_list, value_list, signature_list
        nonlocal response_list_list, value_list_list, signature_list_list

        if vmode.lower()  == ("genparam").lower() :

            htparam = get_cache (Htparam, {"paramnr": [(eq, int_input)]})

            if htparam:

                if htparam.fchar != "" and htparam.fchar != None:

                    if num_entries(htparam.fchar, ";") >= 4:
                        hashed_from_be = sha1(entry(3, htparam.fchar, ";").hexdigest())

                        if hashed_pass.lower()  == (hashed_from_be).lower() :
                            success_status = True
                            gen_signature()
                            msg_str = ""
                            err_no = 0
                        else:
                            success_status = True
                            gen_signature()
                            msg_str = "Password is incorrect."
                            err_no = 1
                    else:
                        success_status = True
                        gen_signature()
                        msg_str = "Improper parameter configuration."
                        err_no = 2
                else:
                    success_status = True
                    gen_signature()
                    msg_str = ""
                    err_no = 0
            else:
                success_status = True
                gen_signature()
                msg_str = "Parameter is not found."
                err_no = 3

        elif vmode.lower()  == ("genparamplain").lower() :

            htparam = get_cache (Htparam, {"paramnr": [(eq, int_input)]})

            if htparam and htparam.bezeichnung.lower()  != ("not used").lower() :

                if htparam.fchar != "" and htparam.fchar != None:
                    hashed_from_be = sha1(htparam.fchar).hexdigest()

                    if hashed_pass.lower()  == (hashed_from_be).lower() :
                        success_status = True
                        gen_signature()
                        msg_str = ""
                        err_no = 0
                    else:
                        success_status = True
                        gen_signature()
                        msg_str = "Password is incorrect."
                        err_no = 1
                else:
                    success_status = True
                    gen_signature()
                    msg_str = ""
                    err_no = 0
            else:
                success_status = True
                gen_signature()
                msg_str = "Parameter is not found."
                err_no = 3

        elif vmode.lower()  == ("cekpassword").lower() :

            htparam = get_cache (Htparam, {"paramnr": [(eq, int_input)]})

            if htparam and htparam.bezeichnung.lower()  != ("not used").lower() :

                if htparam.fchar != "" and htparam.fchar != None:
                    success_status = True
                    msg_str = "Password Exist"
                    err_no = 1
                else:
                    success_status = True
                    msg_str = "No Password"
                    err_no = 0
            else:
                success_status = True
                msg_str = "Parameter is not found."
                err_no = 3


    def gen_signature():

        nonlocal response_list_list, epoch_signature, signature_list_list, hashed_pass, int_input, vmode, success_status, msg_str, err_no, hashed_from_be, licensenr, paramtext, htparam
        nonlocal user_name


        nonlocal payload_list, response_list, value_list, signature_list
        nonlocal response_list_list, value_list_list, signature_list_list


        value_list = Value_list()
        value_list_list.append(value_list)

        value_list.var_name = "success-status"
        value_list.value_str = to_string(success_status)


        epoch_signature, signature_list_list = create_signature(user_name, value_list_list)


    def create_signature(user_name:string, value_list_list:[Value_list]):

        nonlocal response_list_list, epoch_signature, signature_list_list, hashed_pass, int_input, vmode, success_status, msg_str, err_no, hashed_from_be, licensenr, paramtext, htparam
        nonlocal payload_list, response_list, value_list, signature_list
        nonlocal response_list_list, signature_list_list

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

        nonlocal response_list_list, epoch_signature, signature_list_list, hashed_pass, int_input, vmode, success_status, msg_str, err_no, hashed_from_be, licensenr, paramtext, htparam
        nonlocal user_name


        nonlocal payload_list, response_list, value_list, signature_list
        nonlocal response_list_list, value_list_list, signature_list_list

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

    payload_list = query(payload_list_list, first=True)

    if payload_list:
        hashed_pass = payload_list.hashed_pass
        int_input = payload_list.int_input
        vmode = payload_list.vmode


        checker_hash()
        response_list = Response_list()
        response_list_list.append(response_list)

        response_list.success_status = success_status
        response_list.msg_str = msg_str
        response_list.err_no = err_no

    return generate_output()