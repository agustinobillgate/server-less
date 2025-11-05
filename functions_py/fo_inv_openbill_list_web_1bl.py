#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.fo_invoice_open_bill_cld_2bl import fo_invoice_open_bill_cld_2bl
from functions.fo_invoice_fill_rescommentbl import fo_invoice_fill_rescommentbl
from functions.fo_invoice_disp_totbalancebl import fo_invoice_disp_totbalancebl
from functions.fo_invoice_disp_bill_line_cldbl import fo_invoice_disp_bill_line_cldbl
from models import Bill, Res_line, Bill_line

def fo_inv_openbill_list_web_1bl(bil_flag:int, bil_recid:int, room:string, vipflag:bool, fill_co:bool, double_currency:bool, foreign_rate:bool):
    abreise = None
    resname = ""
    res_exrate = to_decimal("0.0")
    zimmer_bezeich = ""
    kreditlimit = to_decimal("0.0")
    master_str = ""
    master_rechnr = ""
    bill_anzahl = 0
    queasy_char1 = ""
    disp_warning = False
    flag_report = False
    rescomment = ""
    printed = ""
    rechnr = 0
    rmrate = to_decimal("0.0")
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    tot_balance = to_decimal("0.0")
    guest_taxcode = ""
    repeat_charge = False
    t_res_line_data = []
    t_bill_data = []
    spbill_list_data = []
    t_bill_line_data = []
    bill = res_line = bill_line = None

    t_bill = t_res_line = spbill_list = t_bill_line = None

    t_bill_data, T_bill = create_model_like(Bill)
    t_res_line_data, T_res_line = create_model_like(Res_line, {"guest_name":string})
    spbill_list_data, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"rec_id":int, "serv":Decimal, "vat":Decimal, "netto":Decimal, "art_type":int})

    db_session = local_storage.db_session

    room = room.strip()

    def generate_output():
        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, guest_taxcode, repeat_charge, t_res_line_data, t_bill_data, spbill_list_data, t_bill_line_data, bill, res_line, bill_line
        nonlocal bil_flag, bil_recid, room, vipflag, fill_co, double_currency, foreign_rate


        nonlocal t_bill, t_res_line, spbill_list, t_bill_line
        nonlocal t_bill_data, t_res_line_data, spbill_list_data, t_bill_line_data

        return {"abreise": abreise, "resname": resname, "res_exrate": res_exrate, "zimmer_bezeich": zimmer_bezeich, "kreditlimit": kreditlimit, "master_str": master_str, "master_rechnr": master_rechnr, "bill_anzahl": bill_anzahl, "queasy_char1": queasy_char1, "disp_warning": disp_warning, "flag_report": flag_report, "rescomment": rescomment, "printed": printed, "rechnr": rechnr, "rmrate": rmrate, "balance": balance, "balance_foreign": balance_foreign, "tot_balance": tot_balance, "guest_taxcode": guest_taxcode, "repeat_charge": repeat_charge, "t-res-line": t_res_line_data, "t-bill": t_bill_data, "spbill-list": spbill_list_data, "t-bill-line": t_bill_line_data}

    def disp_bill_line():

        nonlocal abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, rescomment, printed, rechnr, rmrate, balance, balance_foreign, tot_balance, guest_taxcode, repeat_charge, t_res_line_data, t_bill_data, spbill_list_data, t_bill_line_data, bill, res_line, bill_line
        nonlocal bil_flag, bil_recid, room, vipflag, fill_co, double_currency, foreign_rate


        nonlocal t_bill, t_res_line, spbill_list, t_bill_line
        nonlocal t_bill_data, t_res_line_data, spbill_list_data, t_bill_line_data


        t_bill_line_data, spbill_list_data = get_output(fo_invoice_disp_bill_line_cldbl(bil_recid, double_currency))


    abreise, resname, res_exrate, zimmer_bezeich, kreditlimit, master_str, master_rechnr, bill_anzahl, queasy_char1, disp_warning, flag_report, guest_taxcode, repeat_charge, t_res_line_data, t_bill_data = get_output(fo_invoice_open_bill_cld_2bl(bil_flag, bil_recid, room, vipflag))

    t_bill = query(t_bill_data, first=True)

    t_res_line = query(t_res_line_data, first=True)
    rescomment = get_output(fo_invoice_fill_rescommentbl(bil_recid, fill_co))

    if t_bill.rgdruck == 0:
        printed = ""
    else:
        printed = "*"
    rechnr = t_bill.rechnr
    rmrate =  to_decimal("0")

    if t_res_line:
        rmrate =  to_decimal(t_res_line.zipreis)
    balance =  to_decimal(t_bill.saldo)

    if double_currency or foreign_rate:
        balance_foreign =  to_decimal(t_bill.mwst[98])

    if bil_flag == 0:
        tot_balance =  to_decimal("0")

        if t_bill.parent_nr == 0:
            tot_balance =  to_decimal(t_bill.saldo)
        else:
            tot_balance = get_output(fo_invoice_disp_totbalancebl(bil_recid))
    spbill_list_data.clear()
    disp_bill_line()

    return generate_output()