from functions.additional_functions import *
import decimal
from models import H_bill, Guest, Htparam, Res_line, Queasy, H_bill_line, H_artikel

def ts_restinv_open_tablebl(balance:decimal, curr_dept:int, tischnr:int, curedept_flag:bool, user_init:str, user_name:str, from_acct:bool, room:str, gname:str):
    resrecid = 0
    kreditlimit = 0
    curr_room = ""
    rescomment = ""
    curr_gname = ""
    bcol = 0
    balance_foreign = 0
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

    t_h_bill = bill_guest = h_bline = h_art = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})

    Bill_guest = Guest
    H_bline = H_bill_line
    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resrecid, kreditlimit, curr_room, rescomment, curr_gname, bcol, balance_foreign, printed, curr_user, order_taker, order_id, found, rechnr, avail_queasy, fl_code, t_h_bill_list, h_bill, guest, htparam, res_line, queasy, h_bill_line, h_artikel
        nonlocal bill_guest, h_bline, h_art


        nonlocal t_h_bill, bill_guest, h_bline, h_art
        nonlocal t_h_bill_list
        return {"resrecid": resrecid, "kreditlimit": kreditlimit, "curr_room": curr_room, "rescomment": rescomment, "curr_gname": curr_gname, "bcol": bcol, "balance_foreign": balance_foreign, "printed": printed, "curr_user": curr_user, "order_taker": order_taker, "order_id": order_id, "found": found, "rechnr": rechnr, "avail_queasy": avail_queasy, "fl_code": fl_code, "t-h-bill": t_h_bill_list}

    def check_kitchenprint():

        nonlocal resrecid, kreditlimit, curr_room, rescomment, curr_gname, bcol, balance_foreign, printed, curr_user, order_taker, order_id, found, rechnr, avail_queasy, fl_code, t_h_bill_list, h_bill, guest, htparam, res_line, queasy, h_bill_line, h_artikel
        nonlocal bill_guest, h_bline, h_art


        nonlocal t_h_bill, bill_guest, h_bline, h_art
        nonlocal t_h_bill_list

        use_it:bool = False
            H_bline = H_bill_line
            H_art = H_artikel

            if not use_it or curedept_flag:

                return

            if h_bill and not from_acct:
                found = False

                for h_bline in db_session.query(H_bline).filter(
                        (H_bline.departement == h_bill.departement) &  (H_bline.rechnr == h_bill.rechnr) &  (H_bline.steuercode > 0) &  (H_bline.steuercode < 9999) &  (H_bline.found == False)).all():

                    h_art = db_session.query(H_art).filter(
                            (H_art.departement == h_bline.departement) &  (H_art.artnr == h_bline.artnr) &  (H_art.bondruckernr[0] != 0) &  (H_art.artart == 0)).first()

                    if h_art:
                        found = True

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 867)).first()

    bill_guest = db_session.query(Bill_guest).filter(
            (Bill_guest.gastnr == htparam.finteger)).first()

    if bill_guest:
        kreditlimit = bill_guest.kreditlimit

    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == curr_dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()

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

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == h_bill.resnr) &  (Res_line.reslinnr == h_bill.reslinnr)).first()

            if res_line:
                resrecid = res_line._recid

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrpay)).first()

                if guest.kreditlimit != 0:
                    kreditlimit = guest.kreditlimit
                room = res_line.zinr
                curr_room = room
                rescomment = res_line.bemerk
        gname = h_bill.bilname
        curr_gname = gname

        if balance <= kreditlimit:
            bcol = 2
        balance = h_bill.saldo
        balance_foreign = h_bill.mwst[98]

        if h_bill.rgdruck == 0:
            printed = ""
        else:
            printed = "*"

        if not curedept_flag:
            check_kitchenprint()
        curr_user = user_init + " " + user_name

        if h_bill.betriebsnr != 0:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 10) &  (Queasy.number1 == h_bill.betriebsnr)).first()

            if queasy:
                order_taker = queasy.number1
                order_id = queasy.char1
                curr_user = curr_user + " - " + order_id
    else:
        fl_code = 2

        if res_line:


            if h_bill:

                resrecid = 0
            balance = 0
            rechnr = 0
            printed = ""
            bcol = 2
            curr_user = user_init + " " + user_name

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 10)).first()

            if queasy:
                avail_queasy = True

    return generate_output()