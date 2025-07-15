#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from models import H_bill, Tisch, Queasy, Htparam, Res_line, Mc_guest, Guest, Bill

t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
t_tisch_data, T_tisch = create_model_like(Tisch)

def ts_tbplan_check_table_webbl(pvilanguage:int, resnr:int, reslinnr:int, tischnr:int, curr_waiter:int, tkellner_masterkey:bool, dept_no:int, t_h_bill_data:[T_h_bill], t_tisch_data:[T_tisch]):

    prepare_cache ([Htparam, Res_line, Guest, Bill])

    rmno = ""
    remark = ""
    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    recid_bill = 0
    avail_bill = False
    resline = False
    msg_str = ""
    lvcarea:string = "TS-tbplan"
    p_1342:bool = False
    table_ok:bool = True
    i:int = 0
    str:string = ""
    child_age:string = ""
    ci_date:date = None
    h_bill = tisch = queasy = htparam = res_line = mc_guest = guest = bill = None

    t_h_bill = t_tisch = t_queasy33 = t_queasy31 = None

    t_queasy33_data, T_queasy33 = create_model_like(Queasy)
    t_queasy31_data, T_queasy31 = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmno, remark, klimit, ksaldo, recid_bill, avail_bill, resline, msg_str, lvcarea, p_1342, table_ok, i, str, child_age, ci_date, h_bill, tisch, queasy, htparam, res_line, mc_guest, guest, bill
        nonlocal pvilanguage, resnr, reslinnr, tischnr, curr_waiter, tkellner_masterkey, dept_no


        nonlocal t_h_bill, t_tisch, t_queasy33, t_queasy31
        nonlocal t_queasy33_data, t_queasy31_data

        return {"rmno": rmno, "remark": remark, "klimit": klimit, "ksaldo": ksaldo, "recid_bill": recid_bill, "avail_bill": avail_bill, "resline": resline, "msg_str": msg_str}

    def check_creditlimit():

        nonlocal rmno, remark, klimit, ksaldo, recid_bill, avail_bill, resline, msg_str, lvcarea, p_1342, table_ok, i, str, child_age, ci_date, h_bill, tisch, queasy, htparam, res_line, mc_guest, guest, bill
        nonlocal pvilanguage, resnr, reslinnr, tischnr, curr_waiter, tkellner_masterkey, dept_no


        nonlocal t_h_bill, t_tisch, t_queasy33, t_queasy31
        nonlocal t_queasy33_data, t_queasy31_data

        answer:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)],"activeflag": [(eq, True)]})

        if mc_guest:
            remark = translateExtended ("Membership No:", lvcarea, "") +\
                " " + mc_guest.cardnum + chr_unicode(10)

        if guest.kreditlimit != 0:
            klimit =  to_decimal(guest.kreditlimit)
        else:

            if htparam.fdecimal != 0:
                klimit =  to_decimal(htparam.fdecimal)
            else:
                klimit =  to_decimal(htparam.finteger)
        ksaldo =  to_decimal("0")

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line.zinr)]})

        if bill:
            recid_bill = bill._recid
            avail_bill = True
            ksaldo =  to_decimal(bill.saldo)
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 5) == ("ChAge").lower() :
                child_age = substring(str, 5)

        if child_age != "":
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " " + "(" + child_age + ")" + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk
        else:
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk


    def getremark_rsv_table():

        nonlocal rmno, remark, klimit, ksaldo, recid_bill, avail_bill, resline, msg_str, lvcarea, p_1342, table_ok, i, str, child_age, ci_date, h_bill, tisch, queasy, htparam, res_line, mc_guest, guest, bill
        nonlocal pvilanguage, resnr, reslinnr, tischnr, curr_waiter, tkellner_masterkey, dept_no


        nonlocal t_h_bill, t_tisch, t_queasy33, t_queasy31
        nonlocal t_queasy33_data, t_queasy31_data

        hh1:string = ""
        hh2:string = ""
        hh3:string = ""
        zeit:int = 0
        table_occupied:bool = False

        t_queasy31 = query(t_queasy31_data, filters=(lambda t_queasy31: t_queasy31.number2 == tischnr), first=True)
        table_occupied = None != t_queasy31 and t_queasy31.date1 != None
        hh1 = to_string(get_current_time_in_seconds(), "HH:MM")
        hh1 = substring(hh1, 0, 2) + substring(hh1, 3, 2)
        hh2 = to_string(to_int(substring(hh1, 0, 2)) + 2, "99") + substring(hh1, 2, 2)
        hh3 = to_string(get_current_time_in_seconds() - 1800, "HH:MM")
        hh3 = substring(hh3, 0, 2) + substring(hh3, 3, 2)

        t_queasy33 = query(t_queasy33_data, filters=(lambda t_queasy33: t_queasy33.number2 == tischnr and hh1 <= t_queasy33.char1 and hh2 >= t_queasy33.char1), first=True)

        if not t_queasy33 and not table_occupied:

            t_queasy33 = query(t_queasy33_data, filters=(lambda t_queasy33: t_queasy33.number2 == tischnr and hh1 >= t_queasy33.char1 and hh3 <= t_queasy33.char1), first=True)

        if t_queasy33:
            zeit = to_int(substring(t_queasy33.char1, 0, 2)) * 3600 + to_int(substring(t_queasy33.char1, 2, 2)) * 60

            if zeit > get_current_time_in_seconds():
                remark = remark + entry(0, t_queasy33.char2, "&&") + " - " + trim(substring(t_queasy33.char1, 9)) + chr_unicode(10) + to_string(substring(t_queasy33.char1, 0, 4) , "99:99") + " - " + to_string(substring(t_queasy33.char1, 4, 4) , "99:99") + chr_unicode(10) + translateExtended ("Pax:", lvcarea, "") + " " + to_string(t_queasy33.number3) + chr_unicode(10) + translateExtended ("Remain Time:", lvcarea, "") + " " + to_string(zeit - get_current_time_in_seconds(), "HH:MM")
            else:
                remark = remark + entry(0, t_queasy33.char2, "&&") + " - " + trim(substring(t_queasy33.char1, 9)) + chr_unicode(10) + to_string(substring(t_queasy33.char1, 0, 4) , "99:99") + " - " + to_string(substring(t_queasy33.char1, 4, 4) , "99:99") + chr_unicode(10) + translateExtended ("Pax:", lvcarea, "") + " " + to_string(t_queasy33.number3) + chr_unicode(10) + translateExtended ("Current Time:", lvcarea, "") + " " + to_string(get_current_time_in_seconds(), "HH:MM")

            if trim(entry(1, t_queasy33.char3, ";")) != "":
                remark = remark + chr_unicode(10) + translateExtended ("remark:", lvcarea, "") + " " + trim(entry(1, t_queasy33.char3, ";"))

            if t_queasy33.deci1 != 0:
                remark = remark + chr_unicode(10) + translateExtended ("Deposit:", lvcarea, "") + " " + trim(to_string(t_queasy33.deci1, "->>>,>>>,>>>,>>9.99"))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 33) & (Queasy.number1 == dept_no) & (Queasy.date1 == ci_date) & (Queasy.logi3)).order_by(Queasy._recid).all():
        t_queasy33 = T_queasy33()
        t_queasy33_data.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 31) & (Queasy.number1 == dept_no) & (Queasy.betriebsnr == 0)).order_by(Queasy.number2).all():
        t_queasy31 = T_queasy31()
        t_queasy31_data.append(t_queasy31)

        buffer_copy(queasy, t_queasy31)
        t_queasy31.rec_id = queasy._recid

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if res_line:
        resline = True
        check_creditlimit()
        rmno = res_line.zinr
    else:

        t_h_bill = query(t_h_bill_data, filters=(lambda t_h_bill: t_h_bill.tischnr == tischnr), first=True)

        if t_h_bill:

            if t_h_bill.resnr != 0 and t_h_bill.reslinnr == 0:

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, t_h_bill.resnr)],"activeflag": [(eq, True)]})

                if mc_guest:
                    remark = translateExtended ("Membership No:", lvcarea, "") +\
                            " " + mc_guest.cardnum + chr_unicode(10)


    p_1342 = get_output(htplogic(1342))

    t_h_bill = query(t_h_bill_data, filters=(lambda t_h_bill: t_h_bill.tischnr == tischnr), first=True)

    if t_h_bill:

        if not p_1342:

            if not tkellner_masterkey:

                if t_h_bill and t_h_bill.kellner_nr != curr_waiter:
                    table_ok = False
                else:

                    t_tisch = query(t_tisch_data, filters=(lambda t_tisch: t_tisch.tischnr == tischnr), first=True)

                    if t_tisch:

                        if t_tisch.kellner_nr != 0 and t_tisch.kellner_nr != curr_waiter:
                            table_ok = False

                if not table_ok:
                    msg_str = translateExtended ("This table belongs to other waiter.", lvcarea, "")

                    return generate_output()
    getremark_rsv_table()

    return generate_output()