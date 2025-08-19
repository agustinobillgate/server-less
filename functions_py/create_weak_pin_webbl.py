#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Paramtext

import os

payload_list_data, Payload_list = create_model("Payload_list", {"dummy_input":string, "user_init":string})

def create_weak_pin_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Queasy, Paramtext])

    signature_list_data = []
    output_list_data = []
    epoch_signature = 0
    flag:bool = False
    queasy = paramtext = None

    payload_list = output_list = value_list = signature_list = None

    output_list_data, Output_list = create_model("Output_list", {"dummy_output":string})
    value_list_data, Value_list = create_model("Value_list", {"var_name":string, "value_str":string})
    signature_list_data, Signature_list = create_model("Signature_list", {"var_name":string, "signature":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal signature_list_data, output_list_data, epoch_signature, flag, queasy, paramtext


        nonlocal payload_list, output_list, value_list, signature_list
        nonlocal output_list_data, value_list_data, signature_list_data

        return {"signature-list": signature_list_data, "output-list": output_list_data, "epoch_signature": epoch_signature}

    def create_weak_pins():

        nonlocal signature_list_data, output_list_data, epoch_signature, flag, queasy, paramtext

        nonlocal payload_list, output_list, value_list, signature_list
        nonlocal output_list_data, value_list_data, signature_list_data

        cline:string = ""
        lisvalid:bool = False
        cinvalidhashedpin:string = ""
        counter:int = 0

        # Oscar - 61F94A - fix issue from convertion because INPUT FROM file not handled
        with open("/usr1/serverless/src/additional_files/ListOfWeakPINs.txt", "r") as f:
            for cline in f:
                cinvalidhashedpin = sha1(cline.strip()).hexdigest()
                cinvalidhashedpin = cinvalidhashedpin.upper()
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 362
                queasy.char1 = cinvalidhashedpin


    # Oscar - 61F94A - not used but got converted 
    # def create_signature(user_name:string, value_list_data:[Value_list]):

    #     nonlocal signature_list_data, output_list_data, epoch_signature, flag, queasy, paramtext
    #     nonlocal payload_list, output_list, value_list, signature_list
    #     nonlocal output_list_data, signature_list_data

    #     epoch = 0
    #     dtz1 = None
    #     dtz2 = None
    #     lic_nr:string = ""
    #     data:string = ""
    #     value_str:string = ""

    #     def generate_inner_output():
    #         return (epoch, signature_list_data)

    #     paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    #     if paramtext and paramtext.ptexte != "":
    #         lic_nr = decode_string(paramtext.ptexte)
    #     dtz1 = get_current_datetime()
    #     dtz2 = parse("1970-01-01T00:00:00.000+0:00")
    #     epoch = get_interval(dtz1, dtz2, "milliseconds")

    #     for value_list in query(value_list_data):
    #         value_str = value_list.value_str.lower()

    #         if value_str == "yes":
    #             value_str = "true"
    #         elif value_str == "no":
    #             value_str = "false"
    #         data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
    #         signature_list = Signature_list()
    #         signature_list_data.append(signature_list)

    #         signature_list.var_name = value_list.var_name
    #         signature_list.signature = sha1(data).hexdigest()

    #     return generate_inner_output()

    # Oscar - 61F94A - fix issue from convertion because SEARCH not handled
    if os.path.exists("/usr1/serverless/src/additional_files/ListOfWeakPINs.txt") != None:

        # Oscar - 61F94A - fix issue from convertion because OPSYS not handled
        if os.name == "posix":
            queasy = get_cache(Queasy, {"key": [(eq, 362)]})

            if not queasy:
                create_weak_pins()

    return generate_output()