from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from sqlalchemy import func
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpdate import htpdate
import re
from functions.mk_resline_query_q1bl import mk_resline_query_q1bl
from functions.check_complimentbl import check_complimentbl
from functions.intevent_1 import intevent_1
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from models import Res_line, History, Zimkateg, Ratecode, Zimmer, Htparam, Bediener, Master, Guest, Reslin_queasy, Reservation, Kontline, Gentable, Outorder, Queasy, Arrangement, Nation, Guest_pr, Pricecod, Prmarket, Fixleist, Paramtext, Waehrung, Katpreis

def prepare_resline_1bl(pvilanguage:int, res_mode:str, session_date:str, user_init:str, inp_gastnr:int, inp_resnr:int, inp_reslinnr:int, rate_readonly:bool, qci_zinr:str, res_dynarate:[Res_dynarate]):
    msg_str = ""
    error_flag = False
    record_use = False
    init_time = 0
    init_date = None
    avail_gdpr = False
    f_resline_list = []
    curr_resline_list = []
    reslin_list_list = []
    reschanged_list_list = []
    t_history_list = []
    rline_list_list = []
    weekdays:[str] = ["", "", "", "", "", "", "", "", ""]
    i:int = 0
    str:str = ""
    loopi:int = 0
    loopj:int = 0
    str1:str = ""
    foreign_nr:int = 0
    tokcounter:int = 0
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    rcode:str = ""
    prevcode:str = ""
    do_it:bool = False
    flag_ok:bool = False
    dayuse_flag:bool = False
    split_modify:bool = False
    logic_p1109:bool = False
    priscilla_active:bool = True
    lvcarea:str = "mk_resline"
    new_reslinnr:int = 1
    curr_time:int = 0
    res_line = history = zimkateg = ratecode = zimmer = htparam = bediener = master = guest = reslin_queasy = reservation = kontline = gentable = outorder = queasy = arrangement = nation = guest_pr = pricecod = prmarket = fixleist = paramtext = waehrung = katpreis = None

    rline_list = reslin_list = curr_resline = t_history = currency_list = res_dynarate = reschanged_list = f_resline = resline = resbuff = zimkateg1 = rbuff = qci_zimmer = qsy = m_queasy = m_leist = resmember = rline = genbuff = bline = waehrung1 = gbuff = w1 = None

    rline_list_list, Rline_list = create_model_like(Res_line, {"res_char":str, "rsvname":str, "kurzbez":str, "status_str":str})
    reslin_list_list, Reslin_list = create_model_like(Res_line)
    curr_resline_list, Curr_resline = create_model_like(Res_line)
    t_history_list, T_history = create_model_like(History)
    currency_list_list, Currency_list = create_model("Currency_list", {"wabkurz":str})
    res_dynarate_list, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":decimal, "rmcat":str, "argt":str, "prcode":str, "rcode":str, "markno":int, "setup":int, "adult":int, "child":int})
    reschanged_list_list, Reschanged_list = create_model("Reschanged_list", {"reslinnr":int})
    f_resline_list, F_resline = create_model("F_resline", {"guestname":str, "curr_segm":str, "curr_source":str, "curr_arg":str, "c_purpose":str, "contcode":str, "origcontcode":str, "tip_code":str, "voucher":str, "instruct_str":str, "arrday":str, "depday":str, "flight1":str, "flight2":str, "eta":str, "etd":str, "allot_str":str, "allot_tooltip":str, "rate_zikat":str, "zikatstr":str, "currency":str, "c_setup":str, "memo_zinr":str, "billname":str, "billadress":str, "billcity":str, "billland":str, "name_editor":str, "hist_comment":str, "main_resname":str, "prog_str":str, "rsv_tooltip":str, "rate_tooltip":str, "rline_bemerk":str, "res_bemerk":str, "child_age":str, "combo_code":str, "reslinnr":int, "bill_instruct":int, "kontignr":int, "zimmeranz":int, "comchild":int, "price_decimal":int, "res_status":int, "karteityp":int, "guestnr":int, "tot_qty":int, "zahlungsart":int, "marknr":int, "i_purpose":int, "local_nr":int, "foreign_nr":int, "l_night":int, "six_pm":int, "accompany_gastnr":int, "accompany_gastnr2":int, "accompany_gastnr3":int, "ci_date":date, "billdate":date, "bookdate":date, "l_ankunft":date, "l_abreise":date, "earlyci":bool, "master_exist":bool, "master_active":bool, "pickup_flag":bool, "drop_flag":bool, "enable_frate":bool, "ebdisc_flag":bool, "kbdisc_flag":bool, "restricted":bool, "enable_ebdisc":bool, "enable_kbdisc":bool, "new_contrate":bool, "foreign_rate":bool, "gentable":bool, "offmarket":bool, "grpflag":bool, "sharer":bool, "fixed_rate":bool, "enable_disc":bool, "oral_flag":bool, "param472":bool, "wci_flag":str, "gdpr_flag":str}, {"zimmeranz": 1, "bookdate": None, "l_ankunft": None, "l_abreise": None})

    Resline = Res_line
    Resbuff = Res_line
    Zimkateg1 = Zimkateg
    Rbuff = Ratecode
    Qci_zimmer = Zimmer
    Qsy = Queasy
    M_queasy = Reslin_queasy
    M_leist = Fixleist
    Resmember = Res_line
    Rline = Res_line
    Genbuff = Gentable
    Bline = Res_line
    Waehrung1 = Waehrung
    Gbuff = Guest
    W1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list
        return {"msg_str": msg_str, "error_flag": error_flag, "record_use": record_use, "init_time": init_time, "init_date": init_date, "avail_gdpr": avail_gdpr, "f-resline": f_resline_list, "curr-resline": curr_resline_list, "reslin-list": reslin_list_list, "reschanged-list": reschanged_list_list, "t-history": t_history_list, "rline-list": rline_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        rate:decimal = 0

        if erwachs >= 1 and erwachs <= 4:
            rate = rate + katpreis.perspreis[erwachs - 1]
        rate = rate + kind1 * katpreis.kindpreis[0] + kind2 * katpreis.kindpreis[1]
        return rate

    def fill_flightnr():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list


        f_resline.flight1 = substring(res_line.flight_nr, 0, 6)
        f_resline.eta = substring(res_line.flight_nr, 6, 5)
        f_resline.flight2 = substring(res_line.flight_nr, 11, 6)
        f_resline.etd = substring(res_line.flight_nr, 17, 5)

        if trim(f_resline.eta) == "":
            f_resline.eta = "0000"

        if trim(f_resline.etd) == "":
            f_resline.etd = "0000"

    def split_resline():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        i:int = 0
        anz:int = 0
        reihe:int = 0
        zeit:int = 0
        max_comp:int = 0
        com_rm:int = 0
        its_wrong:bool = False
        msg_str:str = ""
        pswd_str:str = ""
        M_queasy = Reslin_queasy
        M_leist = Fixleist
        Resmember = Res_line
        Rline = Res_line
        Genbuff = Gentable
        Bline = Res_line
        zeit = get_current_time_in_seconds() - 2

        bline = db_session.query(Bline).filter(
                (Bline.resnr == inp_resnr) &  (Bline.reslinnr == inp_reslinnr)).first()

        if bline:
            its_wrong, com_rm, max_comp, pswd_str, msg_str = get_output(check_complimentbl(pvilanguage, bline.resnr, bline.reslinnr, bline.gastnr, bline.ankunft, f_resline.marknr, bline.zikatnr, bline.arrangement, bline.zimmeranz, bline.zipreis))

        for rline in db_session.query(Rline).filter(
                (Rline.resnr == inp_resnr) &  (Rline.active_flag <= 1)).all():

            res_line = db_session.query(Res_line).filter(
                    (Res_line._recid == rline._recid)).first()

            if reihe == 0:
                reihe = res_line.reslinnr

            if priscilla_active:

                if res_line.zimmeranz > 1:
                    get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

            gentable = db_session.query(Gentable).filter(
                    (func.lower(Gentable.key) == "reservation") &  (Gentable.number1 == res_line.resnr) &  (Gentable.number2 == res_line.reslinnr)).first()
            zeit = zeit + 2
            i = 2


            while i <= res_line.zimmeranz:
                resmember = Resmember()
                db_session.add(resmember)

                resmember.zimmeranz = 1
                resmember.reslinnr = f_resline.reslinnr
                resmember.resname = f_resline.main_resname


                buffer_copy(res_line, resmember,except_fields=["zimmeranz","reslinnr","resname"])

                if priscilla_active:
                    get_output(intevent_1(13, "", "Priscilla", resmember.resnr, resmember.reslinnr))

                if com_rm != 0:
                    resmember.zipreis = 0
                    com_rm = com_rm - 1


                m_queasy = M_queasy()
                db_session.add(m_queasy)

                m_queasy.key = "ResChanges"
                m_queasy.resnr = res_line.resnr
                m_queasy.reslinnr = f_resline.reslinnr
                m_queasy.date2 = get_current_date()
                m_queasy.number2 = zeit


                m_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string("Splitted Reservation") + ";"


                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "fargt_line") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                    m_queasy = M_queasy()
                    db_session.add(m_queasy)

                    m_queasy.reslinnr = f_resline.reslinnr


                    buffer_copy(reslin_queasy, m_queasy,except_fields=["reslinnr"])


                if resmember.zipreis != 0:

                    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).all():
                        m_queasy = M_queasy()
                        db_session.add(m_queasy)

                        m_queasy.reslinnr = f_resline.reslinnr


                        buffer_copy(reslin_queasy, m_queasy,except_fields=["reslinnr"])


                    for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                        m_leist = M_leist()
                        db_session.add(m_leist)

                        m_leist.reslinnr = f_resline.reslinnr


                        buffer_copy(fixleist, m_leist,except_fields=["reslinnr"])


                if gentable:
                    genbuff = Genbuff()
                    db_session.add(genbuff)

                    genbuff.number2 = f_resline.reslinnr


                    buffer_copy(gentable, genbuff,except_fields=["number2"])


                resmember = db_session.query(Resmember).first()
                f_resline.reslinnr = f_resline.reslinnr + 1
                i = i + 1
            res_line.zimmeranz = 1

            res_line = db_session.query(Res_line).first()

        f_resline.reslinnr = reihe

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == reihe)).first()

    def check_bedsetup():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        if reslin_list.setup != 0:

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == reslin_list.setup)).first()

            if not zimmer:
                reslin_list.setup = 0
                f_resline.c_setup = ""

                return
            else:

                paramtext = db_session.query(Paramtext).filter(
                        (Paramtext.txtnr == (9200 + reslin_list.setup))).first()
                f_resline.c_setup = substring(paramtext.notes, 0, 1)


        else:
            reslin_list.setup = 0
            f_resline.c_setup = ""


            check_bedsetup1()

    def disp_allotment():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        if reslin_list.kontignr == 0:

            return

        if reslin_list.kontignr > 0:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.kontignr == reslin_list.kontignr) &  (Kontline.kontstat == 1)).first()
        else:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.kontignr == - reslin_list.kontignr) &  (Kontline.betriebsnr == 1) &  (Kontline.kontstat == 1)).first()

        if kontline:
            f_resline.kontignr = reslin_list.kontignr
            f_resline.allot_str = kontline.kontcode

    def get_currency():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        curr_wabnr:int = 0
        guest_currency:int = 0
        found:bool = False
        Waehrung1 = Waehrung
        Rline = Res_line
        Gbuff = Guest

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 152)).first()

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.wabkurz == htparam.fchar)).first()

        if not waehrung1:
            msg_str = translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "") + chr(10)

            return
        f_resline.local_nr = waehrung1.waehrungsnr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung1 = db_session.query(Waehrung1).filter(
                (Waehrung1.wabkurz == htparam.fchar)).first()

        if (not waehrung1) and f_resline.foreign_rate:
            msg_str = translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "") + chr(10)

            return

        if waehrung1:
            foreign_nr = waehrung1.waehrungsnr

        gbuff = db_session.query(Gbuff).filter(
                (Gbuff.gastnr == inp_gastnr)).first()

        if gbuff.notizen[2] != "":

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.wabkurz == gbuff.notizen[2])).first()

            if waehrung1:
                guest_currency = waehrung1.waehrungsnr

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr)).first()

        if reslin_queasy:

            for waehrung1 in db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr != reslin_list.betriebsnr) &  (Waehrung1.betriebsnr == 0)).all():
                f_resline.currency = f_resline.currency + waehrung1.wabkurz + ";"

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == reslin_list.betriebsnr)).first()

            if waehrung1:
                f_resline.currency = waehrung1.wabkurz + ";" + f_resline.currency

            return

        currency_list = query(currency_list_list, first=True)

        if currency_list:

            for currency_list in query(currency_list_list):
                f_resline.currency = f_resline.currency + currency_list.wabkurz + ";"

            return

        if reslin_list.betriebsnr == 0 or f_resline.marknr != 0:

            if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci" or f_resline.marknr != 0):


                if f_resline.contcode != "":

                    guest_pr = db_session.query(Guest_pr).filter(
                            (Guest_pr.CODE == f_resline.contcode)).first()

                if not guest_pr:

                    guest_pr = db_session.query(Guest_pr).filter(
                            (Guest_pr.gastnr == inp_gastnr)).first()

                if guest_pr:

                    if f_resline.marknr == 0:

                        ratecode = db_session.query(Ratecode).filter(
                                (Ratecode.CODE == guest_pr.CODE)).first()

                        if ratecode:
                            f_resline.marknr = ratecode.marknr

                    if f_resline.marknr != 0:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 18) &  (Queasy.number1 == f_resline.marknr)).first()

                        if not queasy or (queasy and queasy.char3 == ""):

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()
                    else:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()

                    if queasy:

                        if queasy.key == 18:

                            waehrung1 = db_session.query(Waehrung1).filter(
                                    (Waehrung1.wabkurz == queasy.char3)).first()
                        else:

                            waehrung1 = db_session.query(Waehrung1).filter(
                                    (Waehrung1.waehrungsnr == queasy.number1)).first()

                        if waehrung1:
                            found = True
                            curr_wabnr = waehrung1.waehrungsnr

                            rline = db_session.query(Rline).filter(
                                    (Rline.resnr == inp_resnr) &  (Rline.reslinnr == inp_reslinnr)).first()

                            if rline:
                                rline.betriebsnr = waehrung1.waehrungsnr

                                rline = db_session.query(Rline).first()
                            reslin_list.betriebsnr = waehrung1.waehrungsnr

            if not found:

                if reslin_list.adrflag  or not f_resline.foreign_rate:
                    curr_wabnr = f_resline.local_nr
                    reslin_list.betriebsnr = f_resline.local_nr

                    waehrung1 = db_session.query(Waehrung1).filter(
                            (Waehrung1.waehrungsnr == f_resline.local_nr)).first()
                else:

                    if guest_currency != 0:
                        curr_wabnr = guest_currency
                    else:
                        curr_wabnr = foreign_nr
                    reslin_list.betriebsnr = curr_wabnr

                for waehrung1 in db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr != curr_wabnr) &  (Waehrung1.betriebsnr == 0)).all():
                    f_resline.currency = f_resline.currency + waehrung1.wabkurz + ";"

                waehrung1 = db_session.query(Waehrung1).filter(
                        (Waehrung1.waehrungsnr == curr_wabnr)).first()
        else:

            for waehrung1 in db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr != reslin_list.betriebsnr) &  (Waehrung1.betriebsnr == 0)).all():
                f_resline.currency = f_resline.currency + waehrung1.wabkurz + ";"

            waehrung1 = db_session.query(Waehrung1).filter(
                    (Waehrung1.waehrungsnr == reslin_list.betriebsnr)).first()
        f_resline.currency = waehrung1.wabkurz + ";" + f_resline.currency

    def disp_history():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        i_anzahl:int = 0

        for history in db_session.query(History).filter(
                (History.gastnr == reslin_list.gastnrmember)).all():
            i_anzahl = i_anzahl + 1
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)

            if i_anzahl == 4:

                return

    def set_roomrate(direct_change:bool):

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        datum:date = None
        add_it:bool = False
        answer:bool = False
        curr_rate:decimal = 0
        exchg_rate:decimal = 1
        qty:int = 0
        i:int = 0
        argt_defined:bool = False
        current_rate:decimal = 0
        exrate1:decimal = 1
        ex2:decimal = 1
        child1:int = 0
        curr_zikatnr:int = 0
        rate_found:bool = False
        prgrate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        W1 = Waehrung

        if not arrangement:

            return

        if res_mode.lower()  != "new" and res_mode.lower()  != "insert" and res_mode.lower()  != "qci":

            if not direct_change and reslin_list.zipreis != 0:

                return

            if substring(bediener.permission, 42, 1) < "2":

                return
        current_rate = reslin_list.zipreis


        datum = reslin_list.ankunft

        if res_mode.lower()  == "inhouse":
            datum = f_resline.ci_date

        if res_mode.lower()  == "inhouse" and reslin_list.resstatus == 8:

            if reslin_list.ankunft == reslin_list.abreise:
                datum = reslin_list.abreise


            else:
                datum = reslin_list.abreise - 1

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == inp_gastnr)).first()

        if reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0:
            reslin_list.zipreis = 0
        else:

            if f_resline.fixed_rate:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr) &  (Reslin_queasy.datum >= Reslin_queasy.date1) &  (Reslin_queasy.datum <= Reslin_queasy.date2)).first()

                if reslin_queasy:
                    reslin_list.zipreis = reslin_queasy.deci1
                    f_resline.rate_tooltip = ""
                    rate_found = True

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == guest.gastnr)).first()

            if guest_pr and not rate_found:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 18) &  (Queasy.number1 == reslin_list.reserve_int)).first()

                if queasy and queasy.logi3:
                    datum = reslin_list.ankunft

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()

                if f_resline.new_contrate:

                    if f_resline.bookdate != None:
                        rate_found, reslin_list.zipreis, f_resline.restricted, kback_flag = get_output(ratecode_rate(f_resline.ebdisc_flag, f_resline.kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + f_resline.contcode), f_resline.bookdate, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))
                    else:
                        rate_found, reslin_list.zipreis, f_resline.restricted, kback_flag = get_output(ratecode_rate(f_resline.ebdisc_flag, f_resline.kbdisc_flag, reslin_list.resnr, reslin_list.reslinnr, ("!" + f_resline.contcode), f_resline.ci_date, datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))
                else:
                    reslin_list.zipreis, rate_found = get_output(pricecod_rate(reslin_list.resnr, reslin_list.reslinnr, ("!" + f_resline.contcode), datum, reslin_list.ankunft, reslin_list.abreise, reslin_list.reserve_int, arrangement.argtnr, curr_zikatnr, reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2, reslin_list.reserve_dec, reslin_list.betriebsnr))

                    if rate_found:
                        check_bonus(datum)

                if queasy and queasy.logi1:
                    reslin_list.adrflag = True
                    f_resline.rate_tooltip = translateExtended ("Contract rate in LOCAL CURRENCY.", lvcarea, "")

            if not rate_found:

                if res_mode.lower()  == "inhouse":

                    katpreis = db_session.query(Katpreis).filter(
                            (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

                    if not katpreis:

                        katpreis = db_session.query(Katpreis).filter(
                                (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.startperiode <= datum) &  (Katpreis.endperiode >= datum) &  (Katpreis.betriebsnr == 0)).first()
                else:

                    katpreis = db_session.query(Katpreis).filter(
                            (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.datum >= Katpreis.startperiode) &  (Katpreis.datum <= Katpreis.endperiode) &  (Katpreis.betriebsnr == wd_array[get_weekday(datum) - 1])).first()

                    if not katpreis:

                        katpreis = db_session.query(Katpreis).filter(
                                (Katpreis.zikatnr == curr_zikatnr) &  (Katpreis.argtnr == arrangement.argtnr) &  (Katpreis.datum >= Katpreis.startperiode) &  (Katpreis.datum <= Katpreis.endperiode) &  (Katpreis.betriebsnr == 0)).first()

                if katpreis:
                    reslin_list.zipreis = get_rackrate (reslin_list.erwachs, reslin_list.kind1, reslin_list.kind2)
                else:
                    reslin_list.zipreis = 0

        if not direct_change and not rate_readonly and current_rate != 0 and reslin_list.zipreis == 0:
            reslin_list.zipreis = current_rate

        if rate_found and reslin_list.zipreis == 0 and (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci") and (reslin_list.erwachs > 0 or reslin_list.kind1 > 0):
            reslin_list.gratis = reslin_list.erwachs + reslin_list.kind1
            reslin_list.erwachs = 0
            reslin_list.kind1 = 0

    def check_dynarate():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        res_dynarate = query(res_dynarate_list, first=True)

        if not res_dynaRate:

            return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.kurzbez == res_dynaRate.rmcat)).first()

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_dynarate.argt)).first()

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == (9200 + res_dynaRate.setup))).first()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 18) &  (Queasy.number1 == res_dynaRate.markNo)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == queasy.char3)).first()
        reslin_list.ankunft = res_dynaRate.date1
        reslin_list.arrangement = res_dynaRate.argt
        reslin_list.zikatnr = zimkateg.zikatnr
        reslin_list.reserve_int = res_dynaRate.markNo
        reslin_list.betriebsnr = waehrungsnr
        reslin_list.l_zuordnung[0] = zimkateg.zikatnr
        f_resline.zikatstr = res_dynaRate.rmcat
        f_resline.rate_zikat = res_dynaRate.rmcat
        f_resline.marknr = res_dynaRate.markNo
        f_resline.contcode = res_dynaRate.prCode
        f_resline.origcontcode = res_dynaRate.rcode
        f_resline.combo_code = res_dynaRate.rcode
        f_resline.currency = queasy.char3

        if reslin_list.gratis == 0:
            reslin_list.erwachs = res_dynaRate.adult
            reslin_list.kind1 = res_dynaRate.child

        if reslin_list.setup == 0:
            reslin_list.setup = res_dynaRate.setup
            f_resline.c_setup = substring(paramtext.notes, 0, 1)

        if res_dynaRate.rate < 0:
            reslin_list.zipreis = - res_dynaRate.rate
        else:
            reslin_list.zipreis = res_dynaRate.rate

        res_dynarate = query(res_dynarate_list, last=True)
        reslin_list.abreise = res_dynaRate.date2 + 1

        if dayuse_flag:
            reslin_list.abreise = reslin_list.ankunft
        reslin_list.anztage = reslin_list.abreise - reslin_list.ankunft
        f_resline.arrday = weekdays[get_weekday(reslin_list.ankunft) - 1]
        f_resline.depday = weekdays[get_weekday(reslin_list.abreise) - 1]

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == f_resline.origcontcode)).first()

        for res_dynarate in query(res_dynarate_list):
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "arrangement"
            reslin_queasy.resnr = inp_resnr
            reslin_queasy.reslinnr = f_resline.reslinnr
            reslin_queasy.date1 = res_dynaRate.date1
            reslin_queasy.date2 = res_dynaRate.date2
            reslin_queasy.deci1 = res_dynaRate.rate
            reslin_queasy.char2 = res_dynaRate.prCode
            reslin_queasy.char3 = user_init

            if reslin_queasy.deci1 < 0:
                reslin_queasy.deci1 = - reslin_queasy.deci1
                res_dynarate_list.remove(res_dynarate)
            f_resline.fixed_rate = True
        f_resline.restricted = None != queasy and queasy.logi2

        if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "qci") and f_resline.restricted:
            reslin_list.zimmer_wunsch = reslin_list.zimmer_wunsch +\
                "restricted;"

    def check_bedsetup1():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, f_resline_list, curr_resline_list, reslin_list_list, reschanged_list_list, t_history_list, rline_list_list, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, htparam, bediener, master, guest, reslin_queasy, reservation, kontline, gentable, outorder, queasy, arrangement, nation, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, resline, resbuff, zimkateg1, rbuff, qci_zimmer, qsy, m_queasy, m_leist, resmember, rline, genbuff, bline, waehrung1, gbuff, w1
        nonlocal rline_list_list, reslin_list_list, curr_resline_list, t_history_list, currency_list_list, res_dynarate_list, reschanged_list_list, f_resline_list

        anz_setup:int = 0
        curr_setup:int = 0

        if reslin_list.setup == 0 and zimkateg:

            for zimmer in db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup != 0)).all():

                if curr_setup == 0:
                    curr_setup = zimmer.setup
                    anz_setup = 1

                if zimmer.setup != curr_setup:
                    anz_setup = 2
                    break

            if anz_setup == 1:
                reslin_list.setup = curr_setup

                paramtext = db_session.query(Paramtext).filter(
                        (Paramtext.txtnr == (9200 + curr_setup))).first()
                f_resline.c_setup = substring(paramtext.notes, 0, 1)


    if res_mode == "split+modify":
        res_mode = "modify"
        split_modify = True

    if num_entries(res_mode, chr(2)) > 1:

        if entry(1, res_mode, chr(2)) == "DU":
            dayuse_flag = True
        res_mode = entry(0, res_mode, chr(2))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 346)).first()

    if htparam and htparam.bezeich.lower()  != "not used":
        avail_gdpr = htparam.flogical
    flag_ok, init_time, init_date = get_output(check_timebl(1, inp_resnr, inp_reslinnr, "res_line", None, None))

    if not flag_ok:
        error_flag = True
        record_use = True

        return generate_output()

    if qci_zinr != "":

        qci_zimmer = db_session.query(Qci_zimmer).filter(
                (func.lower(Qci_zimmer.zinr) == (qci_zinr).lower())).first()
    f_resline = F_resline()
    f_resline_list.append(f_resline)


    if res_mode.lower()  == "modify" or res_mode.lower()  == "inhouse":

        resbuff = db_session.query(Resbuff).filter(
                (Resbuff.resnr == inp_resnr) &  (Resbuff.reslinnr == inp_reslinnr)).first()

        if not resbuff:
            msg_str = translateExtended ("Reservation is being modified by other user.", lvcarea, "")
            error_flag = True

            return generate_output()

        if res_mode.lower()  == "modify" and resbuff.active_flag == 1:
            msg_str = translateExtended ("Guest already checked_in.", lvcarea, "")
            error_flag = True

            return generate_output()
    f_resline.new_contrate = get_output(htplogic(550))
    f_resline.price_decimal = get_output(htpint(491))
    f_resline.ci_date = get_output(htpdate(87))
    f_resline.billdate = get_output(htpdate(110))
    f_resline.foreign_rate = get_output(htplogic(143))
    f_resline.res_status = get_output(htpint(478))
    f_resline.oral_flag = get_output(htplogic(938))
    f_resline.six_pm = get_output(htpint(297))

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    master = db_session.query(Master).filter(
            (Master.resnr == inp_resnr)).first()
    f_resline.master_exist = None != master

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == inp_gastnr)).first()
    f_resline.main_resname = guest.name


    f_resline.karteityp = guest.karteityp

    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (func.lower(Reslin_queasy.key) == "rate_prog") &  (Reslin_queasy.char1 == "") &  (Reslin_queasy.reslinnr == 1) &  (Reslin_queasy.number1 == inp_resnr) &  (Reslin_queasy.number2 == 0)).first()

    if reslin_queasy:
        f_resline.prog_str = reslin_queasy.char3

    if res_mode.lower()  == "earlyci":
        f_resline.earlyci = True
        res_mode = "modify"

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 472)).first()

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        f_resline.param472 = htparam.flogical


    f_resline.allot_tooltip = translateExtended ("Allotment", lvcarea, "")

    if res_mode.lower()  == "new" or res_mode.lower()  == "qci":

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr)).all():
            new_reslinnr = res_line.reslinnr + 1
            break
        f_resline.reslinnr = new_reslinnr

    elif res_mode.lower()  == "modify" or res_mode.lower()  == "inhouse":

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_reslinnr)).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == inp_resnr)).first()

        if res_line.kontignr > 0:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.kontignr == res_line.kontignr) &  (Kontline.kontstat == 1)).first()

            if kontline:
                f_resline.allot_tooltip = translateExtended ("Allotment Code", lvcarea, "")

        elif res_line.kontignr < 0:

            kontline = db_session.query(Kontline).filter(
                    (Kontline.kontignr == - res_line.kontignr) &  (Kontline.kontstat == 1)).first()

            if kontline:
                f_resline.allot_tooltip = translateExtended ("Global Reservation Code", lvcarea, "")
        curr_resline = Curr_resline()
        curr_resline_list.append(curr_resline)

        buffer_copy(res_line, curr_resline)

        gentable = db_session.query(Gentable).filter(
                (func.lower(Gentable.key) == "reservation") &  (Gentable.number1 == inp_resnr) &  (Gentable.number2 == inp_reslinnr)).first()
        f_resline.gentable = None != gentable

        resline = db_session.query(Resline).filter(
                (Resline.resnr == res_line.resnr) &  (Resline.active_flag <= 1) &  (Resline.kontakt_nr == res_line.reslinnr) &  (Resline.l_zuordnung[2] == 1)).first()

        if resline:
            f_resline.accompany_gastnr = resline.gastnrmember

        if resline:

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == res_line.resnr) &  (Resline.active_flag <= 1) &  (Resline.kontakt_nr == res_line.reslinnr) &  (Resline.l_zuordnung[2] == 1)).first()

        if resline:
            f_resline.accompany_gastnr2 = resline.gastnrmember

        if resline:

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == res_line.resnr) &  (Resline.active_flag <= 1) &  (Resline.kontakt_nr == res_line.reslinnr) &  (Resline.l_zuordnung[2] == 1)).first()

        if resline:
            f_resline.accompany_gastnr3 = resline.gastnrmember

        if session_date.lower()  == "dmy":
            f_resline.rsv_tooltip = substring(res_line.reserve_char, 6, 2) + "/" +\
                substring(res_line.reserve_char, 3, 2) + "/" +\
                substring(res_line.reserve_char, 0, 2) + " " +\
                substring(res_line.reserve_char, 8, 5) + " " +\
                substring(res_line.reserve_char, 13)

        elif SESSION:DATE_FORMAT == "mdy":
            f_resline.rsv_tooltip = substring(res_line.reserve_char, 3, 2) + "/" +\
                substring(res_line.reserve_char, 6, 2) + "/" +\
                substring(res_line.reserve_char, 0, 2) + " " +\
                substring(res_line.reserve_char, 8, 5) + " " +\
                substring(res_line.reserve_char, 13)


        else:
            f_resline.rsv_tooltip = substring(res_line.reserve_char, 0, 8) + " " +\
                substring(res_line.reserve_char, 8, 5) + " " +\
                substring(res_line.reserve_char, 13)

        if res_mode.lower()  == "modify" and (res_line.resstatus <= 2 or res_line.resstatus == 5) and res_line.zinr != "":

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == res_line.zinr) &  (Outorder.betriebsnr == res_line.resnr)).first()
            f_resline.offmarket = None != outorder

        if res_line.code != "" and res_line.CODE.lower()  != "0":
            f_resline.bill_instruct = to_int(res_line.code)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 9) &  (Queasy.number1 == bill_instruct)).first()

            if queasy:
                f_resline.instruct_str = queasy.char1
        f_resline.guestnr = res_line.gastnrpay
        f_resline.reslinnr = inp_reslinnr
        f_resline.grpflag = res_line.grpflag
        f_resline.rline_bemerk = res_line.bemerk
        f_resline.res_bemerk = reservation.bemerk
        f_resline.kontignr = res_line.kontignr
        f_resline.zimmeranz = res_line.zimmeranz
        f_resline.sharer = (res_line.resstatus == 11)
        OR (res_line.resstatus = 13)

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()
        f_resline.zikatstr = zimkateg.kurzbez

    elif res_mode.lower()  == "insert" or res_mode.lower()  == "split":
        f_resline.reslinnr = 1
        f_resline.tot_qty = 0

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == inp_resnr)).all():

            if f_resline.guestnr == 0:
                f_resline.guestnr = res_line.gastnrpay

            if res_line.reslinnr > f_resline.reslinnr:
                f_resline.reslinnr = res_line.reslinnr
            f_resline.grpflag = res_line.grpflag
            f_resline.tot_qty = f_resline.tot_qty + res_line.zimmeranz
        f_resline.reslinnr = f_resline.reslinnr + 1
    logic_p1109 = get_output(htplogic(1109))
    f_resline.res_bemerk = f_resline.res_bemerk +\
            chr(2) + to_string(to_int(logic_p1109))

    if res_mode.lower()  == "split":
        split_resline()

    if res_mode.lower()  == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci":
        f_resline.bill_instruct = 0
        f_resline.instruct_str = ""

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == inp_gastnr)).first()
        res_line = Res_line()
        db_session.add(res_line)

        f_resline.guestname = guest.name
        f_resline.guestnr = guest.gastnr
        res_line.resnr = inp_resnr
        res_line.reslinnr = f_resline.reslinnr
        res_line.gastnr = inp_gastnr
        res_line.gastnrpay = inp_gastnr
        res_line.gastnrmember = inp_gastnr
        res_line.ankunft = f_resline.ci_date
        res_line.abreise = res_line.ankunft + 1
        res_line.anztage = 1
        res_line.zimmeranz = 1
        res_line.name = guest.name
        res_line.resname = f_resline.main_resname
        res_line.erwachs = 1
        res_line.gratis = 0
        res_line.grpflag = f_resline.grpflag
        res_line.active_flag = 2
        res_line.resstatus = 12

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 262)).first()

        if htparam.finteger != 0:
            res_line.erwachs = htparam.finteger

        if res_mode.lower()  == "insert":

            resline = db_session.query(Resline).filter(
                    (Resline.resnr == inp_resnr) &  (Resline.active_flag <= 1) &  (Resline.resstatus != 12) &  (Resline.l_zuordnung[2] == 0)).first()

            if resline:

                if resline.active_flag == 0:
                    res_line.ankunft = resline.ankunft
                    res_line.abreise = resline.abreise
                    res_line.anztage = res_line.abreise - res_line.ankunft

                elif resline.active_flag == 1:
                    res_line.abreise = resline.abreise
                    res_line.anztage = res_line.abreise - res_line.ankunft

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 150)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == htparam.finteger)).first()

        if zimkateg:
            f_resline.zikatstr = zimkateg.kurzbez
            res_line.zikatnr = zimkateg.zikatnr

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 151)).first()

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == htparam.fchar)).first()

        if arrangement:
            res_line.arrangement = arrangement


        f_resline.curr_arg = res_line.arrangement


    reslin_list = Reslin_list()
    reslin_list_list.append(reslin_list)

    reslin_list.reserve_dec = 0
    reslin_list.resnr = inp_resnr

    if res_mode.lower()  != "split":

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == f_resline.guestnr)).first()
        f_resline.billname = guest.name + ", " + guest.vorname1 +\
                guest.anredefirma +\
                " " + guest.anrede1
        f_resline.billadress = guest.adresse1
        f_resline.billcity = guest.wohnort + " " + guest.plz

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == guest.land)).first()

        if nation:
            f_resline.billland = nation.bezeich


        f_resline.name_editor = f_resline.billname + chr(10) + chr(10) +\
                f_resline.billadress + chr(10) +\
                f_resline.billcity + chr(10) + chr(10) +\
                f_resline.billland
        f_resline.zahlungsart = guest.zahlungsart

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
        f_resline.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == inp_gastnr)).first()

        if qci_zimmer:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == qci_zimmer.zikatnr)).first()
        else:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            f_resline.zikatstr = zimkateg.kurzbez


        f_resline.curr_arg = res_line.arrangement


        buffer_copy(res_line, reslin_list)

        if qci_zimmer:
            reslin_list.setup = qci_zimmer.setup
            reslin_list.zinr = qci_zimmer.zinr


        f_resline.arrday = weekdays[get_weekday(reslin_list.ankunft) - 1]
        f_resline.depday = weekdays[get_weekday(reslin_list.abreise) - 1]
        f_resline.comchild = reslin_list.l_zuordnung[3]
        f_resline.pickup_flag = re.match(".*pickup.*",reslin_list.zimmer_wunsch)
        f_resline.drop_flag = re.match(".*drop_passanger.*",reslin_list.zimmer_wunsch)
        f_resline.marknr = reslin_list.reserve_int


        pass

        if reslin_list.l_zuordnung[0] != 0:

            zimkateg1 = db_session.query(Zimkateg1).filter(
                    (Zimkateg1.zikatnr == reslin_list.l_zuordnung[0])).first()

            if zimkateg1:
                f_resline.rate_zikat = zimkateg1.kurzbez

        if res_mode.lower()  == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci":

            if f_resline.res_status == 1:
                reslin_list.resstatus = 3

            elif f_resline.res_status == 2:
                reslin_list.resstatus = 2

            elif f_resline.res_status == 3 and f_resline.oral_flag:
                reslin_list.resstatus = 5
            else:
                reslin_list.resstatus = 1
            reslin_list.active_flag = 0
        else:
            reslin_list.resstatus = res_line.resstatus
            reslin_list.active_flag = res_line.active_flag

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == res_line.gastnr)).first()

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()
        fill_flightnr()

    if re.match(".*;.*",res_line.memozinr):
        f_resline.memo_zinr = entry(1, res_line.memozinr, ";")

    if f_resline.new_contrate:
        f_resline.ebdisc_flag = re.match(".*ebdisc.*",reslin_list.zimmer_wunsch)
        f_resline.kbdisc_flag = re.match(".*kbdisc.*",reslin_list.zimmer_wunsch)
        f_resline.restricted = re.match(".*restricted.*",reslin_list.zimmer_wunsch)


    curr_time = get_current_time_in_seconds()

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == inp_gastnr)).first()

    if guest_pr:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.logi2) &  (Queasy.char1 == guest_pr.CODE)).first()

        if queasy:

            if f_resline.new_contrate:
                while None != guest_pr:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 2) &  (Queasy.char1 == guest_pr.CODE)).first()

                    if queasy:
                        do_it = True

                        if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci"):

                            if f_resline.ci_date < queasy.date1:
                                do_it = False

                            elif f_resline.ci_date > queasy.date2:
                                do_it = False

                        if do_it:

                            ratecode = db_session.query(Ratecode).filter(
                                    (Ratecode.code == guest_pr.code) &  (f_resline.ci_date <= Ratecode.endperiode)).first()

                            if ratecode:
                                f_resline.enable_frate = True

                                if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert" or res_mode.lower().lower()  == "qci") and reslin_list.reserve_int == 0 and ratecode.marknr > 0:
                                    reslin_list.reserve_int = ratecode.marknr
                                    f_resline.contcode = ratecode.CODE
                                    f_resline.origcontcode = ratecode.CODE

                            ratecode = db_session.query(Ratecode).filter(
                                    (Ratecode.code == guest_pr.code) &  (Ratecode.char1[0] != "")).first()

                            if ratecode:
                                f_resline.enable_ebdisc = True

                            ratecode = db_session.query(Ratecode).filter(
                                    (Ratecode.code == guest_pr.code) &  (Ratecode.char1[1] != "")).first()

                            if ratecode:
                                f_resline.enable_kbdisc = True

                    guest_pr = db_session.query(Guest_pr).filter(
                            (Guest_pr.gastnr == inp_gastnr)).first()
            else:

                pricecod = db_session.query(Pricecod).filter(
                        (Pricecod.code == guest_pr.code) &  (f_resline.ci_date <= Pricecod.endperiode)).first()

                if pricecod:
                    f_resline.enable_frate = True
    for i in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
        str = entry(i - 1, reslin_list.zimmer_wunsch, ";")

        if substring(str, 0, 7) == "voucher":
            f_resline.voucher = substring(str, 7)

        elif substring(str, 0, 5) == "ChAge":
            f_resline.child_age = substring(str, 5)

        elif substring(str, 0, 6) == "$CODE$":
            f_resline.contcode = substring(str, 6)

        elif substring(str, 0, 5) == "DATE,":
            f_resline.bookdate = date_mdy(to_int(substring(str, 9, 2)) , to_int(substring(str, 11, 2)) , to_int(substring(str, 5, 4)))

        elif substring(str, 0, 8) == "SEGM__PUR":
            f_resline.i_purpose = to_int(substring(str, 8))

        elif re.match(".*WCI_req.*",str):
            str1 = entry(1, str, " == ")


            for loopi in range(1,num_entries(str1, ",")  + 1) :

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 160) &  (Queasy.number1 == to_int(entry(loopi - 1, str1, ",")))).first()

                if queasy:
                    for loopj in range(1,num_entries(queasy.char1, ";")  + 1) :

                        if re.match(".*en.*",entry(loopj - 1, queasy.char1, ";")):
                            f_resline.wci_flag = entry(1, entry(loopj - 1, queasy.char1, ";") , " == ") + ", " + f_resline.wci_flag


                            break

        elif substring(str, 0, 4) == "GDPR":
            f_resline.gdpr_flag = substring(str, 4)

    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr)).first()

    if reslin_queasy:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 189)).first()

        if queasy:
            f_resline.voucher = f_resline.voucher + chr(2) +\
                reslin_queasy.char3

    if f_resline.contcode != "":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == f_resline.contcode)).first()
        f_resline.combo_code = f_resline.contcode

        if queasy:
            f_resline.tip_code = queasy.char1 + " - " + queasy.char2

            rbuff = db_session.query(Rbuff).filter(
                    (Rbuff.CODE == f_resline.contcode)).first()

            if rbuff:

                prmarket = db_session.query(Prmarket).filter(
                        (Prmarket.nr == rbuff.marknr)).first()

                if prmarket:
                    f_resline.marknr = rbuff.marknr
                    f_resline.tip_code = f_resline.tip_code + " [" +\
                        prmarket.bezeich + "]"

    if (res_mode.lower()  == "modify" or res_mode.lower().lower()  == "inhouse") and substring(bediener.permission, 42, 2) < "2":
        f_resline.enable_disc = False

    if res_mode.lower()  == "modify" or res_mode.lower()  == "inhouse" or res_mode.lower()  == "split":
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 10) == "$OrigCode$":
                prevcode = substring(str, 10)
                f_resline.origcontcode = prevcode


                break

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == inp_gastnr)).first()

    if guest_pr:

        guest_pr_obj_list = []
        for guest_pr, queasy in db_session.query(Guest_pr, Queasy).join(Queasy,(Queasy.key == 2) &  (Queasy.char1 == Guest_pr.CODE)).filter(
                (Guest_pr.gastnr == inp_gastnr) &  (Guest_pr.CODE != f_resline.contcode)).all():
            if guest_pr._recid in guest_pr_obj_list:
                continue
            else:
                guest_pr_obj_list.append(guest_pr._recid)


            do_it = True

            if queasy.char1 != prevcode:

                if f_resline.ci_date < queasy.date1:
                    do_it = False

                elif f_resline.ci_date > queasy.date2:
                    do_it = False

            if do_it:
                f_resline.combo_code = f_resline.combo_code + ";" + guest_pr.CODE

                if f_resline.contcode == "":
                    f_resline.contcode = guest_pr.CODE


                    f_resline.tip_code = queasy.char1 + " - " + queasy.char2

                    if queasy.logi2:

                        rbuff = db_session.query(Rbuff).filter(
                                (Rbuff.CODE == f_resline.contcode)).first()

                        if rbuff:
                            iftask = rbuff.char1[4]
                        for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                            mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                            mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                            if mestoken == "RC":
                                rcode = mesvalue

                    if rcode != "":

                        rbuff = db_session.query(Rbuff).filter(
                                (Rbuff.CODE == rcode)).first()

                        if rbuff:

                            qsy = db_session.query(Qsy).filter(
                                    (Qsy.key == 18) &  (Qsy.number1 == rbuff.marknr)).first()
                else:

                    rbuff = db_session.query(Rbuff).filter(
                            (Rbuff.CODE == guest_pr.CODE)).first()

                    if rbuff:

                        prmarket = db_session.query(Prmarket).filter(
                                (Prmarket.nr == rbuff.marknr)).first()

                    if prmarket:
                        f_resline.tip_code = f_resline.tip_code + " [" +\
                                prmarket.bezeich + "]"

                        qsy = db_session.query(Qsy).filter(
                                (Qsy.key == 18) &  (Qsy.number1 == prmarket.nr)).first()

                if qsy:

                    currency_list = query(currency_list_list, filters=(lambda currency_list :currency_list.wabkurz == qsy.char3), first=True)

                    if not currency_list:
                        currency_list = Currency_list()
                        currency_list_list.append(currency_list)

                        currency_list.wabkurz = qsy.char3


    disp_allotment()
    get_currency()
    f_resline.l_ankunft = reslin_list.ankunft
    f_resline.l_abreise = reslin_list.abreise
    f_resline.l_night = reslin_list.anztage

    if reslin_list.active_flag == 0 and reslin_list.zinr != "":

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == reslin_list.zinr) &  (Outorder.betriebsnr == reslin_list.resnr)).first()
        f_resline.offmarket = None != outorder
    disp_history()
    check_dynarate()
    check_bedsetup()

    reslin_queasy = db_session.query(Reslin_queasy).filter(
            (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == reslin_list.resnr) &  (Reslin_queasy.reslinnr == reslin_list.reslinnr)).first()
    f_resline.fixed_rate = None != reslin_queasy

    if f_resline.fixed_rate and reslin_list.l_zuordnung[0] == 0:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == reslin_list.zikatnr)).first()

        if zimkateg:
            f_resline.rate_zikat = zimkateg.kurzbez
            reslin_list.l_zuordnung[0] = zimkateg.zikatnr

    if not f_resline.fixed_rate and (bediener.char1 != ""):
        f_resline.enable_disc = True

    if res_mode.lower()  == "new" or res_mode.lower()  == "insert" or res_mode.lower()  == "qci":
        set_roomrate(True)

    if res_mode.lower()  == "inhouse" and reslin_list.resstatus == 8:
        set_roomrate(True)

    if not split_modify:
        rline_list_list, reschanged_list_list = get_output(mk_resline_query_q1bl(pvilanguage, True, True, inp_resnr, rline_list, reschanged_list))

    if f_resline.restricted:
        msg_str = msg_str + chr(2) + "&W" + translateExtended ("This is Reservation with Restricted Discounted rate", lvcarea, "") + chr(10) + translateExtended ("Any reservation data changes such as C/i- or C/O_date", lvcarea, "") + chr(10) + translateExtended ("might have impact to the given room rate.", lvcarea, "") + chr(10)

    if res_mode.lower()  == "split":
        flag_ok, init_time, init_date = get_output(check_timebl(2, inp_resnr, inp_reslinnr, "res_line", init_time, init_date))

    fixleist = db_session.query(Fixleist).filter(
            (Fixleist.resnr == inp_resnr) &  (Fixleist.reslinnr == inp_reslinnr)).first()

    if fixleist:
        msg_str = msg_str + "FixleistIncluded"

    return generate_output()