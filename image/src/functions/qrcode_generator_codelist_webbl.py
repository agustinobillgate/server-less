from functions.additional_functions import *
import decimal
from datetime import date
from functions.qrcode_generatorbl import qrcode_generatorbl

def qrcode_generator_codelist_webbl(num_of_qr:int, type_code:int, licensenr:int):
    code_list_list = []
    encodedtext:str = ""
    dataqr:str = ""
    pathqr:str = ""
    dirqr:str = ""
    msg_result:str = ""
    initial_date:date = None
    int_date:int = 0
    int_time:int = 0
    outlet_number:int = 0
    count_i:int = 0
    curr_zeit:int = 0
    time_j:int = 0
    q248_count:int = 1
    num_qr:int = 0

    code_list = None

    code_list_list, Code_list = create_model("Code_list", {"code_num":int, "img_name":str, "code_str":str, "code_type":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal code_list_list, encodedtext, dataqr, pathqr, dirqr, msg_result, initial_date, int_date, int_time, outlet_number, count_i, curr_zeit, time_j, q248_count, num_qr


        nonlocal code_list
        nonlocal code_list_list
        return {"code-list": code_list_list}


    int_time = 0
    initial_date = 01/01/2022
    int_date = get_current_date() - initial_date
    dirqr = "C:\\e1_vhp\\Zint\\BarcodeData"
    q248_count, msg_result = get_output(qrcode_generatorbl(1, code_list))

    if q248_count != 1:
        num_qr = (q248_count + num_of_qr) - 1
    else:
        num_qr = num_of_qr
    for count_i in range(q248_count,num_qr + 1) :
        int_time = get_current_time_in_seconds() + count_i
        encodedtext = to_string(licensenr) + to_string(int_date, "9999") + to_string(int_time, "99999")
        dataqr = encodedtext
        pathqr = dirqr + "\\NSCashless" + to_string(count_i, "999") + ".png"
        code_list = Code_list()
        code_list_list.append(code_list)

        code_list.code_num = count_i
        code_list.code_type = type_code
        code_list.img_name = pathqr
        code_list.code_str = dataqr

    return generate_output()