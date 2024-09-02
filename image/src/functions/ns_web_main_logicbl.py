from functions.additional_functions import *
import decimal
from functions.htpchar import htpchar
from functions.prepare_ns_invbl import prepare_ns_invbl
from functions.read_artikel1bl import read_artikel1bl
from models import Bill, Guest, Artikel

def ns_web_main_logicbl(bil_flag:int, curr_department:int):
    cashdrw_prog = ""
    combo_pf_file1 = ""
    combo_pf_file2 = ""
    combo_gastnr = 0
    combo_ledger = 0
    foreign_rate = False
    double_currency = False
    curr_local = ""
    curr_foreign = ""
    exchg_rate = 0
    price_decimal = 0
    ba_dept = 0
    gname = ""
    golf_license = False
    mc_flag = False
    pos1 = 0
    pos2 = 0
    lvanzvat = 0
    cash_refund_str = ""
    rebate_str = ""
    b1_title = ""
    vat_artlist = 0
    r_zahlungsart = 0
    tel_rechnr = 0
    artlist_list = []
    lvint1:int = 0
    bill = guest = artikel = None

    f_foinv = t_bill = t_guest = artlist = None

    f_foinv_list, F_foinv = create_model("F_foinv", {"price_decimal":int, "briefnr2314":int, "param60":int, "param145":int, "param487":int, "tel_rechnr":int, "pos1":int, "pos2":int, "ba_dept":int, "exchg_rate":decimal, "max_price":decimal, "param132":str, "ext_char":str, "curr_local":str, "curr_foreign":str, "b_title":str, "gname":str, "param219":bool, "double_currency":bool, "foreign_rate":bool, "banquet_flag":bool, "mc_flag":bool}, {"ba_dept": -1})
    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    artlist_list, Artlist = create_model_like(Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashdrw_prog, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger, foreign_rate, double_currency, curr_local, curr_foreign, exchg_rate, price_decimal, ba_dept, gname, golf_license, mc_flag, pos1, pos2, lvanzvat, cash_refund_str, rebate_str, b1_title, vat_artlist, r_zahlungsart, tel_rechnr, artlist_list, lvint1, bill, guest, artikel


        nonlocal f_foinv, t_bill, t_guest, artlist
        nonlocal f_foinv_list, t_bill_list, t_guest_list, artlist_list
        return {"cashdrw_prog": cashdrw_prog, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger, "foreign_rate": foreign_rate, "double_currency": double_currency, "curr_local": curr_local, "curr_foreign": curr_foreign, "exchg_rate": exchg_rate, "price_decimal": price_decimal, "ba_dept": ba_dept, "gname": gname, "golf_license": golf_license, "mc_flag": mc_flag, "pos1": pos1, "pos2": pos2, "lvanzvat": lvanzvat, "cash_refund_str": cash_refund_str, "rebate_str": rebate_str, "b1_title": b1_title, "vat_artlist": vat_artlist, "r_zahlungsart": r_zahlungsart, "tel_rechnr": tel_rechnr, "artlist": artlist_list}

    cashdrw_prog = get_output(htpchar(870))
    f_foinv_list, t_bill_list, t_guest_list, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger = get_output(prepare_ns_invbl(0, curr_department, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger))

    f_foinv = query(f_foinv_list, first=True)

    t_bill = query(t_bill_list, first=True)

    t_guest = query(t_guest_list, first=True)
    price_decimal = f_foinv.price_decimal
    double_currency = f_foinv.double_currency
    ext_char = entry(0, f_foinv.ext_char, ";")
    foreign_rate = f_foinv.foreign_rate
    exchg_rate = f_foinv.exchg_rate
    pos1 = f_foinv.pos1
    pos2 = f_foinv.pos2
    mc_flag = f_foinv.mc_flag
    ba_dept = f_foinv.ba_dept
    curr_local = f_foinv.curr_local
    curr_foreign = f_foinv.curr_foreign
    golf_license = (entry(0, f_foinv.gname, chr(2)) == ("YES").lower())
    gname = entry(1, f_foinv.gname, chr(2))
    tel_rechnr = f_foinv.tel_rechnr

    if exchg_rate == 0:
        exchg_rate = 1

    if num_entries(f_foinv.ext_char, ";") > 1:
        cash_refund_str = "," + entry(1, f_foinv.ext_char, ";") + ","
        rebate_str = "," + entry(2, f_foinv.ext_char, ";") + ","
        cash_refund_str = replace_str(cash_refund_str, " ", "")
        rebate_str = replace_str(rebate_str, " ", "")
        rebate_str = replace_str(rebate_str, ";", "")


    lvanzvat = 0

    if f_foinv.param132 != "":
        for lvint1 in range(1,num_entries(f_foinv.param132, ";")  + 1) :

            if to_int(entry(lvint1 - 1, f_foinv.param132, ";")) != 0:
                lvanzvat = lvanzvat + 1
                vat_artlist[lvanzvat - 1] = to_int(entry(lvint1 - 1, f_foinv.param132, ";"))

    if bil_flag == 0:
        b1_title = "DEPT " + f_foinv.b_title

    elif bil_flag == 1:
        b1_title = "CLOSED BILLS - DEPT " + f_foinv.b_title
    artlist_list = get_output(read_artikel1bl(25, None, curr_department, None, None, None, True))

    return generate_output()