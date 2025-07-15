#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_bill2bl import read_bill2bl
from functions.read_guestbl import read_guestbl
from functions.read_htparambl import read_htparambl
from functions.read_bk_veranbl import read_bk_veranbl
from functions.read_bk_reserbl import read_bk_reserbl
from functions.read_bill_line_cldbl import read_bill_line_cldbl
from models import Bk_reser, Guest, Htparam, Bk_veran, Bill_line, Bill

def ns_web_open_bill_1bl(bil_recid:int, foreign_rate:bool, double_currency:bool, ba_dept:int):
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
    curr_select:string = ""
    telbill_flag:bool = False
    babill_flag:bool = False
    curr_gname:string = ""
    curr_invno:int = 0
    curr_b_recid:int = 0
    art_no:int = 0
    bk_reser = guest = htparam = bk_veran = bill_line = bill = None

    t_bk_reser = t_guest = t_htparam = t_bk_veran = t_bill = t_bill_line = spbill_list = None

    t_bk_reser_data, T_bk_reser = create_model_like(Bk_reser)
    t_guest_data, T_guest = create_model_like(Guest)
    t_htparam_data, T_htparam = create_model_like(Htparam)
    t_bk_veran_data, T_bk_veran = create_model_like(Bk_veran)
    t_bill_data, T_bill = create_model("T_bill", {"zinr":string, "flag":int, "rechnr":int, "resnr":int, "gastnr":int, "saldo":Decimal, "gesamtumsatz":Decimal, "logisumsatz":Decimal, "arrangemdat":date, "rgdruck":int, "logiernachte":int, "reslinnr":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "billnr":int, "firstper":bool, "billkur":bool, "logidat":date, "bilname":string, "teleinheit":int, "telsumme":Decimal, "segmentcode":int, "printnr":int, "billbankett":bool, "service":[Decimal,99], "mwst":[Decimal,99], "umleit_zinr":string, "billmaster":bool, "datum":date, "taxsumme":Decimal, "name":string, "billtyp":int, "parent_nr":int, "restargt":Decimal, "init_argt":Decimal, "rest_tage":int, "ums_kurz":Decimal, "ums_lang":Decimal, "nextargt_bookdate":date, "roomcharge":bool, "oldzinr":string, "t_rechnr":int, "rechnr2":int, "betriebsnr":int, "vesrdep":Decimal, "vesrdat":date, "vesrdepot":string, "vesrdepot2":string, "vesrcod":string, "verstat":int, "kontakt_nr":int, "betrieb_gast":int, "billref":int, "bl_recid":int})
    t_bill_line_data, T_bill_line = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string, "serv":Decimal, "vat":Decimal, "netto":Decimal, "art_type":int})
    spbill_list_data, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal invno, gname, resname, rescomment, printed, rechnr, balance, balance_foreign, kreditlimit, enbtn_bareserve, guest_taxcode, t_bill_line_data, t_bill_data, curr_select, telbill_flag, babill_flag, curr_gname, curr_invno, curr_b_recid, art_no, bk_reser, guest, htparam, bk_veran, bill_line, bill
        nonlocal bil_recid, foreign_rate, double_currency, ba_dept


        nonlocal t_bk_reser, t_guest, t_htparam, t_bk_veran, t_bill, t_bill_line, spbill_list
        nonlocal t_bk_reser_data, t_guest_data, t_htparam_data, t_bk_veran_data, t_bill_data, t_bill_line_data, spbill_list_data

        return {"invno": invno, "gname": gname, "resname": resname, "rescomment": rescomment, "printed": printed, "rechnr": rechnr, "balance": balance, "balance_foreign": balance_foreign, "kreditlimit": kreditlimit, "enbtn_bareserve": enbtn_bareserve, "guest_taxcode": guest_taxcode, "t-bill-line": t_bill_line_data, "t-bill": t_bill_data}

    def disp_bill_line(read_flag:bool):

        nonlocal invno, gname, resname, rescomment, printed, rechnr, balance, balance_foreign, kreditlimit, enbtn_bareserve, guest_taxcode, t_bill_line_data, t_bill_data, curr_select, telbill_flag, babill_flag, curr_gname, curr_invno, curr_b_recid, art_no, bk_reser, guest, htparam, bk_veran, bill_line, bill
        nonlocal bil_recid, foreign_rate, double_currency, ba_dept


        nonlocal t_bk_reser, t_guest, t_htparam, t_bk_veran, t_bill, t_bill_line, spbill_list
        nonlocal t_bk_reser_data, t_guest_data, t_htparam_data, t_bk_veran_data, t_bill_data, t_bill_line_data, spbill_list_data

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

    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if not bill:

        return generate_output()
    telbill_flag, babill_flag, t_bill_data = get_output(read_bill2bl(5, bil_recid, None, None, None, None, None, None, None, None))

    t_bill = query(t_bill_data, first=True)
    invno = to_string(t_bill.rechnr)
    curr_invno = t_bill.rechnr
    curr_gname = gname
    curr_b_recid = bil_recid


    t_guest_data = get_output(read_guestbl(1, t_bill.gastnr, None, None))

    t_guest = query(t_guest_data, first=True)
    resname = t_guest.name + ", " + t_guest.vorname1 + t_guest.anredefirma +\
            " " + t_guest.anrede1 +\
            chr_unicode(10) + t_guest.adresse1 +\
            chr_unicode(10) + t_guest.wohnort + " " + t_guest.plz +\
            chr_unicode(10) + t_guest.land
    rescomment = t_guest.bemerk
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