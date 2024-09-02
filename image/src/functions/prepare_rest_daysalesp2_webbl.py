from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_rest_daysalesp2_1_cldbl import prepare_rest_daysalesp2_1_cldbl
from functions.rest_daysalesp2_check_dynacol_cldbl import rest_daysalesp2_check_dynacol_cldbl
from models import Kellner

def prepare_rest_daysalesp2_webbl():
    errcode = ""
    curr_local = None
    price_decimal = None
    bezeich = None
    show_option = False
    oth_flag = False
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    exchg_rate = None
    str = None
    curr_foreign = None
    serv_taxable = None
    dpt_str = ""
    art_str = ""
    oth_str = ""
    anzahl = None
    curr_dept = None
    dept_name = None
    voucher_art = 0
    use_voucher = False
    from_date = None
    to_date = None
    htl_dept_dptnr = 0
    err_flag = 0
    p_110 = None
    p_240 = False
    active_deposit = False
    buf_art_list = []
    htl_dept_list = []
    usr1_list = []
    artnr_list:int = 0
    i:int = 0
    kellner = None

    buf_art = htl_dept = usr1 = other_art = None

    buf_art_list, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":str, "departement":int})
    htl_dept_list, Htl_dept = create_model("Htl_dept", {"dptnr":int, "bezeich":str})
    usr1_list, Usr1 = create_model_like(Kellner, {"rec_id":int})
    other_art_list, Other_art = create_model("Other_art", {"artnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal errcode, curr_local, price_decimal, bezeich, show_option, oth_flag, disc_art1, disc_art2, disc_art3, exchg_rate, str, curr_foreign, serv_taxable, dpt_str, art_str, oth_str, anzahl, curr_dept, dept_name, voucher_art, use_voucher, from_date, to_date, htl_dept_dptnr, err_flag, p_110, p_240, active_deposit, buf_art_list, htl_dept_list, usr1_list, artnr_list, i, kellner


        nonlocal buf_art, htl_dept, usr1, other_art
        nonlocal buf_art_list, htl_dept_list, usr1_list, other_art_list
        return {"errcode": errcode, "curr_local": curr_local, "price_decimal": price_decimal, "bezeich": bezeich, "show_option": show_option, "oth_flag": oth_flag, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "exchg_rate": exchg_rate, "str": str, "curr_foreign": curr_foreign, "serv_taxable": serv_taxable, "dpt_str": dpt_str, "art_str": art_str, "oth_str": oth_str, "anzahl": anzahl, "curr_dept": curr_dept, "dept_name": dept_name, "voucher_art": voucher_art, "use_voucher": use_voucher, "from_date": from_date, "to_date": to_date, "htl_dept_dptnr": htl_dept_dptnr, "err_flag": err_flag, "p_110": p_110, "p_240": p_240, "active_deposit": active_deposit, "buf-art": buf_art_list, "htl-dept": htl_dept_list, "usr1": usr1_list}

    disc_art1, disc_art2, disc_art3, exchg_rate, str, curr_foreign, serv_taxable, dpt_str, art_str, oth_str, anzahl, curr_dept, dept_name, voucher_art, use_voucher, from_date, to_date, htl_dept_dptnr, err_flag, p_110, p_240, active_deposit, buf_art_list, htl_dept_list, usr1_list = get_output(prepare_rest_daysalesp2_1_cldbl())

    if num_entries(str, ";") > 1:
        curr_local = entry(0, str, ";")
        price_decimal = to_int(entry(1, str, ";"))


    else:
        curr_local = str

    if err_flag == 1:
        errcode = to_string(err_flag) + " - Parameter no 732 not yet been setup."

        return generate_output()

    if err_flag == 2:
        errcode = to_string(err_flag) + " - Department not yet been setup in param 716."

        return generate_output()
    anzahl, artnr_list, bezeich, show_option = get_output(rest_daysalesp2_check_dynacol_cldbl(buf_art, art_str, htl_dept_dptnr))

    if oth_str != "":
        bezeich[20] = entry(0, oth_str, ",")
        for i in range(2,num_entries(oth_str, ",")  + 1) :

            if i > 11:
                1
            else:
                other_art = Other_art()
                other_art_list.append(other_art)

                other_art.artnr = to_int(entry(i - 1, oth_str, ","))

        if entry(1, oth_str, ",") != "":
            oth_flag = True
    errcode = "0 - Retrieve data Success."

    return generate_output()