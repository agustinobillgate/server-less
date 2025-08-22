#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 22/8/2025
# bemerk -> bemerkung
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_bill1bl import read_bill1bl
from functions.mast_memberbl import mast_memberbl
from functions.read_guestbl import read_guestbl
from functions.read_htparambl import read_htparambl
from functions.read_bk_veranbl import read_bk_veranbl
from functions.read_bk_reserbl import read_bk_reserbl
from functions.read_bill_line_cldbl import read_bill_line_cldbl
from models import Bk_reser, Guest, Htparam, Bk_veran, Bill, Bill_line, Res_line

def mb_web_open_bill_2bl(bil_recid:int, foreign_rate:bool, double_currency:bool, ba_dept:int):

    prepare_cache ([Res_line])

    invno = ""
    gname = ""
    resname = ""
    rescomment = ""
    printed = ""
    rechnr = to_decimal("0.0")
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    kreditlimit = to_decimal("0.0")
    enbtn_bareserve = False
    guest_taxcode = ""
    t_bill_line_data = []
    t_bill_data = []
    t_data_data = []
    curr_select:string = ""
    telbill_flag:bool = False
    babill_flag:bool = False
    curr_gname:string = ""
    curr_invno:int = 0
    curr_b_recid:int = 0
    art_no:int = 0
    res_no:int = 0
    tot_adult:int = 0
    tot_room:int = 0
    room_no:string = ""
    bk_reser = guest = htparam = bk_veran = bill = bill_line = res_line = None

    t_bk_reser = t_guest = t_htparam = t_bk_veran = t_bill = t_bill_line = spbill_list = b_list = b1_list = t_data = None

    t_bk_reser_data, T_bk_reser = create_model_like(Bk_reser)
    t_guest_data, T_guest = create_model_like(Guest)
    t_htparam_data, T_htparam = create_model_like(Htparam)
    t_bk_veran_data, T_bk_veran = create_model_like(Bk_veran)
    t_bill_data, T_bill = create_model_like(Bill, {"bl_recid":int})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string, "serv":Decimal, "vat":Decimal, "netto":Decimal, "art_type":int})
    spbill_list_data, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    b_list_data, B_list = create_model("B_list", {"resnr":int, "reslinnr":int, "rechnr":int, "saldo":Decimal, "parent_nr":int})
    b1_list_data, B1_list = create_model("B1_list", {"resnr":int, "reslinnr":int, "zinr":string, "name":string, "erwachs":int, "rechnr":int, "saldo":Decimal, "resstatus":int, "ankunft":date, "abreise":date, "gname":string, "gratis":int, "kind1":int, "kind2":int, "arrangement":string, "zipreis":Decimal, "wabkurz":string})
    t_data_data, T_data = create_model("T_data", {"resnr":int, "bill_no":int, "arrival":date, "departure":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal invno, gname, resname, rescomment, printed, rechnr, balance, balance_foreign, kreditlimit, enbtn_bareserve, guest_taxcode, t_bill_line_data, t_bill_data, t_data_data, curr_select, telbill_flag, babill_flag, curr_gname, curr_invno, curr_b_recid, art_no, res_no, tot_adult, tot_room, room_no, bk_reser, guest, htparam, bk_veran, bill, bill_line, res_line
        nonlocal bil_recid, foreign_rate, double_currency, ba_dept


        nonlocal t_bk_reser, t_guest, t_htparam, t_bk_veran, t_bill, t_bill_line, spbill_list, b_list, b1_list, t_data
        nonlocal t_bk_reser_data, t_guest_data, t_htparam_data, t_bk_veran_data, t_bill_data, t_bill_line_data, spbill_list_data, b_list_data, b1_list_data, t_data_data

        return {"invno": invno, "gname": gname, "resname": resname, "rescomment": rescomment, "printed": printed, "rechnr": rechnr, "balance": balance, "balance_foreign": balance_foreign, "kreditlimit": kreditlimit, "enbtn_bareserve": enbtn_bareserve, "guest_taxcode": guest_taxcode, "t-bill-line": t_bill_line_data, "t-bill": t_bill_data, "t-data": t_data_data}

    def disp_bill_line(read_flag:bool):

        nonlocal invno, gname, resname, rescomment, printed, rechnr, balance, balance_foreign, kreditlimit, enbtn_bareserve, guest_taxcode, t_bill_line_data, t_bill_data, t_data_data, curr_select, telbill_flag, babill_flag, curr_gname, curr_invno, curr_b_recid, art_no, res_no, tot_adult, tot_room, room_no, bk_reser, guest, htparam, bk_veran, bill, bill_line, res_line
        nonlocal bil_recid, foreign_rate, double_currency, ba_dept


        nonlocal t_bk_reser, t_guest, t_htparam, t_bk_veran, t_bill, t_bill_line, spbill_list, b_list, b1_list, t_data
        nonlocal t_bk_reser_data, t_guest_data, t_htparam_data, t_bk_veran_data, t_bill_data, t_bill_line_data, spbill_list_data, b_list_data, b1_list_data, t_data_data

        if read_flag:
            t_bill_line_data = get_output(read_bill_line_cldbl(3, 1, t_bill.rechnr, None, None, None, None, None))

        for t_bill_line in query(t_bill_line_data):

            spbill_list = query(spbill_list_data, filters=(lambda spbill_list: spbill_list.bl_recid == t_bill_line.bl_recid), first=True)

            if not spbill_list:
                spbill_list = Spbill_list()
                spbill_list_data.append(spbill_list)

                spbill_list.selected = False
                spbill_list.bl_recid = t_bill_line.bl_recid


    curr_select = ""
    t_bill_data = get_output(read_bill1bl(5, bil_recid, None, None, None, None, None, None, None, None))

    t_bill = query(t_bill_data, first=True)

    if not t_bill:

        return generate_output()
    invno = to_string(t_bill.rechnr)
    curr_invno = t_bill.rechnr
    curr_gname = gname
    curr_b_recid = bil_recid
    res_no = t_bill.resnr


    curr_invno, tot_adult, tot_room, b1_list_data = get_output(mast_memberbl(res_no, curr_invno))

    for b1_list in query(b1_list_data):

        if room_no != b1_list.zinr:
            gname = gname + b1_list.name + " " + "#" + b1_list.zinr + " " + "#" + to_string(b1_list.ankunft) + "-" + to_string(b1_list.abreise) + "|"
        room_no = b1_list.zinr
    t_data_data.clear()

    res_line = get_cache (Res_line, {"resnr": [(eq, res_no)]})

    if res_line:
        t_data = T_data()
        t_data_data.append(t_data)

        t_data.resnr = res_no
        t_data.bill_no = t_bill.rechnr
        t_data.arrival = res_line.ankunft
        t_data.departure = res_line.abreise


    t_guest_data = get_output(read_guestbl(1, t_bill.gastnr, None, None))

    t_guest = query(t_guest_data, first=True)
    resname = t_guest.name + ", " + t_guest.vorname1 + t_guest.anredefirma +\
            " " + t_guest.anrede1 +\
            chr_unicode(10) + t_guest.adresse1 +\
            chr_unicode(10) + t_guest.wohnort + " " + t_guest.plz +\
            chr_unicode(10) + t_guest.land
    
    # Rd 22/8/2025
    # rescomment = t_guest.bemerk
    rescomment = t_guest.bemerkung
    art_no = t_guest.zahlungsart
    guest_taxcode = to_string(t_guest.firmen_nr)

    if t_bill.bilname != "" and t_bill.name != t_bill.bilname:
        rescomment = "Guest Name: " + t_bill.bilname + chr_unicode(10) + rescomment

    if t_bill.vesrdepot != "":
        rescomment = rescomment + chr_unicode(10) + t_bill.vesrdepot + chr_unicode(10)

    if t_bill.rgdruck == 0:
        printed = ""
    else:
        printed = "*"
    rechnr =  to_decimal(t_bill.rechnr)
    balance =  to_decimal(t_bill.saldo)

    if double_currency or foreign_rate:
        balance_foreign =  to_decimal(t_bill.mwst[98])

    if t_guest.kreditlimit != 0:
        kreditlimit =  to_decimal(t_guest.kreditlimit)
    else:
        t_htparam_data = get_output(read_htparambl(1, 68, None))

        t_htparam = query(t_htparam_data, first=True)

        if t_htparam.fdecimal != 0:
            kreditlimit =  to_decimal(t_htparam.fdecimal)
        else:
            kreditlimit =  to_decimal(t_htparam.finteger)
    spbill_list_data.clear()
    disp_bill_line(True)

    if t_bill.flag == 0 and t_bill.rechnr > 0 and t_bill.billtyp == ba_dept and (t_bill.rechnr != int (invno)):
        t_bk_veran_data = get_output(read_bk_veranbl(3, None, None, t_bill.rechnr, 0))

        t_bk_veran = query(t_bk_veran_data, first=True)

        if t_bk_veran:
            t_bk_reser_data = get_output(read_bk_reserbl(4, t_bk_veran.veran_nr, None, 1, None))

            t_bk_reser = query(t_bk_reser_data, first=True)

            if t_bk_reser:
                enbtn_bareserve = True
            else:
                enbtn_bareserve = False
    else:
        enbtn_bareserve = False

    return generate_output()