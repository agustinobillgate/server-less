from functions.additional_functions import *
import decimal
from functions.read_bill1bl import read_bill1bl
from functions.read_bill_line1bl import read_bill_line1bl
from functions.read_guestbl import read_guestbl
from functions.read_htparambl import read_htparambl
from models import Bill, Guest, Htparam, Bill_line

def split_bill_create_newbrowse_webbl(pvilanguage:int, newbill_recid:int, recid_array2:int, recid_array3:int, recid_array4:int):
    recid_array = 0
    title_str2 = ""
    title_str3 = ""
    title_str4 = ""
    balance2 = 0
    balance3 = 0
    balance4 = 0
    bcol2 = 0
    bcol3 = 0
    bcol4 = 0
    t_bline2_list = []
    t_bline3_list = []
    t_bline4_list = []
    lvcarea:str = "split_bill_create_newbrowse_webbl"
    zinr:str = ""
    ind:int = 0
    bill = guest = htparam = bill_line = None

    bill1 = t_guest = t_htparam = t_bline2 = t_bline3 = t_bline4 = None

    bill1_list, Bill1 = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    t_htparam_list, T_htparam = create_model_like(Htparam)
    t_bline2_list, T_bline2 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bline3_list, T_bline3 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bline4_list, T_bline4 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_array, title_str2, title_str3, title_str4, balance2, balance3, balance4, bcol2, bcol3, bcol4, t_bline2_list, t_bline3_list, t_bline4_list, lvcarea, zinr, ind, bill, guest, htparam, bill_line


        nonlocal bill1, t_guest, t_htparam, t_bline2, t_bline3, t_bline4
        nonlocal bill1_list, t_guest_list, t_htparam_list, t_bline2_list, t_bline3_list, t_bline4_list
        return {"recid_array": recid_array, "title_str2": title_str2, "title_str3": title_str3, "title_str4": title_str4, "balance2": balance2, "balance3": balance3, "balance4": balance4, "bcol2": bcol2, "bcol3": bcol3, "bcol4": bcol4, "t-bline2": t_bline2_list, "t-bline3": t_bline3_list, "t-bline4": t_bline4_list}

    def saldo_color(gastnr:int, saldo:decimal):

        nonlocal recid_array, title_str2, title_str3, title_str4, balance2, balance3, balance4, bcol2, bcol3, bcol4, t_bline2_list, t_bline3_list, t_bline4_list, lvcarea, zinr, ind, bill, guest, htparam, bill_line


        nonlocal bill1, t_guest, t_htparam, t_bline2, t_bline3, t_bline4
        nonlocal bill1_list, t_guest_list, t_htparam_list, t_bline2_list, t_bline3_list, t_bline4_list

        bg_col = 0
        kreditlimit:decimal = 0

        def generate_inner_output():
            return bg_col
        t_guest_list = get_output(read_guestbl(1, gastnr, None, None))

        t_guest = query(t_guest_list, first=True)
        kreditlimit = t_guest.kreditlimit

        if kreditlimit == 0:
            t_htparam_list = get_output(read_htparambl(1, 68, None))

            t_htparam = query(t_htparam_list, first=True)

            if t_htparam.fdecimal != 0:
                kreditlimit = t_htparam.fdecimal
            else:
                kreditlimit = t_htparam.finteger

        if saldo <= kreditlimit:
            bg_col = 2
        else:
            bg_col = 12


        return generate_inner_output()


    if recid_array2 == 0:
        ind = 2

    elif recid_array3 == 0:
        ind = 3

    elif recid_array4 == 0:
        ind = 4

    if ind != 0:
        recid_array[ind - 1] = newbill_recid
        bill1_list = get_output(read_bill1bl(5, newbill_recid, None, None, None, None, None, None, None, None))

        bill1 = query(bill1_list, first=True)
        zinr = bill1.zinr

        if ind == 2:
            balance2 = bill1.saldo
            bcol2 = saldo_color(bill1.gastnr, balance2)
            t_bline2_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
            title_str2 = translateExtended ("Folio Number : ", lvcarea, "") + to_string(bill1.rechnr) + " / " + bill1.name + " / " + translateExtended ("Room Number : ", lvcarea, "") + zinr

        elif ind == 3:
            balance3 = bill1.saldo
            bcol3 = saldo_color(bill1.gastnr, balance3)
            t_bline3_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
            title_str3 = translateExtended ("Folio Number : ", lvcarea, "") + to_string(bill1.rechnr) + " / " + bill1.name + " / " + translateExtended ("Room Number : ", lvcarea, "") + zinr

        elif ind == 4:
            balance4 = bill1.saldo
            bcol4 = saldo_color(bill1.gastnr, balance4)
            t_bline4_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
            title_str4 = translateExtended ("Folio Number : ", lvcarea, "") + to_string(bill1.rechnr) + " / " + bill1.name + " / " + translateExtended ("Room Number : ", lvcarea, "") + zinr

    return generate_output()