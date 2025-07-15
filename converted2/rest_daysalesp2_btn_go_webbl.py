#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.rest_daysalesp2_btn_go_3_cldbl import rest_daysalesp2_btn_go_3_cldbl
from models import Hoteldpt

bline_list_data, Bline_list = create_model("Bline_list", {"selected":bool, "depart":string, "dept":int, "knr":int, "bl_recid":int}, {"selected": True})
buf_art_data, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":string, "departement":int})

def rest_daysalesp2_btn_go_webbl(bline_list_data:[Bline_list], buf_art_data:[Buf_art], disc_art1:int, disc_art2:int, disc_art3:int, curr_dept:int, all_user:bool, shift:int, from_date:date, to_date:date, art_str:string, voucher_art:int, zero_vat_compli:bool, show_fbodisc:bool, exclude_compli:bool):
    errcode = ""
    t_betrag = to_decimal("0.0")
    t_foreign = to_decimal("0.0")
    exchg_rate = to_decimal("0.0")
    tot_serv = to_decimal("0.0")
    tot_tax = to_decimal("0.0")
    tot_debit = to_decimal("0.0")
    tot_cash = to_decimal("0.0")
    tot_cash1 = to_decimal("0.0")
    tot_trans = to_decimal("0.0")
    tot_ledger = to_decimal("0.0")
    tot_cover = 0
    nt_cover = 0
    tot_other = to_decimal("0.0")
    nt_other = to_decimal("0.0")
    nt_serv = to_decimal("0.0")
    nt_tax = to_decimal("0.0")
    nt_debit = to_decimal("0.0")
    nt_cash = to_decimal("0.0")
    nt_cash1 = to_decimal("0.0")
    nt_trans = to_decimal("0.0")
    nt_ledger = to_decimal("0.0")
    tot_vat = to_decimal("0.0")
    nt_vat = to_decimal("0.0")
    avail_outstand_list = False
    turnover_data = []
    t_tot_betrag_data = []
    t_nt_betrag_data = []
    outstand_list_data = []
    pay_list_data = []
    summ_list_data = []
    hoteldpt = None

    bline_list = outstand_list = pay_list = turnover = t_tot_betrag = t_nt_betrag = buf_art = summ_list = None

    outstand_list_data, Outstand_list = create_model("Outstand_list", {"name":string, "rechnr":int, "foreign":Decimal, "saldo":Decimal})
    pay_list_data, Pay_list = create_model("Pay_list", {"compli":bool, "person":int, "flag":int, "bezeich":string, "artnr":int, "rechnr":int, "foreign":Decimal, "saldo":Decimal}, {"compli": False})
    turnover_data, Turnover = create_model("Turnover", {"departement":int, "kellner_nr":int, "name":string, "tischnr":int, "rechnr":string, "belegung":int, "artnr":int, "info":string, "betrag":[Decimal,20], "other":Decimal, "t_service":Decimal, "t_tax":Decimal, "t_debit":Decimal, "t_credit":Decimal, "p_cash":Decimal, "p_cash1":Decimal, "r_transfer":Decimal, "c_ledger":Decimal, "compli":bool, "flag":int, "gname":string, "int_rechnr":int, "st_comp":int, "p_curr":string, "t_vat":Decimal, "qty_fpax":int, "qty_bpax":int, "qty_opax":int, "rest_deposit":Decimal})
    t_tot_betrag_data, T_tot_betrag = create_model("T_tot_betrag", {"tot_betrag1":Decimal, "tot_betrag2":Decimal, "tot_betrag3":Decimal, "tot_betrag4":Decimal, "tot_betrag5":Decimal, "tot_betrag6":Decimal, "tot_betrag7":Decimal, "tot_betrag8":Decimal, "tot_betrag9":Decimal, "tot_betrag10":Decimal, "tot_betrag11":Decimal, "tot_betrag12":Decimal, "tot_betrag13":Decimal, "tot_betrag14":Decimal, "tot_betrag15":Decimal, "tot_betrag16":Decimal, "tot_betrag17":Decimal, "tot_betrag18":Decimal, "tot_betrag19":Decimal, "tot_betrag20":Decimal})
    t_nt_betrag_data, T_nt_betrag = create_model("T_nt_betrag", {"nt_betrag1":Decimal, "nt_betrag2":Decimal, "nt_betrag3":Decimal, "nt_betrag4":Decimal, "nt_betrag5":Decimal, "nt_betrag6":Decimal, "nt_betrag7":Decimal, "nt_betrag8":Decimal, "nt_betrag":Decimal, "nt_betrag10":Decimal, "nt_betrag11":Decimal, "nt_betrag12":Decimal, "nt_betrag13":Decimal, "nt_betrag14":Decimal, "nt_betrag15":Decimal, "nt_betrag16":Decimal, "nt_betrag17":Decimal, "nt_betrag18":Decimal, "nt_betrag19":Decimal, "nt_betrag20":Decimal})
    summ_list_data, Summ_list = create_model("Summ_list", {"amount_food":Decimal, "amount_bev":Decimal, "amount_other":Decimal, "disc_food":Decimal, "disc_bev":Decimal, "disc_other":Decimal, "qty_disc_food":int, "qty_disc_bev":int, "qty_disc_other":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal errcode, t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data, hoteldpt
        nonlocal disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, exclude_compli


        nonlocal bline_list, outstand_list, pay_list, turnover, t_tot_betrag, t_nt_betrag, buf_art, summ_list
        nonlocal outstand_list_data, pay_list_data, turnover_data, t_tot_betrag_data, t_nt_betrag_data, summ_list_data

        return {"errcode": errcode, "t_betrag": t_betrag, "t_foreign": t_foreign, "exchg_rate": exchg_rate, "tot_serv": tot_serv, "tot_tax": tot_tax, "tot_debit": tot_debit, "tot_cash": tot_cash, "tot_cash1": tot_cash1, "tot_trans": tot_trans, "tot_ledger": tot_ledger, "tot_cover": tot_cover, "nt_cover": nt_cover, "tot_other": tot_other, "nt_other": nt_other, "nt_serv": nt_serv, "nt_tax": nt_tax, "nt_debit": nt_debit, "nt_cash": nt_cash, "nt_cash1": nt_cash1, "nt_trans": nt_trans, "nt_ledger": nt_ledger, "tot_vat": tot_vat, "nt_vat": nt_vat, "avail_outstand_list": avail_outstand_list, "turnover": turnover_data, "t-tot-betrag": t_tot_betrag_data, "t-nt-betrag": t_nt_betrag_data, "outstand-list": outstand_list_data, "pay-list": pay_list_data, "summ-list": summ_list_data}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if not hoteldpt:
        errcode = "1 - Wrong department"

        return generate_output()

    bline_list = query(bline_list_data, first=True)

    if bline_list:
        turnover_data.clear()
        t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_data, t_tot_betrag_data, t_nt_betrag_data, outstand_list_data, pay_list_data, summ_list_data = get_output(rest_daysalesp2_btn_go_3_cldbl(bline_list_data, buf_art_data, disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, curr_dept))

        if exclude_compli:

            for turnover in query(turnover_data, filters=(lambda turnover: turnover.compli)):
                turnover_data.remove(turnover)
        errcode = "0 - Retrieve Data Success"
    else:
        errcode = "2 - Please select at least a user."

        return generate_output()

    return generate_output()