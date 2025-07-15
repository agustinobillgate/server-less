from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Tisch, H_bill, Kellner, Mc_guest, Htparam, Zimmer, H_bill_line

def prepare_ts_tbplan_1bl(dept:int, curr_waiter:int):
    ci_date = None
    pos1 = 0
    pos2 = 0
    mc_flag = False
    mc_pos1 = 0
    mc_pos2 = 0
    vpos_flag = False
    interval_time = 0
    t_queasy_list = []
    t_tisch_list = []
    t_h_bill_list = []
    t_kellner_list = []
    t_mc_guest_list = []
    t_zimmer_list = []
    t_queasy31_list = []
    t_queasy33_list = []
    s:List[str] = create_empty_list(100,"")
    curr_n:int = 0
    queasy = tisch = h_bill = kellner = mc_guest = htparam = zimmer = h_bill_line = None

    t_queasy = t_queasy33 = t_queasy31 = t_tisch = t_h_bill = t_kellner = t_mc_guest = t_zimmer = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"bcol":int, "fcol":int, "rec_id":int}, {"bcol": 10})
    t_queasy33_list, T_queasy33 = create_model_like(Queasy)
    t_queasy31_list, T_queasy31 = create_model_like(Queasy, {"rec_id":int})
    t_tisch_list, T_tisch = create_model_like(Tisch)
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_kellner_list, T_kellner = create_model_like(Kellner)
    t_mc_guest_list, T_mc_guest = create_model_like(Mc_guest)
    t_zimmer_list, T_zimmer = create_model("T_zimmer", {"zinr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, pos1, pos2, mc_flag, mc_pos1, mc_pos2, vpos_flag, interval_time, t_queasy_list, t_tisch_list, t_h_bill_list, t_kellner_list, t_mc_guest_list, t_zimmer_list, t_queasy31_list, t_queasy33_list, s, curr_n, queasy, tisch, h_bill, kellner, mc_guest, htparam, zimmer, h_bill_line
        nonlocal dept, curr_waiter


        nonlocal t_queasy, t_queasy33, t_queasy31, t_tisch, t_h_bill, t_kellner, t_mc_guest, t_zimmer
        nonlocal t_queasy_list, t_queasy33_list, t_queasy31_list, t_tisch_list, t_h_bill_list, t_kellner_list, t_mc_guest_list, t_zimmer_list
        return {"ci_date": ci_date, "pos1": pos1, "pos2": pos2, "mc_flag": mc_flag, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "vpos_flag": vpos_flag, "interval_time": interval_time, "t-queasy": t_queasy_list, "t-tisch": t_tisch_list, "t-h-bill": t_h_bill_list, "t-kellner": t_kellner_list, "t-mc-guest": t_mc_guest_list, "t-zimmer": t_zimmer_list, "t-queasy31": t_queasy31_list, "t-queasy33": t_queasy33_list}

    def initiate_it():

        nonlocal ci_date, pos1, pos2, mc_flag, mc_pos1, mc_pos2, vpos_flag, interval_time, t_queasy_list, t_tisch_list, t_h_bill_list, t_kellner_list, t_mc_guest_list, t_zimmer_list, t_queasy31_list, t_queasy33_list, s, curr_n, queasy, tisch, h_bill, kellner, mc_guest, htparam, zimmer, h_bill_line
        nonlocal dept, curr_waiter


        nonlocal t_queasy, t_queasy33, t_queasy31, t_tisch, t_h_bill, t_kellner, t_mc_guest, t_zimmer
        nonlocal t_queasy_list, t_queasy33_list, t_queasy31_list, t_tisch_list, t_h_bill_list, t_kellner_list, t_mc_guest_list, t_zimmer_list

        do_it:bool = False
        i:int = 0
        curr_n = 0
        for i in range(1,100 + 1) :
            s[i - 1] = ""

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 31) & (Queasy.number1 == dept) & (Queasy.betriebsnr == 0)).order_by(Queasy.number2).all():

            tisch = db_session.query(Tisch).filter(
                     (Tisch.departement == queasy.number1) & (Tisch.tischnr == queasy.number2)).first()
            do_it = None != tisch

            if do_it:
                curr_n = curr_n + 1
                t_queasy = T_queasy()
                t_queasy_list.append(t_queasy)

                buffer_copy(queasy, t_queasy)
                assign_color(curr_n)
                t_queasy.rec_id = queasy._recid


    def assign_color(i:int):

        nonlocal ci_date, pos1, pos2, mc_flag, mc_pos1, mc_pos2, vpos_flag, interval_time, t_queasy_list, t_tisch_list, t_h_bill_list, t_kellner_list, t_mc_guest_list, t_zimmer_list, t_queasy31_list, t_queasy33_list, s, curr_n, queasy, tisch, h_bill, kellner, mc_guest, htparam, zimmer, h_bill_line
        nonlocal dept, curr_waiter


        nonlocal t_queasy, t_queasy33, t_queasy31, t_tisch, t_h_bill, t_kellner, t_mc_guest, t_zimmer
        nonlocal t_queasy_list, t_queasy33_list, t_queasy31_list, t_tisch_list, t_h_bill_list, t_kellner_list, t_mc_guest_list, t_zimmer_list

        bcol:int = 10
        fcol:int = 0
        zeit:int = 0
        hh1:str = ""
        hh2:str = ""
        hh3:str = ""
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        if queasy.date1 != None:
            zeit = (get_current_date() - queasy.date1) * 86400 + get_current_time_in_seconds() - queasy.number3

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
                     (Qsy.key == 33) & (Qsy.number1 == dept) & (Qsy.number2 == queasy.number2) & (Qsy.date1 == ci_date) & (Qsy.logi3) & (Qsy.hh1 <= Qsy.char1) & (Qsy.hh2 >= Qsy.char1)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == dept) & (Qsy.number2 == queasy.number2) & (Qsy.date1 == ci_date) & (Qsy.logi3) & (Qsy.hh1 >= Qsy.char1) & (Qsy.hh3 <= Qsy.char1)).first()

            if qsy:
                t_queasy.bcol = 1
                t_queasy.fcol = 15

        if t_queasy.bcol == 12:

            h_bill = db_session.query(H_bill).filter(
                     (H_bill.tischnr == to_int(s[i - 1])) & (H_bill.departement == dept) & (H_bill.flag == 0)).first()

            if h_bill:

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line.sysdate.desc(), H_bill_line.zeit.desc()).all():
                    zeit = (get_current_date() - h_bill_line.sysdate) * 86400 + get_current_time_in_seconds() - h_bill_line.zeit

                    if zeit >= 30 * 60:
                        t_queasy.bcol = 0

                    elif zeit >= 15 * 60:
                        t_queasy.bcol = 7
                    break


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 337)).first()
    pos1 = htparam.finteger

    if pos1 == 0:
        pos1 = 1

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 338)).first()
    pos2 = htparam.finteger

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 305) & (Queasy.number1 == 1) & (Queasy.number2 == 1) & (Queasy.number3 == 1) & (Queasy.betriebsnr == dept)).first()

    if queasy:
        interval_time = to_int(queasy.char2)
    initiate_it()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 336)).first()

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 337)).first()
        mc_pos1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 338)).first()
        mc_pos2 = htparam.finteger

    kellner = db_session.query(Kellner).filter(
             (Kellner.kellner_nr == curr_waiter) & (Kellner.departement == dept)).first()

    if kellner:
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        buffer_copy(kellner, t_kellner)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 975)).first()
    vpos_flag = (htparam.finteger == 1)

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == dept)).order_by(Tisch._recid).all():
        t_tisch = T_tisch()
        t_tisch_list.append(t_tisch)

        buffer_copy(tisch, t_tisch)

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.departement == dept) & (H_bill.flag == 0)).order_by(H_bill._recid).all():
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid

    for mc_guest in db_session.query(Mc_guest).filter(
             (Mc_guest.activeflag)).order_by(Mc_guest._recid).all():
        t_mc_guest = T_mc_guest()
        t_mc_guest_list.append(t_mc_guest)

        buffer_copy(mc_guest, t_mc_guest)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        t_zimmer.zinr = zimmer.zinr

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 33) & (Queasy.number1 == dept) & (Queasy.date1 == ci_date) & (Queasy.logi3)).order_by(Queasy._recid).all():
        t_queasy33 = T_queasy33()
        t_queasy33_list.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 31) & (Queasy.number1 == dept) & (Queasy.betriebsnr == 0)).order_by(Queasy.number2).all():
        curr_n = curr_n + 1
        t_queasy31 = T_queasy31()
        t_queasy31_list.append(t_queasy31)

        buffer_copy(queasy, t_queasy31)
        t_queasy31.rec_id = queasy._recid

    return generate_output()