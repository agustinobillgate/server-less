from functions.additional_functions import *
import decimal
from datetime import date
from functions.inv_checking_create_main_cldbl import inv_checking_create_main_cldbl
from functions.inv_checking_create_sub_cldbl import inv_checking_create_sub_cldbl
from functions.inv_checking_create_gl_cldbl import inv_checking_create_gl_cldbl
from functions.inv_checking_create_list_cldbl import inv_checking_create_list_cldbl
from functions.inv_checking_create_list2_cldbl import inv_checking_create_list2_cldbl
from functions.inv_checking_out_gl_cldbl import inv_checking_out_gl_cldbl
from functions.inv_checking_end_gl_cldbl import inv_checking_end_gl_cldbl

def inv_checking_cldbl(fromdate:date, todate:date, inventorytype:int, outgoingprefix:str, maingroup:bool, subgroup:bool, maingroupgl:bool, receivinggl:bool, outgoinggl:bool, beginbalanceinvgl:bool, endingbalanceinvgl:bool):
    artikel1_list = []
    artikel2_list = []
    artikel3_list = []
    coa_list2_list = []
    coa_list3_list = []
    s_list2_list = []
    s_list3_list = []
    art_list_list = []
    art_list2_list = []
    art_list3_list = []
    art_list4_list = []
    d1:date = None
    d2:date = None
    d:date = None
    invtype:int = 0
    frnr:int = 0
    tonr:int = 0
    fibu:str = ""
    art1:int = 0
    art2:int = 0
    mon:int = 0
    refno:str = ""
    saldo:decimal = to_decimal("0.0")
    detail1:bool = False
    detail2:bool = False
    detail3:bool = False
    detail4:bool = False
    detail5:bool = False
    detail6:bool = False
    detail7:bool = False

    coa_list = coa_list2 = coa_list3 = s_list = s_list2 = s_list3 = artikel1 = artikel2 = artikel3 = art_list = art_list2 = art_list3 = art_list4 = None

    coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":str, "datum":date, "wert":decimal, "debit":decimal, "credit":decimal})
    coa_list2_list, Coa_list2 = create_model("Coa_list2", {"datum1":date, "wert1":decimal, "fibu1":str, "debitcredit":decimal, "diff":decimal})
    coa_list3_list, Coa_list3 = create_model("Coa_list3", {"datum2":date, "wert2":decimal, "fibu2":str, "creditdebit":decimal, "diff":decimal})
    s_list_list, S_list = create_model("S_list", {"fibu":str, "saldo1":decimal, "saldo2":decimal, "saldo":decimal})
    s_list2_list, S_list2 = create_model("S_list2", {"fibu1":str, "saldo1a":decimal, "saldo2a":decimal, "saldo1":decimal, "saldo3":decimal})
    s_list3_list, S_list3 = create_model("S_list3", {"fibu2":str, "saldo1b":decimal, "saldo2b":decimal, "saldo3a":decimal, "saldo11":decimal})
    artikel1_list, Artikel1 = create_model("Artikel1", {"art":int, "ekum":int, "zeich":str})
    artikel2_list, Artikel2 = create_model("Artikel2", {"art":int, "ekum":int, "zeich":str, "zeich2":str, "numb":int})
    artikel3_list, Artikel3 = create_model("Artikel3", {"kum":int, "zeich2":str, "numb":int, "fibu":str, "zeich3":str})
    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "artname":str, "saldo1":decimal, "saldo2":decimal})
    art_list2_list, Art_list2 = create_model("Art_list2", {"artnr":int, "artname":str, "saldo1":decimal, "saldo2":decimal})
    art_list3_list, Art_list3 = create_model("Art_list3", {"datum":date, "artnr":int, "artname":str, "saldo1":decimal, "saldo2":decimal})
    art_list4_list, Art_list4 = create_model("Art_list4", {"datum":date, "artnr":int, "artname":str, "saldo1":decimal, "saldo2":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel1_list, artikel2_list, artikel3_list, coa_list2_list, coa_list3_list, s_list2_list, s_list3_list, art_list_list, art_list2_list, art_list3_list, art_list4_list, d1, d2, d, invtype, frnr, tonr, fibu, art1, art2, mon, refno, saldo, detail1, detail2, detail3, detail4, detail5, detail6, detail7
        nonlocal fromdate, todate, inventorytype, outgoingprefix, maingroup, subgroup, maingroupgl, receivinggl, outgoinggl, beginbalanceinvgl, endingbalanceinvgl


        nonlocal coa_list, coa_list2, coa_list3, s_list, s_list2, s_list3, artikel1, artikel2, artikel3, art_list, art_list2, art_list3, art_list4
        nonlocal coa_list_list, coa_list2_list, coa_list3_list, s_list_list, s_list2_list, s_list3_list, artikel1_list, artikel2_list, artikel3_list, art_list_list, art_list2_list, art_list3_list, art_list4_list
        return {"artikel1": artikel1_list, "artikel2": artikel2_list, "artikel3": artikel3_list, "coa-list2": coa_list2_list, "coa-list3": coa_list3_list, "s-list2": s_list2_list, "s-list3": s_list3_list, "art-list": art_list_list, "art-list2": art_list2_list, "art-list3": art_list3_list, "art-list4": art_list4_list}


    d1 = fromdate
    d2 = todate
    invtype = inventorytype
    refno = outgoingprefix
    detail1 = maingroup
    detail2 = subgroup
    detail3 = maingroupgl
    detail4 = beginbalanceinvgl
    detail5 = receivinggl
    detail6 = outgoinggl
    detail7 = endingbalanceinvgl

    if detail1:
        artikel1_list = get_output(inv_checking_create_main_cldbl())

    if detail2:
        artikel2_list = get_output(inv_checking_create_sub_cldbl())

    if detail3:
        artikel3_list = get_output(inv_checking_create_gl_cldbl())

    if detail4:
        saldo, s_list2_list, art_list2_list = get_output(inv_checking_create_list_cldbl(invtype, d1))

    if detail5:
        frnr, tonr, saldo, coa_list2_list, art_list3_list = get_output(inv_checking_create_list2_cldbl(coa_list_list, invtype, d1, d2))

    if detail6:
        frnr, tonr, saldo, coa_list3_list, art_list4_list = get_output(inv_checking_out_gl_cldbl(invtype, d1, d2))

    if detail7:
        s_list3_list, art_list_list = get_output(inv_checking_end_gl_cldbl(frnr, tonr, d2, saldo))

    return generate_output()