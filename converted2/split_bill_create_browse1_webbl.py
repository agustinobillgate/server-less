#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_bedienerbl import read_bedienerbl
from functions.read_bill1bl import read_bill1bl
from functions.read_bill_line1bl import read_bill_line1bl
from datetime import date
from functions.htpchar import htpchar
from functions.read_guestbl import read_guestbl
from functions.read_htparambl import read_htparambl
from models import Bediener, Bill, Guest, Htparam, Bill_line

def split_bill_create_browse1_webbl(pvilanguage:int, bill_type:int, bil_recid1:int, ind:int, user_init:string, tbill_resnr:int, tbill_reslinnr:int, tbill_zinr:string):
    title_str2 = ""
    title_str3 = ""
    title_str4 = ""
    balance2 = to_decimal("0.0")
    balance3 = to_decimal("0.0")
    balance4 = to_decimal("0.0")
    bcol2 = 2
    bcol3 = 2
    bcol4 = 2
    msg_str = ""
    t_bline2_data = []
    t_bline3_data = []
    t_bline4_data = []
    lvcarea:string = "split-bill-create-browse1-webbl"
    zinr:string = ""
    i:int = 1
    recid_array:List[int] = create_empty_list(4,0)
    zugriff:bool = False
    bediener = bill = guest = htparam = bill_line = None

    t_bediener = bill1 = t_guest = t_htparam = t_bline2 = t_bline3 = t_bline4 = None

    t_bediener_data, T_bediener = create_model_like(Bediener)
    bill1_data, Bill1 = create_model_like(Bill, {"bl_recid":int})
    t_guest_data, T_guest = create_model_like(Guest)
    t_htparam_data, T_htparam = create_model_like(Htparam)
    t_bline2_data, T_bline2 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    t_bline3_data, T_bline3 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})
    t_bline4_data, T_bline4 = create_model_like(Bill_line, {"bl_recid":int, "artart":int, "tool_tip":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal title_str2, title_str3, title_str4, balance2, balance3, balance4, bcol2, bcol3, bcol4, msg_str, t_bline2_data, t_bline3_data, t_bline4_data, lvcarea, zinr, i, recid_array, zugriff, bediener, bill, guest, htparam, bill_line
        nonlocal pvilanguage, bill_type, bil_recid1, ind, user_init, tbill_resnr, tbill_reslinnr, tbill_zinr


        nonlocal t_bediener, bill1, t_guest, t_htparam, t_bline2, t_bline3, t_bline4
        nonlocal t_bediener_data, bill1_data, t_guest_data, t_htparam_data, t_bline2_data, t_bline3_data, t_bline4_data

        return {"title_str2": title_str2, "title_str3": title_str3, "title_str4": title_str4, "balance2": balance2, "balance3": balance3, "balance4": balance4, "bcol2": bcol2, "bcol3": bcol3, "bcol4": bcol4, "msg_str": msg_str, "t-bline2": t_bline2_data, "t-bline3": t_bline3_data, "t-bline4": t_bline4_data}

    def zugriff_test(user_init:string, array_nr:int, expected_nr:int):

        nonlocal title_str2, title_str3, title_str4, balance2, balance3, balance4, bcol2, bcol3, bcol4, msg_str, t_bline2_data, t_bline3_data, t_bline4_data, lvcarea, zinr, i, recid_array, zugriff, bediener, bill, guest, htparam, bill_line
        nonlocal pvilanguage, bill_type, bil_recid1, ind, tbill_resnr, tbill_reslinnr, tbill_zinr


        nonlocal t_bediener, bill1, t_guest, t_htparam, t_bline2, t_bline3, t_bline4
        nonlocal t_bediener_data, bill1_data, t_guest_data, t_htparam_data, t_bline2_data, t_bline3_data, t_bline4_data

        zugriff = True
        mail_exist:bool = False
        logical_flag:bool = False
        n:int = 0
        perm:List[int] = create_empty_list(120,0)
        s1:string = ""
        s2:string = ""
        mn_date:date = None
        anz:int = 0
        email_checked:bool = False
        p_786:string = ""

        def generate_inner_output():
            return (zugriff)

        p_786 = get_output(htpchar(786))

        if user_init == "":
            zugriff = False
            msg_str = translateExtended ("User not defined.", lvcarea, "")
        else:
            for n in range(1,length(t_bediener.permissions)  + 1) :
                perm[n - 1] = to_int(substring(t_bediener.permissions, n - 1, 1))

            if perm[array_nr - 1] < expected_nr:
                zugriff = False
                s1 = to_string(array_nr, "999")
                s2 = to_string(expected_nr)
                msg_str = translateExtended ("Sorry, No Access Right.", lvcarea, "") + chr_unicode(10) + translateExtended ("Access Code =", lvcarea, "") + " " + s1 + s2

        return generate_inner_output()


    def saldo_color(gastnr:int, saldo:Decimal):

        nonlocal title_str2, title_str3, title_str4, balance2, balance3, balance4, bcol2, bcol3, bcol4, msg_str, t_bline2_data, t_bline3_data, t_bline4_data, lvcarea, zinr, i, recid_array, zugriff, bediener, bill, guest, htparam, bill_line
        nonlocal pvilanguage, bill_type, bil_recid1, ind, user_init, tbill_resnr, tbill_reslinnr, tbill_zinr


        nonlocal t_bediener, bill1, t_guest, t_htparam, t_bline2, t_bline3, t_bline4
        nonlocal t_bediener_data, bill1_data, t_guest_data, t_htparam_data, t_bline2_data, t_bline3_data, t_bline4_data

        bg_col = 0
        kreditlimit:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (bg_col)

        t_guest_data = get_output(read_guestbl(1, gastnr, None, None))

        t_guest = query(t_guest_data, first=True)
        kreditlimit =  to_decimal(t_guest.kreditlimit)

        if kreditlimit == 0:
            t_htparam_data = get_output(read_htparambl(1, 68, None))

            t_htparam = query(t_htparam_data, first=True)

            if t_htparam.fdecimal != 0:
                kreditlimit =  to_decimal(t_htparam.fdecimal)
            else:
                kreditlimit =  to_decimal(t_htparam.finteger)

        if saldo <= kreditlimit:
            bg_col = 2
        else:
            bg_col = 12

        return generate_inner_output()

    t_bediener_data = get_output(read_bedienerbl(0, user_init))

    t_bediener = query(t_bediener_data, first=True)
    while i <= 4:

        if bil_recid1 == recid_array[i - 1] and i != ind:
            msg_str = translateExtended ("This bill has been selected on the viewport ", lvcarea, "") + to_string(i) + chr_unicode(10) + translateExtended ("Ignored the selection.", lvcarea, "")

            return generate_output()
        i = i + 1

    if bil_recid1 == 0:

        return generate_output()
    bill1_data = get_output(read_bill1bl(5, bil_recid1, None, None, None, None, None, None, None, None))

    bill1 = query(bill1_data, first=True)

    if tbill_resnr > 0:

        if (tbill_zinr).lower()  != "" and bill1.resnr == tbill_resnr and (bill1.zinr.lower()  == (tbill_zinr).lower()  or bill1.reslinnr == 0):
            pass

        elif (tbill_zinr).lower()  != "" and bill1.resnr == tbill_resnr and (bill1.zinr.lower()  != "" and bill1.zinr.lower()  != (tbill_zinr).lower()  and substring(t_bediener.permissions, 11, 1) >= ("1").lower()):
            pass

        elif tbill_reslinnr == 0 and bill1.resnr == tbill_resnr and bill1.reslinnr > 0 and substring(t_bediener.permissions, 11, 1) >= ("1").lower() :
            pass
        else:
            zugriff = zugriff_test(user_init, 12, 2)

            if not zugriff:

                return generate_output()

    elif tbill_resnr == 0:
        zugriff = zugriff_test(user_init, 55, 2)

        if not zugriff:

            return generate_output()

    if bill_type == 1:
        zinr = bill1.zinr
    else:
        zinr = ""

    if ind == 2:
        balance2 =  to_decimal(bill1.saldo)
        bcol2 = saldo_color(bill1.gastnr, balance2)
        t_bline2_data = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
        title_str2 = translateExtended ("Folio Number : ", lvcarea, "") + to_string(bill1.rechnr) + " / " + bill1.name + " / " + translateExtended ("Room Number : ", lvcarea, "") + zinr

    elif ind == 3:
        balance3 =  to_decimal(bill1.saldo)
        bcol3 = saldo_color(bill1.gastnr, balance3)
        t_bline3_data = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
        title_str3 = translateExtended ("Folio Number : ", lvcarea, "") + to_string(bill1.rechnr) + " / " + bill1.name + " / " + translateExtended ("Room Number : ", lvcarea, "") + zinr

    elif ind == 4:
        balance4 =  to_decimal(bill1.saldo)
        bcol4 = saldo_color(bill1.gastnr, balance4)
        t_bline4_data = get_output(read_bill_line1bl(3, pvilanguage, bill1.rechnr, None, None, None, None, None))
        title_str4 = translateExtended ("Folio Number : ", lvcarea, "") + to_string(bill1.rechnr) + " / " + bill1.name + " / " + translateExtended ("Room Number : ", lvcarea, "") + zinr

    return generate_output()