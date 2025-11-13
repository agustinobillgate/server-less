# using conversion tools version: 1.0.0.119
"""_yusufwijasena_

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - add import from function_py
"""
from functions.additional_functions import *
from decimal import Decimal
# from functions.read_billbl import read_billbl
# from functions.read_bill1bl import read_bill1bl
# from functions.read_bill_line1bl import read_bill_line1bl
# from functions.read_guestbl import read_guestbl
# from functions.read_htparambl import read_htparambl
from functions_py.read_billbl import read_billbl
from functions_py.read_bill1bl import read_bill1bl
from functions_py.read_bill_line1bl import read_bill_line1bl
from functions_py.read_guestbl import read_guestbl
from functions_py.read_htparambl import read_htparambl
from models import Bill, Guest, Htparam, Bill_line


def prepare_split_bill_webbl(pvilanguage: int, bil_recid: int):
    closed_bill = False
    bill_anzahl = 0
    title_str1 = ""
    title_str2 = ""
    title_str3 = ""
    title_str4 = ""
    recid_array = [0, 0, 0, 0]
    balance1 = to_decimal("0.0")
    balance2 = to_decimal("0.0")
    balance3 = to_decimal("0.0")
    balance4 = to_decimal("0.0")
    bcol1 = 2
    bcol2 = 2
    bcol3 = 2
    bcol4 = 2
    t_bill_data = []
    t_bline1_data = []
    t_bline2_data = []
    t_bline3_data = []
    t_bline4_data = []
    lvcarea: str = "prepare-split-bill-webbl"
    bill = guest = htparam = bill_line = None

    t_bill = bill1 = t_guest = t_htparam = t_bline1 = t_bline2 = t_bline3 = t_bline4 = None

    t_bill_data, T_bill = create_model_like(Bill)
    bill1_data, Bill1 = create_model_like(Bill, {"bl_recid": int})
    t_guest_data, T_guest = create_model_like(Guest)
    t_htparam_data, T_htparam = create_model_like(Htparam)
    t_bline1_data, T_bline1 = create_model_like(
        Bill_line,
        {
            "bl_recid": int,
            "artart": int,
            "tool_tip": str
        })
    t_bline2_data, T_bline2 = create_model_like(
        Bill_line,
        {
            "bl_recid": int,
            "artart": int,
            "tool_tip": str
        })
    t_bline3_data, T_bline3 = create_model_like(
        Bill_line,
        {
            "bl_recid": int,
            "artart": int,
            "tool_tip": str
        })
    t_bline4_data, T_bline4 = create_model_like(
        Bill_line,
        {
            "bl_recid": int,
            "artart": int,
            "tool_tip": str
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal closed_bill, bill_anzahl, title_str1, title_str2, title_str3, title_str4, recid_array, balance1, balance2, balance3, balance4, bcol1, bcol2, bcol3, bcol4, t_bill_data, t_bline1_data, t_bline2_data, t_bline3_data, t_bline4_data, lvcarea, bill, guest, htparam, bill_line
        nonlocal pvilanguage, bil_recid
        nonlocal t_bill, bill1, t_guest, t_htparam, t_bline1, t_bline2, t_bline3, t_bline4
        nonlocal t_bill_data, bill1_data, t_guest_data, t_htparam_data, t_bline1_data, t_bline2_data, t_bline3_data, t_bline4_data

        return {
            "closed_bill": closed_bill,
            "bill_anzahl": bill_anzahl,
            "title_str1": title_str1,
            "title_str2": title_str2,
            "title_str3": title_str3,
            "title_str4": title_str4,
            "recid_array": recid_array,
            "balance1": balance1,
            "balance2": balance2,
            "balance3": balance3,
            "balance4": balance4,
            "bcol1": bcol1,
            "bcol2": bcol2,
            "bcol3": bcol3,
            "bcol4": bcol4,
            "t-bill": t_bill_data,
            "t-bline1": t_bline1_data,
            "t-bline2": t_bline2_data,
            "t-bline3": t_bline3_data,
            "t-bline4": t_bline4_data
        }

    def create_browse():
        nonlocal closed_bill, bill_anzahl, title_str1, title_str2, title_str3, title_str4, recid_array, balance1, balance2, balance3, balance4, bcol1, bcol2, bcol3, bcol4, t_bill_data, t_bline1_data, t_bline2_data, t_bline3_data, t_bline4_data, lvcarea, bill, guest, htparam, bill_line
        nonlocal pvilanguage, bil_recid
        nonlocal t_bill, bill1, t_guest, t_htparam, t_bline1, t_bline2, t_bline3, t_bline4
        nonlocal t_bill_data, bill1_data, t_guest_data, t_htparam_data, t_bline1_data, t_bline2_data, t_bline3_data, t_bline4_data

        i: int = 1
        j: int = 2
        billnr1: int = 0
        t_bill_data = get_output(read_billbl(16, bil_recid, None, None, None))

        t_bill = query(t_bill_data, first=True)
        billnr1 = t_bill.billnr
        title_str1 = translateExtended("Folio Number : ", lvcarea, "") + \
            to_string(t_bill.rechnr) + " / " + t_bill.name + " / " + \
            translateExtended("Room Number : ", lvcarea, "") + \
            t_bill.zinr + "|" + to_string(t_bill.billnr)

        if t_bill.rechnr != 0:
            t_bline1_data = get_output(read_bill_line1bl(
                3, pvilanguage, t_bill.rechnr, None, None, None, None, None))
        recid_array[0] = bil_recid
        balance1 = to_decimal(t_bill.saldo)
        bcol1 = saldo_color(t_bill.gastnr, balance1)
        while i <= bill_anzahl:
            if i != billnr1:
                bill1_data = get_output(read_bill1bl(
                    12, i, t_bill.resnr, t_bill.parent_nr, 0, t_bill.zinr, None, None, None, None))

                bill1 = query(bill1_data, first=True)

                if bill1:
                    if j == 2:
                        balance2 = to_decimal(bill1.saldo)
                        bcol2 = saldo_color(bill1.gastnr, balance2)
                        title_str2 = translateExtended("Folio Number : ", lvcarea, "") + \
                            to_string(bill1.rechnr) + " / " + bill1.name + " / " + \
                            translateExtended("Room Number : ", lvcarea, "") + \
                            bill1.zinr + "|" + to_string(bill1.billnr)
                        t_bline2_data = get_output(read_bill_line1bl(
                            3, pvilanguage, bill1.rechnr, None, None, None, None, None))

                    elif j == 3:
                        balance3 = to_decimal(bill1.saldo)
                        bcol3 = saldo_color(bill1.gastnr, balance3)
                        title_str3 = translateExtended("Folio Number : ", lvcarea, "") + \
                            to_string(bill1.rechnr) + " / " + bill1.name + " / " + \
                            translateExtended("Room Number : ", lvcarea, "") + \
                            bill1.zinr + "|" + to_string(bill1.billnr)
                        t_bline3_data = get_output(read_bill_line1bl(
                            3, pvilanguage, bill1.rechnr, None, None, None, None, None))

                    elif j == 4:
                        balance4 = to_decimal(bill1.saldo)
                        bcol4 = saldo_color(bill1.gastnr, balance4)
                        title_str4 = translateExtended("Folio Number : ", lvcarea, "") + \
                            to_string(bill1.rechnr) + " / " + bill1.name + " / " + \
                            translateExtended("Room Number : ", lvcarea, "") + \
                            bill1.zinr + "|" + to_string(bill1.billnr)
                        t_bline4_data = get_output(read_bill_line1bl(
                            3, pvilanguage, bill1.rechnr, None, None, None, None, None))
                    recid_array[j - 1] = bill1.bl_recid
                j = j + 1
            i = i + 1

    def saldo_color(gastnr: int, saldo: Decimal):
        nonlocal closed_bill, bill_anzahl, title_str1, title_str2, title_str3, title_str4, recid_array, balance1, balance2, balance3, balance4, bcol1, bcol2, bcol3, bcol4, t_bill_data, t_bline1_data, t_bline2_data, t_bline3_data, t_bline4_data, lvcarea, bill, guest, htparam, bill_line
        nonlocal pvilanguage, bil_recid
        nonlocal t_bill, bill1, t_guest, t_htparam, t_bline1, t_bline2, t_bline3, t_bline4
        nonlocal t_bill_data, bill1_data, t_guest_data, t_htparam_data, t_bline1_data, t_bline2_data, t_bline3_data, t_bline4_data

        bg_col = 0
        kreditlimit: Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (bg_col)

        t_guest_data = get_output(read_guestbl(1, gastnr, None, None))

        t_guest = query(t_guest_data, first=True)
        kreditlimit = to_decimal(t_guest.kreditlimit)

        if kreditlimit == 0:
            t_htparam_data = get_output(read_htparambl(1, 68, None))

            t_htparam = query(t_htparam_data, first=True)

            if t_htparam.fdecimal != 0:
                kreditlimit = to_decimal(t_htparam.fdecimal)
            else:
                kreditlimit = to_decimal(t_htparam.finteger)

        if saldo <= kreditlimit:
            bg_col = 2
        else:
            bg_col = 12

        return generate_inner_output()

    t_bill_data = get_output(read_billbl(16, bil_recid, None, None, None))

    t_bill = query(t_bill_data, first=True)

    if t_bill:
        closed_bill = (t_bill.flag == 1)
        bill_anzahl = 0
        bill1_data = get_output(read_bill1bl(
            2, None, t_bill.resnr, t_bill.parent_nr, 0, t_bill.zinr, None, None, None, None))

        for bill1 in query(bill1_data):
            bill_anzahl = bill_anzahl + 1
        create_browse()

    return generate_output()
