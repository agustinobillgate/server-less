from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from models import H_bill, Tisch, Queasy, Htparam, Res_line, Mc_guest, Guest, Bill

def ts_tbplan_check_table_webbl(pvilanguage:int, resnr:int, reslinnr:int, tischnr:int, curr_waiter:int, tkellner_masterkey:bool, dept_no:int, t_h_bill:[T_h_bill], t_tisch:[T_tisch]):
    rmno = ""
    remark = ""
    klimit = 0
    ksaldo = 0
    recid_bill = 0
    avail_bill = False
    resline = False
    msg_str = ""
    lvcarea:str = "TS_tbplan"
    p_1342:bool = False
    table_ok:bool = True
    i:int = 0
    str:str = ""
    child_age:str = ""
    ci_date:date = None
    h_bill = tisch = queasy = htparam = res_line = mc_guest = guest = bill = None

    t_h_bill = t_tisch = t_queasy33 = t_queasy31 = None

    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_tisch_list, T_tisch = create_model_like(Tisch)
    t_queasy33_list, T_queasy33 = create_model_like(Queasy)
    t_queasy31_list, T_queasy31 = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmno, remark, klimit, ksaldo, recid_bill, avail_bill, resline, msg_str, lvcarea, p_1342, table_ok, i, str, child_age, ci_date, h_bill, tisch, queasy, htparam, res_line, mc_guest, guest, bill


        nonlocal t_h_bill, t_tisch, t_queasy33, t_queasy31
        nonlocal t_h_bill_list, t_tisch_list, t_queasy33_list, t_queasy31_list
        return {"rmno": rmno, "remark": remark, "klimit": klimit, "ksaldo": ksaldo, "recid_bill": recid_bill, "avail_bill": avail_bill, "resline": resline, "msg_str": msg_str}

    def check_creditlimit():

        nonlocal rmno, remark, klimit, ksaldo, recid_bill, avail_bill, resline, msg_str, lvcarea, p_1342, table_ok, i, str, child_age, ci_date, h_bill, tisch, queasy, htparam, res_line, mc_guest, guest, bill


        nonlocal t_h_bill, t_tisch, t_queasy33, t_queasy31
        nonlocal t_h_bill_list, t_tisch_list, t_queasy33_list, t_queasy31_list

        answer:bool = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 68)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrpay)).first()

        mc_guest = db_session.query(Mc_guest).filter(
                (Mc_guest.gastnr == guest.gastnr) &  (Mc_guest.activeflag)).first()

        if mc_guest:
            remark = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr(10)

        if guest.kreditlimit != 0:
            klimit = guest.kreditlimit
        else:

            if htparam.fdecimal != 0:
                klimit = htparam.fdecimal
            else:
                klimit = htparam.finteger
        ksaldo = 0

        bill = db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr) &  (Bill.flag == 0) &  (Bill.zinr == res_line.zinr)).first()

        if bill:
            recid_bill = bill._recid
            avail_bill = True
            ksaldo = bill.saldo
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 5) == "ChAge":
                child_age = substring(str, 5)

        if child_age != "":
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " " + "(" + child_age + ")" + " - " + res_line.arrangement + chr(10) + res_line.bemerk
        else:
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " - " + res_line.arrangement + chr(10) + res_line.bemerk

    def getremark_rsv_table():

        nonlocal rmno, remark, klimit, ksaldo, recid_bill, avail_bill, resline, msg_str, lvcarea, p_1342, table_ok, i, str, child_age, ci_date, h_bill, tisch, queasy, htparam, res_line, mc_guest, guest, bill


        nonlocal t_h_bill, t_tisch, t_queasy33, t_queasy31
        nonlocal t_h_bill_list, t_tisch_list, t_queasy33_list, t_queasy31_list

        hh1:str = ""
        hh2:str = ""
        hh3:str = ""
        zeit:int = 0
        table_occupied:bool = False

        t_queasy31 = query(t_queasy31_list, filters=(lambda t_queasy31 :t_queasy31.number2 == tischnr), first=True)
        table_occupied = None != t_queasy31 and t_queasy31.date1 != None
        hh1 = to_string(get_current_time_in_seconds(), "HH:MM")
        hh1 = substring(hh1, 0, 2) + substring(hh1, 3, 2)
        hh2 = to_string(to_int(substring(hh1, 0, 2)) + 2, "99") + substring(hh1, 2, 2)
        hh3 = to_string(get_current_time_in_seconds() - 1800, "HH:MM")
        hh3 = substring(hh3, 0, 2) + substring(hh3, 3, 2)

        t_queasy33 = query(t_queasy33_list, filters=(lambda t_queasy33 :t_queasy33.number2 == tischnr and hh1 <= t_queasy33.char1 and hh2 >= t_queasy33.char1), first=True)

        if not t_queasy33 and not table_occupied:

            t_queasy33 = query(t_queasy33_list, filters=(lambda t_queasy33 :t_queasy33.number2 == tischnr and hh1 >= t_queasy33.char1 and hh3 <= t_queasy33.char1), first=True)

        if t_queasy33:
            zeit = to_int(substring(t_queasy33.char1, 0, 2)) * 3600 + to_int(substring(t_queasy33.char1, 2, 2)) * 60

            if zeit > get_current_time_in_seconds():
                remark = remark + entry(0, t_queasy33.char2, "&&") + " - " + trim(substring(t_queasy33.char1, 9)) + chr(10) + to_string(substring(t_queasy33.char1, 0, 4) , "99:99") + " - " + to_string(substring(t_queasy33.char1, 4, 4) , "99:99") + chr(10) + translateExtended ("Pax:", lvcarea, "") + " " + to_string(t_queasy33.number3) + chr(10) + translateExtended ("Remain Time:", lvcarea, "") + " " + to_string(zeit - get_current_time_in_seconds(), "HH:MM")
            else:
                remark = remark + entry(0, t_queasy33.char2, "&&") + " - " + trim(substring(t_queasy33.char1, 9)) + chr(10) + to_string(substring(t_queasy33.char1, 0, 4) , "99:99") + " - " + to_string(substring(t_queasy33.char1, 4, 4) , "99:99") + chr(10) + translateExtended ("Pax:", lvcarea, "") + " " + to_string(t_queasy33.number3) + chr(10) + translateExtended ("Current Time:", lvcarea, "") + " " + to_string(get_current_time_in_seconds(), "HH:MM")


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 33) &  (Queasy.number1 == dept_no) &  (Queasy.date1 == ci_date) &  (Queasy.logi3)).all():
        t_queasy33 = T_queasy33()
        t_queasy33_list.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 31) &  (Queasy.number1 == dept_no) &  (Queasy.betriebsnr == 0)).all():
        t_queasy31 = T_queasy31()
        t_queasy31_list.append(t_queasy31)

        buffer_copy(queasy, t_queasy31)
        t_queasy31.rec_id = queasy._recid

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    if res_line:
        resline = True
        check_creditlimit()
        rmno = res_line.zinr
    else:

        t_h_bill = query(t_h_bill_list, filters=(lambda t_h_bill :t_h_bill.tischnr == tischnr), first=True)

        if t_h_bill:

            if t_h_bill.resnr != 0 and t_h_bill.reslinnr == 0:

                mc_guest = db_session.query(Mc_guest).filter(
                        (Mc_guest.gastnr == t_h_bill.resnr) &  (Mc_guest.activeflag)).first()

                if mc_guest:
                    remark = translateExtended ("Membership No:", lvcarea, "") +\
                            " " + mc_guest.cardnum + chr(10)


    p_1342 = get_output(htplogic(1342))

    t_h_bill = query(t_h_bill_list, filters=(lambda t_h_bill :t_h_bill.tischnr == tischnr), first=True)

    if t_h_bill:

        if not p_1342:

            if not tkellner_masterkey:

                if t_h_bill and t_h_bill.kellner_nr != curr_waiter:
                    table_ok = False
                else:

                    t_tisch = query(t_tisch_list, filters=(lambda t_tisch :t_tischnr == tischnr), first=True)

                    if t_tisch:

                        if t_tisch.kellner_nr != 0 and t_tisch.kellner_nr != curr_waiter:
                            table_ok = False

                if not table_ok:
                    msg_str = translateExtended ("This table belongs to other waiter.", lvcarea, "")

                    return generate_output()
    getremark_rsv_table()

    return generate_output()