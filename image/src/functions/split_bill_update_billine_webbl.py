from functions.additional_functions import *
import decimal
from functions.read_bill1bl import read_bill1bl
from functions.read_bill_line1bl import read_bill_line1bl
from functions.read_guestbl import read_guestbl
from functions.read_htparambl import read_htparambl
from models import Bill, Guest, Htparam, Bill_line

def split_bill_update_billine_webbl(pvilanguage:int, j:int, recid_array:int):
    balance1 = 0
    balance2 = 0
    balance3 = 0
    balance4 = 0
    bcol1 = 0
    bcol2 = 0
    bcol3 = 0
    bcol4 = 0
    t_bline1_list = []
    t_bline2_list = []
    t_bline3_list = []
    t_bline4_list = []
    lvcarea:str = "split_bill_update_billine_webbl"
    bill = guest = htparam = bill_line = None

    spbill_list = bill1 = t_guest = t_htparam = t_bline1 = t_bline2 = t_bline3 = t_bline4 = None

    spbill_list_list, Spbill_list = create_model("Spbill_list", {"selected":bool, "bl_recid":int}, {"selected": True})
    bill1_list, Bill1 = create_model_like(Bill, {"bl_recid":int})
    t_guest_list, T_guest = create_model_like(Guest)
    t_htparam_list, T_htparam = create_model_like(Htparam)
    t_bline1_list, T_bline1 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bline2_list, T_bline2 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bline3_list, T_bline3 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})
    t_bline4_list, T_bline4 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal balance1, balance2, balance3, balance4, bcol1, bcol2, bcol3, bcol4, t_bline1_list, t_bline2_list, t_bline3_list, t_bline4_list, lvcarea, bill, guest, htparam, bill_line


        nonlocal spbill_list, bill1, t_guest, t_htparam, t_bline1, t_bline2, t_bline3, t_bline4
        nonlocal spbill_list_list, bill1_list, t_guest_list, t_htparam_list, t_bline1_list, t_bline2_list, t_bline3_list, t_bline4_list
        return {"balance1": balance1, "balance2": balance2, "balance3": balance3, "balance4": balance4, "bcol1": bcol1, "bcol2": bcol2, "bcol3": bcol3, "bcol4": bcol4, "t-bline1": t_bline1_list, "t-bline2": t_bline2_list, "t-bline3": t_bline3_list, "t-bline4": t_bline4_list}

    def update_browse(j:int):

        nonlocal balance1, balance2, balance3, balance4, bcol1, bcol2, bcol3, bcol4, t_bline1_list, t_bline2_list, t_bline3_list, t_bline4_list, lvcarea, bill, guest, htparam, bill_line


        nonlocal spbill_list, bill1, t_guest, t_htparam, t_bline1, t_bline2, t_bline3, t_bline4
        nonlocal spbill_list_list, bill1_list, t_guest_list, t_htparam_list, t_bline1_list, t_bline2_list, t_bline3_list, t_bline4_list

        if (recid_array[j - 1] != 0):
            bill1_list = get_output(read_bill1bl(5, recid_array[j - 1], None, None, None, None, None, None, None, None))

            bill1 = query(bill1_list, first=True)

            if j == 1 and bill1.rechnr != 0:
                t_bline1_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
                balance1 = bill1.saldo
                bcol1 = saldo_color(bill1.gastnr, balance1)

            elif j == 2 and bill1.rechnr != 0:
                t_bline2_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
                balance2 = bill1.saldo
                bcol2 = saldo_color(bill1.gastnr, balance2)

            elif j == 3 and bill1.rechnr != 0:
                t_bline3_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
                balance3 = bill1.saldo
                bcol3 = saldo_color(bill1.gastnr, balance3)

            elif j == 4 and bill1.rechnr != 0:
                t_bline4_list = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
                balance4 = bill1.saldo
                bcol4 = saldo_color(bill1.gastnr, balance4)

    def saldo_color(gastnr:int, saldo:decimal):

        nonlocal balance1, balance2, balance3, balance4, bcol1, bcol2, bcol3, bcol4, t_bline1_list, t_bline2_list, t_bline3_list, t_bline4_list, lvcarea, bill, guest, htparam, bill_line


        nonlocal spbill_list, bill1, t_guest, t_htparam, t_bline1, t_bline2, t_bline3, t_bline4
        nonlocal spbill_list_list, bill1_list, t_guest_list, t_htparam_list, t_bline1_list, t_bline2_list, t_bline3_list, t_bline4_list

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

    update_browse(j)

    return generate_output()