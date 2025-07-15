#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.prepare_fo_invoicebl import prepare_fo_invoicebl

def prepare_fo_invbl(bil_flag:int):
    vipnr1 = 0
    vipnr2 = 0
    vipnr3 = 0
    vipnr4 = 0
    vipnr5 = 0
    vipnr6 = 0
    vipnr7 = 0
    vipnr8 = 0
    vipnr9 = 0
    ext_char = ""
    price_decimal = 0
    double_currency = False
    change_date = False
    foreign_rate = False
    exchg_rate = 1
    curr_local = ""
    curr_foreign = ""
    lvanzvat = 0
    b_title = ""
    artikel_str = ""
    p_219 = False
    p_199 = False
    p_145 = 0
    p_242 = 0
    p_60 = 0
    p_251 = False
    p_2313 = 0
    p_1116 = 0
    p_685 = 0
    avail_brief685 = False
    p_173 = ""
    p_2314 = 0
    p_83 = False
    p_497 = 0
    p_120 = 0
    avail_brief497 = False
    p_1086 = to_decimal("0.0")
    cash_refund_str = ""
    rebate_str = ""
    t_artikel_data = []

    t_artikel = t_foinv = None

    t_artikel_data, T_artikel = create_model("T_artikel", {"artnr":int, "bezeich":string, "epreis":Decimal, "departement":int, "artart":int, "activeflag":bool, "artgrp":int, "bezaendern":bool, "autosaldo":bool, "pricetab":bool, "betriebsnr":int, "resart":bool, "zwkum":int})
    t_foinv_data, T_foinv = create_model("T_foinv", {"vipnr1":int, "vipnr2":int, "vipnr3":int, "vipnr4":int, "vipnr5":int, "vipnr6":int, "vipnr7":int, "vipnr8":int, "vipnr9":int, "ext_char":string, "price_decimal":int, "double_currency":bool, "change_date":bool, "foreign_rate":bool, "exchg_rate":Decimal, "curr_local":string, "curr_foreign":string, "lvanzvat":int, "b_title":string, "artikel_str":string, "p_219":bool, "p_199":bool, "p_145":int, "p_242":int, "p_60":int, "p_251":bool, "p_2313":int, "p_1116":int, "p_685":int, "avail_brief685":bool, "p_173":string, "p_2314":int, "p_83":bool, "p_497":int, "p_120":int, "avail_brief497":bool, "p_1086":Decimal}, {"exchg_rate": 1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ext_char, price_decimal, double_currency, change_date, foreign_rate, exchg_rate, curr_local, curr_foreign, lvanzvat, b_title, artikel_str, p_219, p_199, p_145, p_242, p_60, p_251, p_2313, p_1116, p_685, avail_brief685, p_173, p_2314, p_83, p_497, p_120, avail_brief497, p_1086, cash_refund_str, rebate_str, t_artikel_data
        nonlocal bil_flag


        nonlocal t_artikel, t_foinv
        nonlocal t_artikel_data, t_foinv_data

        return {"vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9, "ext_char": ext_char, "price_decimal": price_decimal, "double_currency": double_currency, "change_date": change_date, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "lvanzvat": lvanzvat, "b_title": b_title, "artikel_str": artikel_str, "p_219": p_219, "p_199": p_199, "p_145": p_145, "p_242": p_242, "p_60": p_60, "p_251": p_251, "p_2313": p_2313, "p_1116": p_1116, "p_685": p_685, "avail_brief685": avail_brief685, "p_173": p_173, "p_2314": p_2314, "p_83": p_83, "p_497": p_497, "p_120": p_120, "avail_brief497": avail_brief497, "p_1086": p_1086, "cash_refund_str": cash_refund_str, "rebate_str": rebate_str, "t-artikel": t_artikel_data}

    def init_var():

        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, ext_char, price_decimal, double_currency, change_date, foreign_rate, exchg_rate, curr_local, curr_foreign, lvanzvat, b_title, artikel_str, p_219, p_199, p_145, p_242, p_60, p_251, p_2313, p_1116, p_685, avail_brief685, p_173, p_2314, p_83, p_497, p_120, avail_brief497, p_1086, cash_refund_str, rebate_str, t_artikel_data
        nonlocal bil_flag


        nonlocal t_artikel, t_foinv
        nonlocal t_artikel_data, t_foinv_data

        t_foinv = query(t_foinv_data, first=True)
        vipnr1 = t_foinv.vipnr1
        vipnr2 = t_foinv.vipnr2
        vipnr3 = t_foinv.vipnr3
        vipnr4 = t_foinv.vipnr4
        vipnr5 = t_foinv.vipnr5
        vipnr6 = t_foinv.vipnr6
        vipnr7 = t_foinv.vipnr7
        vipnr8 = t_foinv.vipnr8
        vipnr9 = t_foinv.vipnr9
        ext_char = entry(0, t_foinv.ext_char, ";")
        price_decimal = t_foinv.price_decimal
        double_currency = t_foinv.double_currency
        change_date = t_foinv.change_date
        foreign_rate = t_foinv.foreign_rate
        exchg_rate =  to_decimal(t_foinv.exchg_rate)
        curr_local = t_foinv.curr_local
        curr_foreign = t_foinv.curr_foreign
        lvanzvat = t_foinv.lvanzvat
        b_title = t_foinv.b_title
        artikel_str = t_foinv.artikel_str
        p_219 = t_foinv.p_219
        p_199 = t_foinv.p_199
        p_145 = t_foinv.p_145
        p_242 = t_foinv.p_242
        p_60 = t_foinv.p_60
        p_251 = t_foinv.p_251
        p_2313 = t_foinv.p_2313
        p_1116 = t_foinv.p_1116
        p_685 = t_foinv.p_685
        avail_brief685 = t_foinv.avail_brief685
        p_173 = t_foinv.p_173
        p_2314 = t_foinv.p_2314
        p_83 = t_foinv.p_83
        p_497 = t_foinv.p_497
        p_120 = t_foinv.p_120
        avail_brief497 = t_foinv.avail_brief497
        p_1086 =  to_decimal(t_foinv.p_1086)

        if num_entries(t_foinv.ext_char, ";") > 1:
            cash_refund_str = "," + entry(1, t_foinv.ext_char, ";") + ","
            rebate_str = "," + entry(2, t_foinv.ext_char, ";") + ","
            cash_refund_str = replace_str(cash_refund_str, " ", "")
            rebate_str = replace_str(rebate_str, " ", "")
            rebate_str = replace_str(rebate_str, ";", "")


    t_artikel_data, t_foinv_data = get_output(prepare_fo_invoicebl(bil_flag))
    init_var()

    return generate_output()