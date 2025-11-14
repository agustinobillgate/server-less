#using conversion tools version: 1.0.0.119

# ===============================
# Rulita, 14-11-2025 | 9FA58C
# - Update Convertion tiket Hdesk 
# ===============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Tisch, H_bill, Kellner, Mc_guest, Htparam, Zimmer, H_bill_line

def prepare_ts_tbplan2_webbl(dept:int, location:int, curr_waiter:int):

    prepare_cache ([H_bill, Htparam, Zimmer, H_bill_line])

    ci_date = None
    pos1 = 0
    pos2 = 0
    mc_flag = False
    mc_pos1 = 0
    mc_pos2 = 0
    vpos_flag = False
    t_queasy_data = []
    t_tisch_data = []
    t_h_bill_data = []
    t_kellner_data = []
    t_mc_guest_data = []
    t_zimmer_data = []
    t_queasy31_data = []
    t_queasy33_data = []
    s:List[string] = create_empty_list(100,"")
    curr_n:int = 0
    split_count:int = 0
    queasy = tisch = h_bill = kellner = mc_guest = htparam = zimmer = h_bill_line = None

    t_queasy = t_queasy33 = t_queasy31 = t_tisch = t_h_bill = t_kellner = t_mc_guest = t_zimmer = hbill_buf = None

    t_queasy_data, T_queasy = create_model_like(Queasy, {"bcol":int, "fcol":int, "rec_id":int, "billprint_flag":bool, "splitbill_flag":bool}, {"bcol": 10})
    t_queasy33_data, T_queasy33 = create_model_like(Queasy)
    t_queasy31_data, T_queasy31 = create_model_like(Queasy, {"rec_id":int})
    t_tisch_data, T_tisch = create_model_like(Tisch)
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_kellner_data, T_kellner = create_model_like(Kellner)
    t_mc_guest_data, T_mc_guest = create_model_like(Mc_guest)
    t_zimmer_data, T_zimmer = create_model("T_zimmer", {"zinr":string})

    Hbill_buf = create_buffer("Hbill_buf",H_bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, pos1, pos2, mc_flag, mc_pos1, mc_pos2, vpos_flag, t_queasy_data, t_tisch_data, t_h_bill_data, t_kellner_data, t_mc_guest_data, t_zimmer_data, t_queasy31_data, t_queasy33_data, s, curr_n, split_count, queasy, tisch, h_bill, kellner, mc_guest, htparam, zimmer, h_bill_line
        nonlocal dept, location, curr_waiter
        nonlocal hbill_buf


        nonlocal t_queasy, t_queasy33, t_queasy31, t_tisch, t_h_bill, t_kellner, t_mc_guest, t_zimmer, hbill_buf
        nonlocal t_queasy_data, t_queasy33_data, t_queasy31_data, t_tisch_data, t_h_bill_data, t_kellner_data, t_mc_guest_data, t_zimmer_data

        return {"ci_date": ci_date, "pos1": pos1, "pos2": pos2, "mc_flag": mc_flag, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "vpos_flag": vpos_flag, "t-queasy": t_queasy_data, "t-tisch": t_tisch_data, "t-h-bill": t_h_bill_data, "t-kellner": t_kellner_data, "t-mc-guest": t_mc_guest_data, "t-zimmer": t_zimmer_data, "t-queasy31": t_queasy31_data, "t-queasy33": t_queasy33_data}

    def initiate_it():

        nonlocal ci_date, pos1, pos2, mc_flag, mc_pos1, mc_pos2, vpos_flag, t_queasy_data, t_tisch_data, t_h_bill_data, t_kellner_data, t_mc_guest_data, t_zimmer_data, t_queasy31_data, t_queasy33_data, s, curr_n, split_count, queasy, tisch, h_bill, kellner, mc_guest, htparam, zimmer, h_bill_line
        nonlocal dept, location, curr_waiter
        nonlocal hbill_buf


        nonlocal t_queasy, t_queasy33, t_queasy31, t_tisch, t_h_bill, t_kellner, t_mc_guest, t_zimmer, hbill_buf
        nonlocal t_queasy_data, t_queasy33_data, t_queasy31_data, t_tisch_data, t_h_bill_data, t_kellner_data, t_mc_guest_data, t_zimmer_data

        do_it:bool = False
        i:int = 0
        bill_time:int = 0
        bill_datum:date = None
        qsy_31 = None
        Qsy_31 =  create_buffer("Qsy_31",Queasy)
        curr_n = 0
        for i in range(1,100 + 1) :
            s[i - 1] = ""

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 31) & (Queasy.number1 == dept) & (Queasy.betriebsnr == 0) & (Queasy.deci3 == location)).order_by(Queasy.number2).all():

            tisch = get_cache (Tisch, {"departement": [(eq, queasy.number1)],"betriebsnr": [(eq, queasy.deci3)],"tischnr": [(eq, queasy.number2)]})
            do_it = None != tisch

            if do_it:
                curr_n = curr_n + 1
                t_queasy = T_queasy()
                t_queasy_data.append(t_queasy)

                buffer_copy(queasy, t_queasy)
                assign_color(curr_n)
                t_queasy.rec_id = queasy._recid

                hbill_buf = get_cache (H_bill, {"tischnr": [(eq, tisch.tischnr)],"departement": [(eq, tisch.departement)],"flag": [(eq, 0)]})

                if hbill_buf:
                    t_queasy.billprint_flag = logical(hbill_buf.rgdruck)
                    split_count = 0

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == hbill_buf.rechnr) & (H_bill_line.departement == hbill_buf.departement) & (H_bill_line.waehrungsnr != 0)).order_by(H_bill_line._recid).all():
                        split_count = split_count + 1

                        if split_count >= 1:
                            t_queasy.splitbill_flag = True
                            break

                    for h_bill_line in db_session.query(H_bill_line).filter(
                             (H_bill_line.rechnr == hbill_buf.rechnr) & (H_bill_line.departement == hbill_buf.departement)).order_by(H_bill_line.bill_datum, H_bill_line.zeit).all():
                        bill_time = h_bill_line.zeit
                        bill_datum = h_bill_line.bill_datum
                        break

                    if queasy.number3 == 0 and queasy.date1 == None:

                        qsy_31 = db_session.query(Qsy_31).filter(
                                 (Qsy_31._recid == queasy._recid)).first()

                        if qsy_31:
                            qsy_31.number3 = bill_time
                            qsy_31.date1 = bill_datum


                            pass
                            pass
                            assign_color(curr_n)
                else:

                    if queasy.number3 != 0 and queasy.date1 != None:

                        qsy_31 = db_session.query(Qsy_31).filter(
                                 (Qsy_31._recid == queasy._recid)).first()

                        if qsy_31:
                            qsy_31.number3 = 0
                            qsy_31.date1 = None


                            pass
                            pass
                            t_queasy.bcol = 10
                            t_queasy.fcol = 0


    def assign_color(i:int):

        nonlocal ci_date, pos1, pos2, mc_flag, mc_pos1, mc_pos2, vpos_flag, t_queasy_data, t_tisch_data, t_h_bill_data, t_kellner_data, t_mc_guest_data, t_zimmer_data, t_queasy31_data, t_queasy33_data, s, curr_n, split_count, queasy, tisch, h_bill, kellner, mc_guest, htparam, zimmer, h_bill_line
        nonlocal dept, location, curr_waiter
        nonlocal hbill_buf


        nonlocal t_queasy, t_queasy33, t_queasy31, t_tisch, t_h_bill, t_kellner, t_mc_guest, t_zimmer, hbill_buf
        nonlocal t_queasy_data, t_queasy33_data, t_queasy31_data, t_tisch_data, t_h_bill_data, t_kellner_data, t_mc_guest_data, t_zimmer_data

        bcol:int = 10
        fcol:int = 0
        zeit:int = 0
        hh1:string = ""
        hh2:string = ""
        hh3:string = ""
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        if queasy.date1 != None:
            zeit = ((get_current_date() - queasy.date1).days) * 86400 + get_current_time_in_seconds() - queasy.number3

            if zeit > 0 and zeit <= 1800:
                t_queasy.bcol = 14

            elif zeit > 1800 and zeit <= 3600:
                t_queasy.bcol = 4
                t_queasy.fcol = 15

            elif zeit > 3600:
                t_queasy.bcol = 12
                t_queasy.fcol = 15


        else:
            hh1 = to_string(get_current_time_in_seconds(), "HH:MM")
            hh1 = substring(hh1, 0, 2) + substring(hh1, 3, 2)
            hh2 = to_string(to_int(substring(hh1, 0, 2)) + 2, "99") + substring(hh1, 2, 2)
            hh3 = to_string(get_current_time_in_seconds() - 1800, "HH:MM")
            hh3 = substring(hh3, 0, 2) + substring(hh3, 3, 2)

            qsy = db_session.query(Qsy).filter(
                     (Qsy.key == 33) & (Qsy.number1 == dept) & (Qsy.number2 == queasy.number2) & (Qsy.date1 == ci_date) & (Qsy.logi3) & (hh1 <= Qsy.char1) & (hh2 >= Qsy.char1)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == dept) & (Qsy.number2 == queasy.number2) & (Qsy.date1 == ci_date) & (Qsy.logi3) & (hh1 >= Qsy.char1) & (hh3 <= Qsy.char1)).first()

            if qsy:
                t_queasy.bcol = 1
                t_queasy.fcol = 15

        if t_queasy.bcol == 12:

            h_bill = get_cache (H_bill, {"tischnr": [(eq, to_int(s[i - 1]))],"departement": [(eq, dept)],"flag": [(eq, 0)]})

            if h_bill:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).yield_per(100):
                    zeit = ((get_current_date() - h_bill_line.sysdate).days) * 86400 + get_current_time_in_seconds() - h_bill_line.zeit

                    if zeit >= 30 * 60:
                        t_queasy.bcol = 0

                    elif zeit >= 15 * 60:
                        t_queasy.bcol = 7
                    break


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
    pos1 = htparam.finteger

    if pos1 == 0:
        pos1 = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
    pos2 = htparam.finteger
    initiate_it()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 336)]})

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
        mc_pos1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
        mc_pos2 = htparam.finteger

    kellner = get_cache (Kellner, {"kellner_nr": [(eq, curr_waiter)],"departement": [(eq, dept)]})

    if kellner:
        t_kellner = T_kellner()
        t_kellner_data.append(t_kellner)

        buffer_copy(kellner, t_kellner)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})
    vpos_flag = (htparam.finteger == 1)

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == dept) & (Tisch.betriebsnr == location)).order_by(Tisch._recid).all():
        t_tisch = T_tisch()
        t_tisch_data.append(t_tisch)

        buffer_copy(tisch, t_tisch)

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.departement == dept) & (H_bill.flag == 0)).order_by(H_bill._recid).all():
        t_h_bill = T_h_bill()
        t_h_bill_data.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        t_zimmer.zinr = zimmer.zinr

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 33) & (Queasy.number1 == dept) & (Queasy.date1 == ci_date) & (Queasy.logi3)).order_by(Queasy._recid).all():
        t_queasy33 = T_queasy33()
        t_queasy33_data.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 31) & (Queasy.number1 == dept) & (Queasy.betriebsnr == 0) & (Queasy.deci3 == location)).order_by(Queasy.number2).all():
        curr_n = curr_n + 1
        t_queasy31 = T_queasy31()
        t_queasy31_data.append(t_queasy31)

        buffer_copy(queasy, t_queasy31)
        t_queasy31.rec_id = queasy._recid

    return generate_output()