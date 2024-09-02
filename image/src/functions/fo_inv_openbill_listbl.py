from functions.additional_functions import *
import decimal
from datetime import date
from functions.fo_invoice_open_billbl import fo_invoice_open_billbl
from functions.fo_invoice_fill_rescommentbl import fo_invoice_fill_rescommentbl
from functions.fo_invoice_disp_totbalancebl import fo_invoice_disp_totbalancebl
from functions.fo_invoice_disp_bill_linebl import fo_invoice_disp_bill_linebl
from models import Bill, Res_line, Bill_line

def fo_inv_openbill_listbl(bil_flag:int, bil_recid:int, room:str, vipflag:bool, fill_co:bool, double_currency:bool, foreign_rate:bool):
    abreise = None
    resname = ""
    res_exrate = 0
    zimmer_bezeich = ""
    kreditlimit = 0
    master_str = ""
    master_rechnr = ""
    bill_anzahl = 0
    queasy_char1 = ""
    disp_warning = False
    flag_report = False
    rescomment = ""
    printed = ""
    rechnr = 0
    rmrate = 0
    balance = 0
    balance_foreign = 0
    tot_balance = 0
    t_res_line_list = []
    t_bill_list = []
    spbill_list_list = []
    t_bill_line_list = []
    bill = res_line = bill_line = None

    t_bill = t_res_line = spbill_list = t_bill_line = None

    t_bill_list, T_bill = create_model_like(Bill)
    t_res_line_list, T_res_line = create_model_like(Res_line)
    spbill_list_list, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_list, T_bill_line = create_model_like(Bill_line, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, t_res_line_list, t_bill_list, spbill_list_list, t_bill_line_list, bill, res_line, bill_line


        nonlocal t_bill, t_res_line, spbill_list, t_bill_line
        nonlocal t_bill_list, t_res_line_list, spbill_list_list, t_bill_line_list
        return {"abreise": abreise, "resname": resname, "res_exrate": res_exrate, "zimmer_bezeich": zimmer_bezeich, "kreditlimit": kreditlimit, "master_str": master_str, "master_rechnr": master_rechnr, "bill_anzahl": bill_anzahl, "queasy_char1": queasy_char1, "disp_warning": disp_warning, "flag_report": flag_report, "rescomment": rescomment, "printed": printed, "rechnr": rechnr, "rmrate": rmrate, "balance": balance, "balance_foreign": balance_foreign, "tot_balance": tot_balance, "t-res-line": t_res_line_list, "t-bill": t_bill_list, "spbill-list": spbill_list_list, "t-bill-line": t_bill_line_list}

    def disp_bill_line():

        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, t_res_line_list, t_bill_list, spbill_list_list, t_bill_line_list, bill, res_line, bill_line


        nonlocal t_bill, t_res_line, spbill_list, t_bill_line
        nonlocal t_bill_list, t_res_line_list, spbill_list_list, t_bill_line_list


        t_bill_line_list, spbill_list_list = get_output(fo_invoice_disp_bill_linebl(bil_recid, double_currency))

    abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, t_res_line_list, t_bill_list = get_output(fo_invoice_open_billbl(bil_flag, bil_recid, room, vipflag))

    t_bill = query(t_bill_list, first=True)

    t_res_line = query(t_res_line_list, first=True)
    rescomment = get_output(fo_invoice_fill_rescommentbl(bil_recid, fill_co))

    if t_bill.rgdruck == 0:
        printed = ""
    else:
        printed = "*"
    rechnr = t_bill.rechnr
    rmrate = 0

    if t_res_line:
        rmrate = t_res_line.zipreis
    balance = t_bill.saldo

    if double_currency or foreign_rate:
        balance_foreign = t_bill.mwst[98]

    if bil_flag == 0:
        tot_balance = 0

        if t_bill.parent_nr == 0:
            tot_balance = t_bill.saldo
        else:
            tot_balance = get_output(fo_invoice_disp_totbalancebl(bil_recid))
    spbill_list_list.clear()
    disp_bill_line()

    return generate_output()