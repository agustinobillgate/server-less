from functions.additional_functions import *
import decimal
from datetime import date
from functions.rest_daysalesp2_btn_go_4_cldbl import rest_daysalesp2_btn_go_4_cldbl
from models import Hoteldpt

def rest_daysalesp2_btn_go1_webbl(bline_list:[Bline_list], buf_art:[Buf_art], disc_art1:int, disc_art2:int, disc_art3:int, curr_dept:int, all_user:bool, shift:int, from_date:date, to_date:date, art_str:str, voucher_art:int, zero_vat_compli:bool, show_fbodisc:bool, exclude_compli:bool, incl_move_table:bool):
    errcode = ""
    t_betrag = 0
    t_foreign = 0
    exchg_rate = 0
    tot_serv = None
    tot_tax = None
    tot_debit = None
    tot_cash = None
    tot_cash1 = None
    tot_trans = None
    tot_ledger = None
    tot_cover = None
    nt_cover = None
    tot_other = 0
    nt_other = 0
    nt_serv = None
    nt_tax = None
    nt_debit = None
    nt_cash = None
    nt_cash1 = None
    nt_trans = None
    nt_ledger = None
    tot_vat = None
    nt_vat = None
    avail_outstand_list = False
    turnover_list = []
    t_tot_betrag_list = []
    t_nt_betrag_list = []
    outstand_list_list = []
    pay_list_list = []
    summ_list_list = []
    hoteldpt = None

    bline_list = outstand_list = pay_list = turnover = t_tot_betrag = t_nt_betrag = buf_art = summ_list = None

    bline_list_list, Bline_list = create_model("Bline_list")
    outstand_list_list, Outstand_list = create_model("Outstand_list")
    pay_list_list, Pay_list = create_model("Pay_list")
    turnover_list, Turnover = create_model("Turnover", {"betrag":[decimal, 20], "other":decimal, "compli":bool, "flag":int, "gname":str, "int_rechnr":int, "st_comp":int, "p_curr":str, "t_vat":decimal, "qty_fpax":int, "qty_bpax":int, "qty_opax":int, "rest_deposit":decimal})
    t_tot_betrag_list, T_tot_betrag = create_model("T_tot_betrag", {"tot_betrag1":decimal, "tot_betrag2":decimal, "tot_betrag3":decimal, "tot_betrag4":decimal, "tot_betrag5":decimal, "tot_betrag6":decimal, "tot_betrag7":decimal, "tot_betrag8":decimal, "tot_betrag9":decimal, "tot_betrag10":decimal, "tot_betrag11":decimal, "tot_betrag12":decimal, "tot_betrag13":decimal, "tot_betrag14":decimal, "tot_betrag15":decimal, "tot_betrag16":decimal, "tot_betrag17":decimal, "tot_betrag18":decimal, "tot_betrag19":decimal, "tot_betrag20":decimal})
    t_nt_betrag_list, T_nt_betrag = create_model("T_nt_betrag", {"nt_betrag1":decimal, "nt_betrag2":decimal, "nt_betrag3":decimal, "nt_betrag4":decimal, "nt_betrag5":decimal, "nt_betrag6":decimal, "nt_betrag7":decimal, "nt_betrag8":decimal, "nt_betrag":decimal, "nt_betrag10":decimal, "nt_betrag11":decimal, "nt_betrag12":decimal, "nt_betrag13":decimal, "nt_betrag14":decimal, "nt_betrag15":decimal, "nt_betrag16":decimal, "nt_betrag17":decimal, "nt_betrag18":decimal, "nt_betrag19":decimal, "nt_betrag20":decimal})
    buf_art_list, Buf_art = create_model("Buf_art", {"artnr":int, "bezeich":str, "departement":int})
    summ_list_list, Summ_list = create_model("Summ_list", {"amount_food":decimal, "amount_bev":decimal, "amount_other":decimal, "disc_food":decimal, "disc_bev":decimal, "disc_other":decimal, "qty_disc_food":int, "qty_disc_bev":int, "qty_disc_other":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal errcode, t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list, hoteldpt


        nonlocal bline_list, outstand_list, pay_list, turnover, t_tot_betrag, t_nt_betrag, buf_art, summ_list
        nonlocal bline_list_list, outstand_list_list, pay_list_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, buf_art_list, summ_list_list
        return {"errcode": errcode, "t_betrag": t_betrag, "t_foreign": t_foreign, "exchg_rate": exchg_rate, "tot_serv": tot_serv, "tot_tax": tot_tax, "tot_debit": tot_debit, "tot_cash": tot_cash, "tot_cash1": tot_cash1, "tot_trans": tot_trans, "tot_ledger": tot_ledger, "tot_cover": tot_cover, "nt_cover": nt_cover, "tot_other": tot_other, "nt_other": nt_other, "nt_serv": nt_serv, "nt_tax": nt_tax, "nt_debit": nt_debit, "nt_cash": nt_cash, "nt_cash1": nt_cash1, "nt_trans": nt_trans, "nt_ledger": nt_ledger, "tot_vat": tot_vat, "nt_vat": nt_vat, "avail_outstand_list": avail_outstand_list, "turnover": turnover_list, "t-tot-betrag": t_tot_betrag_list, "t-nt-betrag": t_nt_betrag_list, "outstand-list": outstand_list_list, "pay-list": pay_list_list, "summ-list": summ_list_list}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    if not hoteldpt:
        errcode = "1 - Wrong department"

        return generate_output()

    bline_list = query(bline_list_list, first=True)

    if bline_list:
        turnover_list.clear()
        t_betrag, t_foreign, exchg_rate, tot_serv, tot_tax, tot_debit, tot_cash, tot_cash1, tot_trans, tot_ledger, tot_cover, nt_cover, tot_other, nt_other, nt_serv, nt_tax, nt_debit, nt_cash, nt_cash1, nt_trans, nt_ledger, tot_vat, nt_vat, avail_outstand_list, turnover_list, t_tot_betrag_list, t_nt_betrag_list, outstand_list_list, pay_list_list, summ_list_list = get_output(rest_daysalesp2_btn_go_4_cldbl(bline_list, buf_art, disc_art1, disc_art2, disc_art3, curr_dept, all_user, shift, from_date, to_date, art_str, voucher_art, zero_vat_compli, show_fbodisc, curr_dept, incl_move_table))

        if exclude_compli:

            for turnover in query(turnover_list, filters=(lambda turnover :turnover.compli)):
                turnover_list.remove(turnover)
        errcode = "0 - Retrieve Data Success"
    else:
        errcode = "2 - Please select at least a user."

        return generate_output()