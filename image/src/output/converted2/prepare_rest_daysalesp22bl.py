#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_rest_daysalesp2bl import prepare_rest_daysalesp2bl
from models import Kellner

def prepare_rest_daysalesp22bl():
    errcode = ""
    curr_local = ""
    price_decimal = 0
    bezeich = ["", "", "", "", "", "", "", "", "", "", ""]
    show_option = False
    oth_flag = False
    disc_art1 = -1
    disc_art2 = -1
    disc_art3 = -1
    exchg_rate = to_decimal("0.0")
    str = ""
    curr_foreign = ""
    serv_taxable = False
    dpt_str = ""
    art_str = ""
    oth_str = ""
    anzahl = 0
    curr_dept = 0
    dept_name = ""
    voucher_art = 0
    use_voucher = True
    from_date = None
    to_date = None
    htl_dept_dptnr = 0
    err_flag = 0
    p_110 = None
    p_240 = False
    buf_art_list = []
    htl_dept_list = []
    usr1_list = []
    artnr_list:List[int] = create_empty_list(10,0)
    i:int = 0
    kellner = None

    buf_art = htl_dept = usr1 = None

    buf_art_list, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":string, "departement":int})
    htl_dept_list, Htl_dept = create_model("Htl_dept", {"dptnr":int, "bezeich":string})
    usr1_list, Usr1 = create_model_like(Kellner, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal errcode, curr_local, price_decimal, bezeich, show_option, oth_flag, disc_art1, disc_art2, disc_art3, exchg_rate, str, curr_foreign, serv_taxable, dpt_str, art_str, oth_str, anzahl, curr_dept, dept_name, voucher_art, use_voucher, from_date, to_date, htl_dept_dptnr, err_flag, p_110, p_240, buf_art_list, htl_dept_list, usr1_list, artnr_list, i, kellner


        nonlocal buf_art, htl_dept, usr1
        nonlocal buf_art_list, htl_dept_list, usr1_list

        return {"errcode": errcode, "curr_local": curr_local, "price_decimal": price_decimal, "bezeich": bezeich, "show_option": show_option, "oth_flag": oth_flag, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "exchg_rate": exchg_rate, "str": str, "curr_foreign": curr_foreign, "serv_taxable": serv_taxable, "dpt_str": dpt_str, "art_str": art_str, "oth_str": oth_str, "anzahl": anzahl, "curr_dept": curr_dept, "dept_name": dept_name, "voucher_art": voucher_art, "use_voucher": use_voucher, "from_date": from_date, "to_date": to_date, "htl_dept_dptnr": htl_dept_dptnr, "err_flag": err_flag, "p_110": p_110, "p_240": p_240, "buf-art": buf_art_list, "htl-dept": htl_dept_list, "usr1": usr1_list}


    disc_art1, disc_art2, disc_art3, exchg_rate, str, curr_foreign, serv_taxable, dpt_str, art_str, oth_str, anzahl, curr_dept, dept_name, voucher_art, use_voucher, from_date, to_date, htl_dept_dptnr, err_flag, p_110, p_240, buf_art_list, htl_dept_list, usr1_list = get_output(prepare_rest_daysalesp2bl())

    if num_entries(str, ";") > 1:
        curr_local = entry(0, str, ";")
        price_decimal = to_int(entry(1, str, ";"))


    else:
        curr_local = str

    if err_flag == 1:
        errcode = to_string(err_flag) + "- Parameter no 732 not yet been setup."

        return generate_output()

    if err_flag == 2:
        errcode = to_string(err_flag) + "- Department not yet been setup in param 716."

        return generate_output()
    errcode = "0 - Retrieve data Success."
    for i in range(1,num_entries(art_str, ",")  + 1) :

        if i > 11:
            pass
        else:
            artnr_list[i - 1] = to_int(entry(i - 1, art_str, ","))

            if artnr_list[i - 1] == disc_art2 or artnr_list[i - 1] == disc_art3:
                show_option = True
    for i in range(1,anzahl + 1) :

        buf_art = query(buf_art_list, filters=(lambda buf_art: buf_art.artnr == artnr_list[i - 1] and buf_art.departement == htl_dept_dptnr), first=True)

        if buf_art:
            bezeich[i - 1] = buf_art.bezeich

    if oth_str != "":
        bezeich[10] = entry(0, oth_str, ",")

        if entry(1, oth_str, ",") != "":
            oth_flag = True

    return generate_output()