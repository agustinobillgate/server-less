#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.prepare_ns_invbl import prepare_ns_invbl
from functions.read_artikel1bl import read_artikel1bl
from models import Bill, Guest, Artikel, Htparam, Brief

def mb_web_main_logicbl(bil_flag:int, curr_department:int):

    prepare_cache ([Htparam])

    cashdrw_prog = ""
    combo_pf_file1 = ""
    combo_pf_file2 = ""
    combo_gastnr = 0
    combo_ledger = 0
    foreign_rate = False
    double_currency = False
    curr_local = ""
    curr_foreign = ""
    exchg_rate = 1
    price_decimal = 0
    ba_dept = -1
    gname = ""
    golf_license = False
    mc_flag = False
    pos1 = 0
    pos2 = 0
    lvanzvat = 0
    cash_refund_str = ""
    rebate_str = ""
    b1_title = ""
    vat_artlist = [0, 0, 0, 0]
    r_zahlungsart = 0
    tel_rechnr = 0
    param146 = False
    param199 = False
    param219 = False
    param60 = 0
    param145 = 0
    param497 = 0
    artlist_list = []
    lvint1:int = 0
    bill = guest = artikel = htparam = brief = None

    f_foinv = t_bill = t_guest = artlist = None

    f_foinv_list, F_foinv = create_model("F_foinv", {"price_decimal":int, "briefnr2314":int, "param60":int, "param145":int, "param487":int, "tel_rechnr":int, "pos1":int, "pos2":int, "ba_dept":int, "exchg_rate":Decimal, "max_price":Decimal, "param132":string, "ext_char":string, "curr_local":string, "curr_foreign":string, "b_title":string, "gname":string, "param219":bool, "double_currency":bool, "foreign_rate":bool, "banquet_flag":bool, "mc_flag":bool}, {"ba_dept": -1})
    t_bill_list, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    artlist_list, Artlist = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashdrw_prog, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger, foreign_rate, double_currency, curr_local, curr_foreign, exchg_rate, price_decimal, ba_dept, gname, golf_license, mc_flag, pos1, pos2, lvanzvat, cash_refund_str, rebate_str, b1_title, vat_artlist, r_zahlungsart, tel_rechnr, param146, param199, param219, param60, param145, param497, artlist_list, lvint1, bill, guest, artikel, htparam, brief
        nonlocal bil_flag, curr_department


        nonlocal f_foinv, t_bill, t_guest, artlist
        nonlocal f_foinv_list, t_bill_list, t_guest_list, artlist_list

        return {"cashdrw_prog": cashdrw_prog, "combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "combo_gastnr": combo_gastnr, "combo_ledger": combo_ledger, "foreign_rate": foreign_rate, "double_currency": double_currency, "curr_local": curr_local, "curr_foreign": curr_foreign, "exchg_rate": exchg_rate, "price_decimal": price_decimal, "ba_dept": ba_dept, "gname": gname, "golf_license": golf_license, "mc_flag": mc_flag, "pos1": pos1, "pos2": pos2, "lvanzvat": lvanzvat, "cash_refund_str": cash_refund_str, "rebate_str": rebate_str, "b1_title": b1_title, "vat_artlist": vat_artlist, "r_zahlungsart": r_zahlungsart, "tel_rechnr": tel_rechnr, "param146": param146, "param199": param199, "param219": param219, "param60": param60, "param145": param145, "param497": param497, "artlist": artlist_list}

    cashdrw_prog = get_output(htpchar(870))
    param146 = get_output(htplogic(146))
    param199 = get_output(htplogic(199))
    param219 = get_output(htplogic(219))
    param60 = get_output(htpint(60))
    param145 = get_output(htpint(145))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 497)]})

    if htparam.finteger > 0:

        brief = get_cache (Brief, {"briefnr": [(eq, htparam.finteger)]})

        if brief:
            param497 = htparam.finteger
    f_foinv_list, t_bill_list, t_guest_list, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger = get_output(prepare_ns_invbl(0, curr_department, combo_pf_file1, combo_pf_file2, combo_gastnr, combo_ledger))

    f_foinv = query(f_foinv_list, first=True)

    t_bill = query(t_bill_list, first=True)

    t_guest = query(t_guest_list, first=True)
    price_decimal = f_foinv.price_decimal
    double_currency = f_foinv.double_currency
    ext_char = entry(0, f_foinv.ext_char, ";")
    foreign_rate = f_foinv.foreign_rate
    exchg_rate =  to_decimal(f_foinv.exchg_rate)
    pos1 = f_foinv.pos1
    pos2 = f_foinv.pos2
    mc_flag = f_foinv.mc_flag
    ba_dept = f_foinv.ba_dept
    curr_local = f_foinv.curr_local
    curr_foreign = f_foinv.curr_foreign
    golf_license = (entry(0, f_foinv.gname, chr_unicode(2)) == "YES")
    gname = entry(1, f_foinv.gname, chr_unicode(2))
    tel_rechnr = f_foinv.tel_rechnr

    if exchg_rate == 0:
        exchg_rate =  to_decimal("1")

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