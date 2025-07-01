#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill, Guest, Htparam, Res_line, Queasy, H_bill_line, H_artikel

def ts_restinv_open_tablebl(balance:Decimal, curr_dept:int, tischnr:int, curedept_flag:bool, user_init:string, user_name:string, from_acct:bool, room:string, gname:string):

    prepare_cache ([Guest, Htparam, Res_line, Queasy, H_bill_line])

    resrecid = 0
    kreditlimit = to_decimal("0.0")
    curr_room = ""
    rescomment = ""
    curr_gname = ""
    bcol = 0
    balance_foreign = to_decimal("0.0")
    printed = ""
    curr_user = ""
    order_taker = 0
    order_id = ""
    found = False
    rechnr = 0
    avail_queasy = False
    fl_code = 0
    t_h_bill_list = []
    h_bill = guest = htparam = res_line = queasy = h_bill_line = h_artikel = None

    t_h_bill = bill_guest = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resrecid, kreditlimit, curr_room, rescomment, curr_gname, bcol, balance_foreign, printed, curr_user, order_taker, order_id, found, rechnr, avail_queasy, fl_code, t_h_bill_list, h_bill, guest, htparam, res_line, queasy, h_bill_line, h_artikel
        nonlocal balance, curr_dept, tischnr, curedept_flag, user_init, user_name, from_acct, room, gname
        nonlocal bill_guest


        nonlocal t_h_bill, bill_guest
        nonlocal t_h_bill_list

        return {"balance": balance, "room": room, "gname": gname, "resrecid": resrecid, "kreditlimit": kreditlimit, "curr_room": curr_room, "rescomment": rescomment, "curr_gname": curr_gname, "bcol": bcol, "balance_foreign": balance_foreign, "printed": printed, "curr_user": curr_user, "order_taker": order_taker, "order_id": order_id, "found": found, "rechnr": rechnr, "avail_queasy": avail_queasy, "fl_code": fl_code, "t-h-bill": t_h_bill_list}

    def check_kitchenprint():

        nonlocal resrecid, kreditlimit, curr_room, rescomment, curr_gname, bcol, balance_foreign, printed, curr_user, order_taker, order_id, found, rechnr, avail_queasy, fl_code, t_h_bill_list, h_bill, guest, htparam, res_line, queasy, h_bill_line, h_artikel
        nonlocal balance, curr_dept, tischnr, curedept_flag, user_init, user_name, from_acct, room, gname
        nonlocal bill_guest


        nonlocal t_h_bill, bill_guest
        nonlocal t_h_bill_list

        h_bline = None
        h_art = None
        use_it:bool = False
        H_bline =  create_buffer("H_bline",H_bill_line)
        H_art =  create_buffer("H_art",H_artikel)

        if not use_it or curedept_flag:

            return

        if h_bill and not from_acct:
            found = False

            for h_bline in db_session.query(H_bline).filter(
                     (H_bline.departement == h_bill.departement) & (H_bline.rechnr == h_bill.rechnr) & (H_bline.steuercode > 0) & (H_bline.steuercode < 9999) & (found == False)).order_by(H_bline._recid).all():

                h_art = db_session.query(H_art).filter(
                         (H_art.departement == h_bline.departement) & (H_art.artnr == h_bline.artnr) & (H_art.bondruckernr[inc_value(0)] != 0) & (H_art.artart == 0)).first()

                if h_art:
                    found = True


    htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

    bill_guest = get_cache (Guest, {"gastnr": [(eq, htparam.finteger)]})

    if bill_guest:
        kreditlimit =  to_decimal(bill_guest.kreditlimit)

    h_bill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"tischnr": [(eq, tischnr)],"flag": [(eq, 0)]})

    if h_bill:
        fl_code = 1


        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid


        rechnr = h_bill.rechnr
        room = ""
        gname = ""

        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

            if res_line:
                resrecid = res_line._recid

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

                if guest.kreditlimit != 0:
                    kreditlimit =  to_decimal(guest.kreditlimit)
                room = res_line.zinr
                curr_room = room
                rescomment = res_line.bemerk
        gname = h_bill.bilname
        curr_gname = gname

        if balance != None and kreditlimit != None:

            if balance <= kreditlimit:
                bcol = 2
        balance =  to_decimal(h_bill.saldo)
        balance_foreign =  to_decimal(h_bill.mwst[98])

        if h_bill.rgdruck == 0:
            printed = ""
        else:
            printed = "*"

        if not curedept_flag:
            check_kitchenprint()
        curr_user = user_init + " " + user_name

        if h_bill.betriebsnr != 0:

            queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

            if queasy:
                order_taker = queasy.number1
                order_id = queasy.char1
                curr_user = curr_user + " - " + order_id
    else:
        fl_code = 2

        if res_line:
            pass

        if h_bill:
            pass
        resrecid = 0
        balance =  to_decimal("0")
        rechnr = 0
        printed = ""
        bcol = 2
        curr_user = user_init + " " + user_name

        queasy = get_cache (Queasy, {"key": [(eq, 10)]})

        if queasy:
            avail_queasy = True

    return generate_output()