#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.check_timebl import check_timebl
from functions.htplogic import htplogic
from functions.htpint import htpint
from functions.htpdate import htpdate
import re
from functions.mk_resline_query_q1bl import mk_resline_query_q1bl
from functions.check_complimentbl import check_complimentbl
from functions.intevent_1 import intevent_1
from functions.ratecode_rate import ratecode_rate
from functions.pricecod_rate import pricecod_rate
from models import Res_line, History, Zimkateg, Ratecode, Zimmer, Guest, Queasy, Htparam, Nation, Bediener, Master, Reslin_queasy, Reservation, Kontline, Gentable, Outorder, Arrangement, Guest_pr, Pricecod, Prmarket, Fixleist, Paramtext, Waehrung, Katpreis

res_dynarate_data, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":Decimal, "rmcat":string, "argt":string, "prcode":string, "rcode":string, "markno":int, "setup":int, "adult":int, "child":int})

def prepare_resline_4bl(pvilanguage:int, res_mode:string, session_date:string, user_init:string, inp_gastnr:int, inp_resnr:int, inp_reslinnr:int, rate_readonly:bool, qci_zinr:string, res_dynarate_data:[Res_dynarate]):

    prepare_cache ([Res_line, Zimkateg, Ratecode, Zimmer, Queasy, Htparam, Nation, Bediener, Reservation, Kontline, Arrangement, Prmarket, Paramtext, Waehrung, Katpreis])

    msg_str = ""
    error_flag = False
    record_use = False
    init_time = 0
    init_date = None
    avail_gdpr = False
    avail_mark = False
    avail_news = False
    save_gdpr = 0
    curr_date = None
    serv_date = False
    f_resline_data = []
    curr_resline_data = []
    reslin_list_data = []
    reschanged_list_data = []
    t_history_data = []
    rline_list_data = []
    weekdays:List[string] = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    i:int = 0
    str:string = ""
    loopi:int = 0
    loopj:int = 0
    str1:string = ""
    foreign_nr:int = 0
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    rcode:string = ""
    prevcode:string = ""
    do_it:bool = False
    do_it1:bool = False
    flag_ok:bool = False
    dayuse_flag:bool = False
    split_modify:bool = False
    logic_p1109:bool = False
    priscilla_active:bool = True
    loopk:int = 0
    resbemerk:string = ""
    lvcarea:string = "mk-resline"
    new_reslinnr:int = 1
    curr_time:int = 0
    res_line = history = zimkateg = ratecode = zimmer = guest = queasy = htparam = nation = bediener = master = reslin_queasy = reservation = kontline = gentable = outorder = arrangement = guest_pr = pricecod = prmarket = fixleist = paramtext = waehrung = katpreis = None

    rline_list = reslin_list = curr_resline = t_history = currency_list = res_dynarate = reschanged_list = f_resline = nation_list = periode_list = resline = resbuff = zimkateg1 = rbuff = qci_zimmer = bresline = bguest = bqueasy = qsy = None

    rline_list_data, Rline_list = create_model_like(Res_line, {"res_char":string, "rsvname":string, "kurzbez":string, "status_str":string})
    reslin_list_data, Reslin_list = create_model_like(Res_line)
    curr_resline_data, Curr_resline = create_model_like(Res_line)
    t_history_data, T_history = create_model_like(History)
    currency_list_data, Currency_list = create_model("Currency_list", {"wabkurz":string})
    reschanged_list_data, Reschanged_list = create_model("Reschanged_list", {"reslinnr":int})
    f_resline_data, F_resline = create_model("F_resline", {"guestname":string, "curr_segm":string, "curr_source":string, "curr_arg":string, "c_purpose":string, "contcode":string, "origcontcode":string, "tip_code":string, "voucher":string, "instruct_str":string, "arrday":string, "depday":string, "flight1":string, "flight2":string, "eta":string, "etd":string, "allot_str":string, "allot_tooltip":string, "rate_zikat":string, "zikatstr":string, "currency":string, "c_setup":string, "memo_zinr":string, "billname":string, "billadress":string, "billcity":string, "billland":string, "name_editor":string, "hist_comment":string, "main_resname":string, "prog_str":string, "rsv_tooltip":string, "rate_tooltip":string, "rline_bemerk":string, "res_bemerk":string, "child_age":string, "combo_code":string, "reslinnr":int, "bill_instruct":int, "kontignr":int, "zimmeranz":int, "comchild":int, "price_decimal":int, "res_status":int, "karteityp":int, "guestnr":int, "tot_qty":int, "zahlungsart":int, "marknr":int, "i_purpose":int, "local_nr":int, "foreign_nr":int, "l_night":int, "six_pm":int, "accompany_gastnr":int, "accompany_gastnr2":int, "accompany_gastnr3":int, "ci_date":date, "billdate":date, "bookdate":date, "l_ankunft":date, "l_abreise":date, "earlyci":bool, "master_exist":bool, "master_active":bool, "pickup_flag":bool, "drop_flag":bool, "enable_frate":bool, "ebdisc_flag":bool, "kbdisc_flag":bool, "restricted":bool, "enable_ebdisc":bool, "enable_kbdisc":bool, "new_contrate":bool, "foreign_rate":bool, "gentable":bool, "offmarket":bool, "grpflag":bool, "sharer":bool, "fixed_rate":bool, "enable_disc":bool, "oral_flag":bool, "param472":bool, "wci_flag":string, "gdpr_flag":string, "mark_flag":string, "news_flag":string, "repeat_charge":bool, "every_month":int, "repeat_amount":Decimal, "start_date":date, "end_date":date}, {"zimmeranz": 1, "bookdate": None, "l_ankunft": None, "l_abreise": None})
    nation_list_data, Nation_list = create_model("Nation_list", {"nr":int, "kurzbez":string, "bezeich":string})
    periode_list_data, Periode_list = create_model("Periode_list", {"counter":int, "periode1":date, "periode2":date, "diff_day":int, "amt_periode":Decimal, "tamount":Decimal})

    Resline = create_buffer("Resline",Res_line)
    Resbuff = create_buffer("Resbuff",Res_line)
    Zimkateg1 = create_buffer("Zimkateg1",Zimkateg)
    Rbuff = create_buffer("Rbuff",Ratecode)
    Qci_zimmer = create_buffer("Qci_zimmer",Zimmer)
    Bresline = create_buffer("Bresline",Res_line)
    Bguest = create_buffer("Bguest",Guest)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        return {"res_mode": res_mode, "msg_str": msg_str, "error_flag": error_flag, "record_use": record_use, "init_time": init_time, "init_date": init_date, "avail_gdpr": avail_gdpr, "avail_mark": avail_mark, "avail_news": avail_news, "save_gdpr": save_gdpr, "curr_date": curr_date, "serv_date": serv_date, "f-resline": f_resline_data, "curr-resline": curr_resline_data, "reslin-list": reslin_list_data, "reschanged-list": reschanged_list_data, "t-history": t_history_data, "rline-list": rline_list_data}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    def fill_flightnr():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data


        f_resline.flight1 = substring(res_line.flight_nr, 0, 6)
        f_resline.eta = substring(res_line.flight_nr, 6, 5)
        f_resline.flight2 = substring(res_line.flight_nr, 11, 6)
        f_resline.etd = substring(res_line.flight_nr, 17, 5)

        if trim(f_resline.eta) == "":
            f_resline.eta = "0000"

        if trim(f_resline.etd) == "":
            f_resline.etd = "0000"


    def split_resline():

        nonlocal error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        i:int = 0
        anz:int = 0
        reihe:int = 0
        main_reihe:int = 0
        zeit:int = 0
        m_queasy = None
        m_leist = None
        resmember = None
        rline = None
        genbuff = None
        bline = None
        prline = None
        max_comp:int = 0
        com_rm:int = 0
        its_wrong:bool = False
        msg_str:string = ""
        pswd_str:string = ""
        M_queasy =  create_buffer("M_queasy",Reslin_queasy)
        M_leist =  create_buffer("M_leist",Fixleist)
        Resmember =  create_buffer("Resmember",Res_line)
        Rline =  create_buffer("Rline",Res_line)
        Genbuff =  create_buffer("Genbuff",Gentable)
        Bline =  create_buffer("Bline",Res_line)
        Prline =  create_buffer("Prline",Res_line)
        zeit = get_current_time_in_seconds() - 2

        bline = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

        if bline:
            its_wrong, com_rm, max_comp, pswd_str, msg_str = get_output(check_complimentbl(pvilanguage, bline.resnr, bline.reslinnr, bline.gastnr, bline.ankunft, f_resline.marknr, bline.zikatnr, bline.arrangement, bline.zimmeranz, bline.zipreis))

        for rline in db_session.query(Rline).filter(
                 (Rline.resnr == inp_resnr) & (Rline.active_flag <= 1)).order_by(Rline.reslinnr).all():

            res_line = get_cache (Res_line, {"_recid": [(eq, rline._recid)]})

            if reihe == 0:
                reihe = res_line.reslinnr

            if res_line.reslinnr == 1:
                m_queasy = Reslin_queasy()
                db_session.add(m_queasy)

                m_queasy.key = "ResChanges"
                m_queasy.resnr = res_line.resnr
                m_queasy.reslinnr = res_line.reslinnr
                m_queasy.date2 = get_current_date()
                m_queasy.number2 = zeit


                m_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string("Splitted Reservation") + ";"
                pass

            if priscilla_active:

                if res_line.zimmeranz > 1:
                    get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

            gentable = get_cache (Gentable, {"key": [(eq, "reservation")],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

            if res_line.resstatus == 11:

                for prline in db_session.query(Prline).filter(
                         (Prline.resnr == res_line.resnr) & (Prline.resstatus == 11) & (Prline.kontakt_nr == 1)).order_by(Prline.reslinnr.desc()).yield_per(100):
                    main_reihe = prline.reslinnr + 1


                    break
            zeit = zeit + 2
            i = 2


            while i <= res_line.zimmeranz:
                resmember = Res_line()
                db_session.add(resmember)

                resmember.zimmeranz = 1
                resmember.reslinnr = f_resline.reslinnr
                resmember.resname = f_resline.main_resname


                buffer_copy(res_line, resmember,except_fields=["zimmeranz","reslinnr","resname"])

                if res_line.resstatus == 11:
                    resmember.kontakt_nr = main_reihe
                    main_reihe = main_reihe + 1

                if priscilla_active:
                    get_output(intevent_1(13, "", "Priscilla", resmember.resnr, resmember.reslinnr))

                if com_rm != 0:
                    resmember.zipreis =  to_decimal("0")
                    com_rm = com_rm - 1


                m_queasy = Reslin_queasy()
                db_session.add(m_queasy)

                m_queasy.key = "ResChanges"
                m_queasy.resnr = res_line.resnr
                m_queasy.reslinnr = f_resline.reslinnr
                m_queasy.date2 = get_current_date()
                m_queasy.number2 = zeit


                m_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name) + ";" + to_string("Splitted Reservation") + ";"
                pass

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).all():
                    m_queasy = Reslin_queasy()
                    db_session.add(m_queasy)

                    m_queasy.reslinnr = f_resline.reslinnr


                    buffer_copy(reslin_queasy, m_queasy,except_fields=["reslinnr"])
                    pass

                if resmember.zipreis != 0:

                    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy._recid).all():
                        m_queasy = Reslin_queasy()
                        db_session.add(m_queasy)

                        m_queasy.reslinnr = f_resline.reslinnr


                        buffer_copy(reslin_queasy, m_queasy,except_fields=["reslinnr"])
                        pass

                    for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        m_leist = Fixleist()
                        db_session.add(m_leist)

                        m_leist.reslinnr = f_resline.reslinnr


                        buffer_copy(fixleist, m_leist,except_fields=["reslinnr"])
                        pass

                if gentable:
                    genbuff = Gentable()
                    db_session.add(genbuff)

                    genbuff.number2 = f_resline.reslinnr


                    buffer_copy(gentable, genbuff,except_fields=["number2"])
                    pass
                pass
                f_resline.reslinnr = f_resline.reslinnr + 1
                i = i + 1
            res_line.zimmeranz = 1
            pass
            pass
        f_resline.reslinnr = reihe

        res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, reihe)]})


    def check_bedsetup():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        if reslin_list.setup != 0:

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, reslin_list.setup)]})

            if not zimmer:
                reslin_list.setup = 0
                f_resline.c_setup = ""

                return
            else:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, (9200 + reslin_list.setup))]})
                f_resline.c_setup = substring(paramtext.notes, 0, 1)


        else:
            reslin_list.setup = 0
            f_resline.c_setup = ""


            check_bedsetup1()


    def disp_allotment():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        if reslin_list.kontignr == 0:

            return

        if reslin_list.kontignr > 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, reslin_list.kontignr)],"kontstatus": [(eq, 1)]})
        else:

            kontline = get_cache (Kontline, {"kontignr": [(eq, - reslin_list.kontignr)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

        if kontline:
            f_resline.kontignr = reslin_list.kontignr
            f_resline.allot_str = kontline.kontcode


    def get_currency():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        curr_wabnr:int = 0
        guest_currency:int = 0
        waehrung1 = None
        rline = None
        gbuff = None
        found:bool = False
        Waehrung1 =  create_buffer("Waehrung1",Waehrung)
        Rline =  create_buffer("Rline",Res_line)
        Gbuff =  create_buffer("Gbuff",Guest)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if not waehrung1:
            msg_str = translateExtended ("Local Currency Code incorrect! (Param 152 / Grp 7)", lvcarea, "") + chr_unicode(10)

            return
        f_resline.local_nr = waehrung1.waehrungsnr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if (not waehrung1) and f_resline.foreign_rate:
            msg_str = translateExtended ("Foreign Currency Code incorrect! (Param 144 / Grp 7)", lvcarea, "") + chr_unicode(10)

            return

        if waehrung1:
            foreign_nr = waehrung1.waehrungsnr

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff.gastnr == inp_gastnr)).first()

        if gbuff.notizen[2] != "":

            waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, gbuff.notizen[2])]})

            if waehrung1:
                guest_currency = waehrung1.waehrungsnr

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

        if reslin_queasy:

            for waehrung1 in db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr != reslin_list.betriebsnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                f_resline.currency = f_resline.currency + waehrung1.wabkurz + ";"

            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})

            if waehrung1:
                f_resline.currency = waehrung1.wabkurz + ";" + f_resline.currency

            return

        currency_list = query(currency_list_data, first=True)

        if currency_list:

            for currency_list in query(currency_list_data):
                f_resline.currency = f_resline.currency + currency_list.wabkurz + ";"

            return

        if reslin_list.betriebsnr == 0 or f_resline.marknr != 0:

            if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()  or f_resline.marknr != 0):
                pass

                if f_resline.contcode != "":

                    guest_pr = get_cache (Guest_pr, {"code": [(eq, f_resline.contcode)]})

                if not guest_pr:

                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, inp_gastnr)]})

                if guest_pr:

                    if f_resline.marknr == 0:

                        ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)]})

                        if ratecode:
                            f_resline.marknr = ratecode.marknr

                    if f_resline.marknr != 0:

                        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, f_resline.marknr)]})

                        if not queasy or (queasy and queasy.char3 == ""):

                            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})
                    else:

                        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

                    if queasy:

                        if queasy.key == 18:

                            waehrung1 = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})
                        else:

                            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy.number1)]})

                        if waehrung1:
                            found = True
                            curr_wabnr = waehrung1.waehrungsnr

                            rline = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

                            if rline:
                                rline.betriebsnr = waehrung1.waehrungsnr
                                pass
                            reslin_list.betriebsnr = waehrung1.waehrungsnr

            if not found:

                if reslin_list.adrflag  or not f_resline.foreign_rate:
                    curr_wabnr = f_resline.local_nr
                    reslin_list.betriebsnr = f_resline.local_nr

                    waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, f_resline.local_nr)]})
                else:

                    if guest_currency != 0:
                        curr_wabnr = guest_currency
                    else:
                        curr_wabnr = foreign_nr
                    reslin_list.betriebsnr = curr_wabnr

                for waehrung1 in db_session.query(Waehrung1).filter(
                         (Waehrung1.waehrungsnr != curr_wabnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                    f_resline.currency = f_resline.currency + waehrung1.wabkurz + ";"

                waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, curr_wabnr)]})
        else:

            for waehrung1 in db_session.query(Waehrung1).filter(
                     (Waehrung1.waehrungsnr != reslin_list.betriebsnr) & (Waehrung1.betriebsnr == 0)).order_by(Waehrung1.bezeich).all():
                f_resline.currency = f_resline.currency + waehrung1.wabkurz + ";"

            waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, reslin_list.betriebsnr)]})
        f_resline.currency = waehrung1.wabkurz + ";" + f_resline.currency


    def disp_history():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        i_anzahl:int = 0

        for history in db_session.query(History).filter(
                 (History.gastnr == reslin_list.gastnrmember)).order_by(History.ankunft.desc()).all():
            i_anzahl = i_anzahl + 1
            t_history = T_history()
            t_history_data.append(t_history)

            buffer_copy(history, t_history)

            if i_anzahl == 4:

                return


    def set_roomrate(direct_change:bool):

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        datum:date = None
        add_it:bool = False
        answer:bool = False
        curr_rate:Decimal = to_decimal("0.0")
        exchg_rate:Decimal = 1
        qty:int = 0
        i:int = 0
        argt_defined:bool = False
        current_rate:Decimal = to_decimal("0.0")
        exrate1:Decimal = 1
        ex2:Decimal = 1
        child1:int = 0
        curr_zikatnr:int = 0
        rate_found:bool = False
        prgrate_found:bool = False
        early_flag:bool = False
        kback_flag:bool = False
        wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
        w1 = None
        W1 =  create_buffer("W1",Waehrung)

        if not arrangement:

            return

        if res_mode.lower()  != ("new").lower()  and res_mode.lower()  != ("insert").lower()  and res_mode.lower()  != ("qci").lower() :

            if not direct_change and reslin_list.zipreis != 0:

                return

            if substring(bediener.permissions, 42, 1) < ("2").lower() :

                return
        current_rate =  to_decimal(reslin_list.zipreis)


        datum = reslin_list.ankunft

        if res_mode.lower()  == ("inhouse").lower() :
            datum = f_resline.ci_date

        if res_mode.lower()  == ("inhouse").lower()  and reslin_list.resstatus == 8:

            if reslin_list.ankunft == reslin_list.abreise:
                datum = reslin_list.abreise


            else:
                datum = reslin_list.abreise - timedelta(days=1)

        if reslin_list.l_zuordnung[0] != 0:
            curr_zikatnr = reslin_list.l_zuordnung[0]
        else:
            curr_zikatnr = reslin_list.zikatnr

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, inp_gastnr)]})

        if reslin_list.erwachs == 0 and reslin_list.kind1 == 0 and reslin_list.kind2 == 0:
            reslin_list.zipreis =  to_decimal("0")
        else:

            if f_resline.fixed_rate:

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if reslin_queasy:
                    reslin_list.zipreis =  to_decimal(reslin_queasy.deci1)
                    f_resline.rate_tooltip = ""
                    rate_found = True

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

            if guest_pr and not rate_found:

                queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, reslin_list.reserve_int)]})

                if queasy and queasy.logi3:
                    datum = reslin_list.ankunft

                queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

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

                if res_mode.lower()  == ("inhouse").lower() :

                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

                    if not katpreis:

                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})
                else:

                    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

                    if not katpreis:

                        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, curr_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})

                if katpreis:
                    reslin_list.zipreis =  to_decimal(get_rackrate (reslin_list.erwachs , reslin_list.kind1 , reslin_list.kind2))
                else:
                    reslin_list.zipreis =  to_decimal("0")

        if not direct_change and not rate_readonly and current_rate != 0 and reslin_list.zipreis == 0:
            reslin_list.zipreis =  to_decimal(current_rate)

        if rate_found and reslin_list.zipreis == 0 and (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()) and (reslin_list.erwachs > 0 or reslin_list.kind1 > 0):
            reslin_list.gratis = reslin_list.erwachs + reslin_list.kind1
            reslin_list.erwachs = 0
            reslin_list.kind1 = 0


    def check_dynarate():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        datum:date = None
        loopdate:date = None

        res_dynarate = query(res_dynarate_data, first=True)

        if not res_dynarate:

            return

        elif res_dynarate and res_dynarate.date1 == None and res_dynarate.date1 == None:

            return

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_dynarate.argt)]})

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (9200 + res_dynarate.setup))]})

        queasy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, res_dynarate.markno)]})

        if queasy:
            f_resline.currency = queasy.char3

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, queasy.char3)]})
            reslin_list.betriebsnr = waehrung.waehrungsnr


        reslin_list.ankunft = res_dynarate.date1
        reslin_list.arrangement = res_dynarate.argt
        reslin_list.reserve_int = res_dynarate.markno
        f_resline.zikatstr = res_dynarate.rmcat
        f_resline.rate_zikat = res_dynarate.rmcat
        f_resline.marknr = res_dynarate.markno
        f_resline.contcode = res_dynarate.prcode
        f_resline.origcontcode = res_dynarate.rcode
        f_resline.combo_code = res_dynarate.rcode

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, res_dynarate.rmcat)]})

        if zimkateg:
            reslin_list.zikatnr = zimkateg.zikatnr
            reslin_list.l_zuordnung[0] = zimkateg.zikatnr

        if reslin_list.gratis == 0:
            reslin_list.erwachs = res_dynarate.adult
            reslin_list.kind1 = res_dynarate.child

        if reslin_list.setup == 0:
            reslin_list.setup = res_dynarate.setup
            f_resline.c_setup = substring(paramtext.notes, 0, 1)

        if res_dynarate.rate < 0:
            reslin_list.zipreis =  - to_decimal(res_dynarate.rate)
        else:
            reslin_list.zipreis =  to_decimal(res_dynarate.rate)

        res_dynarate = query(res_dynarate_data, last=True)
        reslin_list.abreise = res_dynarate.date2 + timedelta(days=1)

        if dayuse_flag:
            reslin_list.abreise = reslin_list.ankunft
        reslin_list.anztage = (reslin_list.abreise - reslin_list.ankunft).days
        f_resline.arrday = weekdays[get_weekday(reslin_list.ankunft) - 1]
        f_resline.depday = weekdays[get_weekday(reslin_list.abreise) - 1]

        for res_dynarate in query(res_dynarate_data):
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "arrangement"
            reslin_queasy.resnr = inp_resnr
            reslin_queasy.reslinnr = f_resline.reslinnr
            reslin_queasy.date1 = res_dynarate.date1
            reslin_queasy.date2 = res_dynarate.date2
            reslin_queasy.deci1 =  to_decimal(res_dynarate.rate)
            reslin_queasy.char2 = res_dynarate.prcode
            reslin_queasy.char3 = user_init

            if reslin_queasy.deci1 < 0:
                reslin_queasy.deci1 =  - to_decimal(reslin_queasy.deci1)
                res_dynarate_data.remove(res_dynarate)
            f_resline.fixed_rate = True

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, f_resline.origcontcode)]})
        f_resline.restricted = None != queasy and queasy.logi2

        if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("qci").lower()) and f_resline.restricted:
            reslin_list.zimmer_wunsch = reslin_list.zimmer_wunsch +\
                "restricted;"


    def calc_periode(resno:int, reslinnr:int):

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        periode_rsv1:date = None
        periode_rsv2:date = None
        counter:int = 0
        periode:date = None
        loopi:date = None
        tqueasy = None
        bbresline = None
        Tqueasy =  create_buffer("Tqueasy",Queasy)
        Bbresline =  create_buffer("Bbresline",Res_line)

        tqueasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, resno)],"logi1": [(eq, True)]})

        if tqueasy:

            bbresline = get_cache (Res_line, {"resnr": [(eq, resno),(eq, reslinnr)]})
            periode_rsv1 = bbresline.ankunft
            periode_rsv2 = bbresline.abreise

            if get_month(periode_rsv1) + 1 > 12:
                periode = date_mdy(1, get_day(periode_rsv1) , get_year(periode_rsv1) + timedelta(days=1) - 1)


            else:
                periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1, get_day(periode_rsv1) , get_year(periode_rsv1)) - 1)


            for loopi in date_range(periode_rsv1,periode_rsv2 - 1) :

                if loopi > periode:
                    periode_rsv1 = loopi

                    if get_month(periode_rsv1) + 1 > 12:
                        periode = date_mdy(1, get_day(periode_rsv1) , get_year(periode_rsv1) + timedelta(days=1) - 1)


                    else:
                        periode = date_mdy(get_month(periode_rsv1) + timedelta(days=1, get_day(periode_rsv1) , get_year(periode_rsv1)) - 1)

                if loopi <= periode:

                    periode_list = query(periode_list_data, filters=(lambda periode_list: periode_list.periode1 == periode_rsv1), first=True)

                    if not periode_list:
                        periode_list = Periode_list()
                        periode_list_data.append(periode_list)

                        periode_list.periode1 = periode_rsv1
                        counter = counter + 1
                        periode_list.counter = counter


                    periode_list.periode2 = loopi

            for periode_list in query(periode_list_data):
                periode_list.diff_day = (periode_list.periode2 - periode_list.periode1 + 1).days

                if periode_list.diff_day >= 30:
                    periode_list.amt_periode =  to_decimal(tqueasy.deci1) / to_decimal(periode_list.diff_day)
                    periode_list.tamount =  to_decimal(periode_list.amt_periode) * to_decimal(periode_list.diff_day)


                else:
                    periode_list.amt_periode = ( to_decimal(tqueasy.deci1) * to_decimal(12)) / to_decimal("365")
                    periode_list.tamount =  to_decimal(periode_list.amt_periode) * to_decimal(periode_list.diff_day)


    def check_bedsetup1():

        nonlocal msg_str, error_flag, record_use, init_time, init_date, avail_gdpr, avail_mark, avail_news, save_gdpr, curr_date, serv_date, f_resline_data, curr_resline_data, reslin_list_data, reschanged_list_data, t_history_data, rline_list_data, weekdays, i, str, loopi, loopj, str1, foreign_nr, tokcounter, iftask, mestoken, mesvalue, rcode, prevcode, do_it, do_it1, flag_ok, dayuse_flag, split_modify, logic_p1109, priscilla_active, loopk, resbemerk, lvcarea, new_reslinnr, curr_time, res_line, history, zimkateg, ratecode, zimmer, guest, queasy, htparam, nation, bediener, master, reslin_queasy, reservation, kontline, gentable, outorder, arrangement, guest_pr, pricecod, prmarket, fixleist, paramtext, waehrung, katpreis
        nonlocal pvilanguage, res_mode, session_date, user_init, inp_gastnr, inp_resnr, inp_reslinnr, rate_readonly, qci_zinr
        nonlocal resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy


        nonlocal rline_list, reslin_list, curr_resline, t_history, currency_list, res_dynarate, reschanged_list, f_resline, nation_list, periode_list, resline, resbuff, zimkateg1, rbuff, qci_zimmer, bresline, bguest, bqueasy, qsy
        nonlocal rline_list_data, reslin_list_data, curr_resline_data, t_history_data, currency_list_data, reschanged_list_data, f_resline_data, nation_list_data, periode_list_data

        anz_setup:int = 0
        curr_setup:int = 0

        if reslin_list.setup == 0 and zimkateg:

            for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.zikatnr == zimkateg.zikatnr) & (Zimmer.setup != 0)).order_by(Zimmer.setup).yield_per(100):

                if curr_setup == 0:
                    curr_setup = zimmer.setup
                    anz_setup = 1

                if zimmer.setup != curr_setup:
                    anz_setup = 2
                    break

            if anz_setup == 1:
                reslin_list.setup = curr_setup

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, (9200 + curr_setup))]})
                f_resline.c_setup = substring(paramtext.notes, 0, 1)

    if res_mode == "split+modify":
        res_mode = "modify"
        split_modify = True

    if num_entries(res_mode, chr_unicode(2)) > 1:

        if entry(1, res_mode, chr_unicode(2)) == ("DU").lower() :
            dayuse_flag = True
        res_mode = entry(0, res_mode, chr_unicode(2))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 346)]})

    if htparam and htparam.bezeichnung.lower()  != ("not used").lower() :
        avail_gdpr = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 466)]})

        if htparam:
            save_gdpr = htparam.finteger

    if avail_gdpr:

        nation_obj_list = {}
        nation = Nation()
        queasy = Queasy()
        for nation.nationnr, nation.kurzbez, nation.bezeich, nation._recid, queasy.logi1, queasy._recid, queasy.char3 in db_session.query(Nation.nationnr, Nation.kurzbez, Nation.bezeich, Nation._recid, Queasy.logi1, Queasy._recid, Queasy.char3).join(Queasy,(Queasy.key == 6) & (Queasy.number1 == Nation.untergruppe) & (matches(Queasy.char1,"*europe*"))).filter(
                 (Nation.natcode == 0)).order_by(Nation.kurzbez).all():
            if nation_obj_list.get(nation._recid):
                continue
            else:
                nation_obj_list[nation._recid] = True


            nation_list = Nation_list()
            nation_list_data.append(nation_list)

            nation_list.nr = nation.nationnr
            nation_list.kurzbez = nation.kurzbez
            nation_list.bezeich = entry(0, nation.bezeich, ";")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 477)]})

    if htparam and htparam.bezeichnung.lower()  != ("not used").lower() :
        avail_mark = htparam.flogical
        avail_news = htparam.flogical
    flag_ok, init_time, init_date = get_output(check_timebl(1, inp_resnr, inp_reslinnr, "res-line", None, None))

    if not flag_ok:
        error_flag = True
        record_use = True

        return generate_output()

    if qci_zinr != "":

        qci_zimmer = get_cache (Zimmer, {"zinr": [(eq, qci_zinr)]})
    f_resline = F_resline()
    f_resline_data.append(f_resline)


    if res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("inhouse").lower() :

        resbuff = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

        if not resbuff:
            msg_str = translateExtended ("Reservation is being modified by other user.", lvcarea, "")
            error_flag = True

            return generate_output()

        if res_mode.lower()  == ("modify").lower()  and resbuff.active_flag == 1:
            msg_str = translateExtended ("Guest already checked-in.", lvcarea, "")
            error_flag = True

            return generate_output()
    f_resline.new_contrate = get_output(htplogic(550))
    f_resline.price_decimal = get_output(htpint(491))
    curr_date = get_output(htpdate(87))
    f_resline.billdate = get_output(htpdate(110))
    f_resline.foreign_rate = get_output(htplogic(143))
    f_resline.res_status = get_output(htpint(478))
    f_resline.oral_flag = get_output(htplogic(938))
    f_resline.six_pm = get_output(htpint(297))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1355)]})

    if htparam.flogical  and htparam.bezeichnung.lower()  != ("not used").lower() :
        f_resline.ci_date = get_current_date()
        f_resline.billdate = get_current_date()


    else:
        f_resline.ci_date = curr_date

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    master = get_cache (Master, {"resnr": [(eq, inp_resnr)]})
    f_resline.master_exist = None != master

    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})
    f_resline.main_resname = guest.name


    f_resline.karteityp = guest.karteityp

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "rate-prog")],"char1": [(eq, "")],"reslinnr": [(eq, 1)],"number1": [(eq, inp_resnr)],"number2": [(eq, 0)]})

    if reslin_queasy:
        f_resline.prog_str = reslin_queasy.char3

    if res_mode.lower()  == ("earlyci").lower() :
        f_resline.earlyci = True
        res_mode = "modify"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 472)]})

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        f_resline.param472 = htparam.flogical


    f_resline.allot_tooltip = translateExtended ("Allotment", lvcarea, "")

    if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("qci").lower() :

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == inp_resnr)).order_by(Res_line.reslinnr.desc()).yield_per(100):
            new_reslinnr = res_line.reslinnr + 1
            break
        f_resline.reslinnr = new_reslinnr

    elif res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("inhouse").lower() :

        res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, inp_resnr)]})

        if res_line.kontignr > 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"kontstatus": [(eq, 1)]})

            if kontline:
                f_resline.allot_tooltip = translateExtended ("Allotment Code", lvcarea, "")

        elif res_line.kontignr < 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, - res_line.kontignr)],"kontstatus": [(eq, 1)]})

            if kontline:
                f_resline.allot_tooltip = translateExtended ("Global Reservation Code", lvcarea, "")
        curr_resline = Curr_resline()
        curr_resline_data.append(curr_resline)

        buffer_copy(res_line, curr_resline)

        gentable = get_cache (Gentable, {"key": [(eq, "reservation")],"number1": [(eq, inp_resnr)],"number2": [(eq, inp_reslinnr)]})
        f_resline.gentable = None != gentable

        resline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"active_flag": [(le, 1)],"kontakt_nr": [(eq, res_line.reslinnr)],"l_zuordnung[2]": [(eq, 1)]})

        if resline:
            f_resline.accompany_gastnr = resline.gastnrmember

        if resline:

            curr_recid = resline._recid
            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline._recid > curr_recid)).first()

        if resline:
            f_resline.accompany_gastnr2 = resline.gastnrmember

        if resline:

            curr_recid = resline._recid
            resline = db_session.query(Resline).filter(
                     (Resline.resnr == res_line.resnr) & (Resline.active_flag <= 1) & (Resline.kontakt_nr == res_line.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline._recid > curr_recid)).first()

        if resline:
            f_resline.accompany_gastnr3 = resline.gastnrmember

        if session_date.lower()  == ("dmy").lower() :
            f_resline.rsv_tooltip = substring(res_line.reserve_char, 6, 2) + "/" +\
                substring(res_line.reserve_char, 3, 2) + "/" +\
                substring(res_line.reserve_char, 0, 2) + " " +\
                substring(res_line.reserve_char, 8, 5) + " " +\
                substring(res_line.reserve_char, 13)

        elif session_date_format() == ("mdy").lower() :
            f_resline.rsv_tooltip = substring(res_line.reserve_char, 3, 2) + "/" +\
                substring(res_line.reserve_char, 6, 2) + "/" +\
                substring(res_line.reserve_char, 0, 2) + " " +\
                substring(res_line.reserve_char, 8, 5) + " " +\
                substring(res_line.reserve_char, 13)


        else:
            f_resline.rsv_tooltip = substring(res_line.reserve_char, 0, 8) + " " +\
                substring(res_line.reserve_char, 8, 5) + " " +\
                substring(res_line.reserve_char, 13)

        if res_mode.lower()  == ("modify").lower()  and (res_line.resstatus <= 2 or res_line.resstatus == 5) and res_line.zinr != "":

            outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"betriebsnr": [(eq, res_line.resnr)]})
            f_resline.offmarket = None != outorder

        if res_line.code != "" and res_line.code.lower()  != ("0").lower() :
            f_resline.bill_instruct = to_int(res_line.code)

            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, bill_instruct)]})

            if queasy:
                f_resline.instruct_str = queasy.char1
        f_resline.guestnr = res_line.gastnrpay
        f_resline.reslinnr = inp_reslinnr
        f_resline.grpflag = res_line.grpflag
        f_resline.rline_bemerk = res_line.bemerk
        f_resline.res_bemerk = reservation.bemerk
        f_resline.kontignr = res_line.kontignr
        f_resline.zimmeranz = res_line.zimmeranz
        f_resline.sharer = (res_line.resstatus == 11) or (res_line.resstatus == 13)

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            f_resline.zikatstr = zimkateg.kurzbez

    elif res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("split").lower() :
        f_resline.reslinnr = 1
        f_resline.tot_qty = 0

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == inp_resnr)).order_by(Res_line._recid).all():

            if f_resline.guestnr == 0:
                f_resline.guestnr = res_line.gastnrpay

            if res_line.reslinnr > f_resline.reslinnr:
                f_resline.reslinnr = res_line.reslinnr
            f_resline.grpflag = res_line.grpflag
            f_resline.tot_qty = f_resline.tot_qty + res_line.zimmeranz
        f_resline.reslinnr = f_resline.reslinnr + 1
    logic_p1109 = get_output(htplogic(1109))
    f_resline.res_bemerk = f_resline.res_bemerk +\
            chr_unicode(2) + to_string(to_int(logic_p1109))


    resbemerk = ""


    for loopk in range(1,length(f_resline.res_bemerk)  + 1) :

        if asc(substring(f_resline.res_bemerk, loopk - 1, 1)) == 0 or asc(substring(f_resline.res_bemerk, loopk, 1)) > 255:
            pass
        else:
            resbemerk = resbemerk + substring(f_resline.res_bemerk, loopk - 1, 1)
    f_resline.res_bemerk = resbemerk

    if length(f_resline.res_bemerk) < 3:
        f_resline.res_bemerk = replace_str(f_resline.res_bemerk, chr_unicode(32) , "")

    if length(f_resline.res_bemerk) == None:
        f_resline.res_bemerk = ""
    resbemerk = ""


    for loopk in range(1,length(f_resline.rline_bemerk)  + 1) :

        if asc(substring(f_resline.rline_bemerk, loopk - 1, 1)) == 0 or asc(substring(f_resline.rline_bemerk, loopk, 1)) > 255:
            pass
        else:
            resbemerk = resbemerk + substring(f_resline.rline_bemerk, loopk - 1, 1)
    f_resline.rline_bemerk = resbemerk

    if length(f_resline.rline_bemerk) < 3:
        f_resline.rline_bemerk = replace_str(f_resline.rline_bemerk, chr_unicode(32) , "")

    if length(f_resline.rline_bemerk) == None:
        f_resline.rline_bemerk = ""

    if res_mode.lower()  == ("split").lower() :
        split_resline()

    if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
        f_resline.bill_instruct = 0
        f_resline.instruct_str = ""

        guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})
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
        res_line.abreise = res_line.ankunft + timedelta(days=1)
        res_line.anztage = 1
        res_line.zimmeranz = 1
        res_line.name = guest.name
        res_line.resname = f_resline.main_resname
        res_line.erwachs = 1
        res_line.gratis = 0
        res_line.grpflag = f_resline.grpflag
        res_line.active_flag = 2
        res_line.resstatus = 12

        htparam = get_cache (Htparam, {"paramnr": [(eq, 262)]})

        if htparam.finteger != 0:
            res_line.erwachs = htparam.finteger

        if res_mode.lower()  == ("insert").lower() :

            resline = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"l_zuordnung[2]": [(eq, 0)]})

            if resline:

                if resline.active_flag == 0:
                    res_line.ankunft = resline.ankunft
                    res_line.abreise = resline.abreise
                    res_line.anztage = (res_line.abreise - res_line.ankunft).days

                elif resline.active_flag == 1:
                    res_line.abreise = resline.abreise
                    res_line.anztage = (res_line.abreise - res_line.ankunft).days

        htparam = get_cache (Htparam, {"paramnr": [(eq, 150)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, htparam.finteger)]})

        if zimkateg:
            f_resline.zikatstr = zimkateg.kurzbez
            res_line.zikatnr = zimkateg.zikatnr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 151)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, htparam.fchar)]})

        if arrangement:
            res_line.arrangement = arrangement.arrangement


        f_resline.curr_arg = res_line.arrangement


    reslin_list = Reslin_list()
    reslin_list_data.append(reslin_list)

    reslin_list.reserve_dec =  to_decimal("0")
    reslin_list.resnr = inp_resnr

    if res_mode.lower()  != ("split").lower() :

        guest = get_cache (Guest, {"gastnr": [(eq, f_resline.guestnr)]})
        f_resline.billname = guest.name + ", " + guest.vorname1 +\
                guest.anredefirma +\
                " " + guest.anrede1
        f_resline.billadress = guest.adresse1
        f_resline.billcity = guest.wohnort + " " + guest.plz

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

        if nation:
            f_resline.billland = nation.bezeich


        f_resline.name_editor = f_resline.billname + chr_unicode(10) + chr_unicode(10) +\
                f_resline.billadress + chr_unicode(10) +\
                f_resline.billcity + chr_unicode(10) + chr_unicode(10) +\
                f_resline.billland
        f_resline.zahlungsart = guest.zahlungsart

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        f_resline.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1

        guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})

        if qci_zimmer:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, qci_zimmer.zikatnr)]})
        else:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            f_resline.zikatstr = zimkateg.kurzbez


        f_resline.curr_arg = res_line.arrangement


        buffer_copy(res_line, reslin_list)
        reslin_list.bemerk = replace_str(reslin_list.bemerk, chr_unicode(10) , "")


        reslin_list.bemerk = replace_str(reslin_list.bemerk, chr_unicode(13) , "")
        reslin_list.bemerk = replace_str(reslin_list.bemerk, "~n", "")
        reslin_list.bemerk = replace_str(reslin_list.bemerk, "\\n", "")
        reslin_list.bemerk = replace_str(reslin_list.bemerk, "~r", "")
        reslin_list.bemerk = replace_str(reslin_list.bemerk, "~r~n", "")
        reslin_list.bemerk = replace_str(reslin_list.bemerk, chr_unicode(10) + chr_unicode(13) , "")
        resbemerk = " "


        for loopk in range(1,length(reslin_list.bemerk)  + 1) :

            if asc(substring(reslin_list.bemerk, loopk - 1, 1)) == 0 or asc(substring(reslin_list.bemerk, loopk, 1)) > 255:
                pass
            else:
                resbemerk = resbemerk + substring(reslin_list.bemerk, loopk - 1, 1)
        reslin_list.bemerk = resbemerk

        if length(reslin_list.bemerk) < 3:
            reslin_list.bemerk = replace_str(reslin_list.bemerk, chr_unicode(32) , "")

        if length(reslin_list.bemerk) == None:
            reslin_list.bemerk = ""

        if qci_zimmer:
            reslin_list.setup = qci_zimmer.setup
            reslin_list.zinr = qci_zimmer.zinr


        f_resline.arrday = weekdays[get_weekday(reslin_list.ankunft) - 1]
        f_resline.depday = weekdays[get_weekday(reslin_list.abreise) - 1]
        f_resline.comchild = reslin_list.l_zuordnung[3]
        f_resline.pickup_flag = matches(reslin_list.zimmer_wunsch, ("*pickup*"))
        f_resline.drop_flag = matches(reslin_list.zimmer_wunsch, ("*drop-passanger*"))
        f_resline.marknr = reslin_list.reserve_int


        if reslin_list.l_zuordnung[0] != 0:

            zimkateg1 = get_cache (Zimkateg, {"zikatnr": [(eq, reslin_list.l_zuordnung[0])]})

            if zimkateg1:
                f_resline.rate_zikat = zimkateg1.kurzbez

        if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :

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

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
        fill_flightnr()

    if matches(res_line.memozinr,r"*;*"):
        f_resline.memo_zinr = entry(1, res_line.memozinr, ";")

    if f_resline.new_contrate:
        f_resline.ebdisc_flag = matches(reslin_list.zimmer_wunsch, ("*ebdisc*"))
        f_resline.kbdisc_flag = matches(reslin_list.zimmer_wunsch, ("*kbdisc*"))
        f_resline.restricted = matches(reslin_list.zimmer_wunsch, ("*restricted*"))


    curr_time = get_current_time_in_seconds()

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, inp_gastnr)]})

    if guest_pr:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 2) & (Queasy.logi2) & (Queasy.char1 == guest_pr.code)).first()

        if queasy:

            if f_resline.new_contrate:
                while None != guest_pr:

                    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

                    if queasy:
                        do_it = True

                        if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()):

                            if f_resline.ci_date < queasy.date1:
                                do_it = False

                            elif f_resline.ci_date > queasy.date2:
                                do_it = False

                        if do_it:

                            ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)],"endperiode": [(ge, f_resline.ci_date)]})

                            if ratecode:
                                f_resline.enable_frate = True

                                if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower()) and reslin_list.reserve_int == 0 and ratecode.marknr > 0:
                                    reslin_list.reserve_int = ratecode.marknr
                                    f_resline.contcode = ratecode.code
                                    f_resline.origcontcode = ratecode.code

                            ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)],"char1[0]": [(ne, "")]})

                            if ratecode:
                                f_resline.enable_ebdisc = True

                            ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)],"char1[1]": [(ne, "")]})

                            if ratecode:
                                f_resline.enable_kbdisc = True

                    curr_recid = guest_pr._recid
                    guest_pr = db_session.query(Guest_pr).filter(
                             (Guest_pr.gastnr == inp_gastnr) & (Guest_pr._recid > curr_recid)).first()
            else:

                pricecod = get_cache (Pricecod, {"code": [(eq, guest_pr.code)],"endperiode": [(ge, f_resline.ci_date)]})

                if pricecod:
                    f_resline.enable_frate = True
    for i in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
        str = entry(i - 1, reslin_list.zimmer_wunsch, ";")

        if substring(str, 0, 7) == ("voucher").lower() :
            f_resline.voucher = substring(str, 7)

        elif substring(str, 0, 5) == ("ChAge").lower() :
            f_resline.child_age = substring(str, 5)

        elif substring(str, 0, 6) == ("$CODE$").lower() :
            f_resline.contcode = substring(str, 6)

        elif substring(str, 0, 5) == ("DATE,").lower() :
            f_resline.bookdate = date_mdy(to_int(substring(str, 9, 2)) , to_int(substring(str, 11, 2)) , to_int(substring(str, 5, 4)))

        elif substring(str, 0, 8) == ("SEGM_PUR").lower() :
            f_resline.i_purpose = to_int(substring(str, 8))

        elif matches(str,r"*WCI-req*"):
            str1 = entry(1, str, "=")


            for loopi in range(1,num_entries(str1, ",")  + 1) :

                queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, to_int(entry(loopi - 1, str1, ",")))]})

                if queasy:
                    for loopj in range(1,num_entries(queasy.char1, ";")  + 1) :

                        if matches(entry(loopj - 1, queasy.char1, ";"),r"*en*"):
                            f_resline.wci_flag = entry(1, entry(loopj - 1, queasy.char1, ";") , "=") + ", " + f_resline.wci_flag


                            break

        elif substring(str, 0, 4) == ("GDPR").lower() :
            f_resline.gdpr_flag = substring(str, 4)

        elif substring(str, 0, 9) == ("MARKETING").lower() :
            f_resline.mark_flag = substring(str, 9)

        elif substring(str, 0, 10) == ("NEWSLETTER").lower() :
            f_resline.news_flag = substring(str, 10)

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

    if reslin_queasy:

        queasy = get_cache (Queasy, {"key": [(eq, 189)]})

        if queasy:
            f_resline.voucher = f_resline.voucher + chr_unicode(2) +\
                reslin_queasy.char3

    if f_resline.contcode != "":

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, f_resline.contcode)]})
        f_resline.combo_code = f_resline.contcode

        if queasy:
            f_resline.tip_code = queasy.char1 + " - " + queasy.char2

            rbuff = get_cache (Ratecode, {"code": [(eq, f_resline.contcode)]})

            if rbuff:

                prmarket = get_cache (Prmarket, {"nr": [(eq, rbuff.marknr)]})

                if prmarket:
                    f_resline.marknr = rbuff.marknr
                    f_resline.tip_code = f_resline.tip_code + " [" +\
                        prmarket.bezeich + "]"

    if (res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("inhouse").lower()) and substring(bediener.permissions, 42, 2) < ("2").lower() :
        f_resline.enable_disc = False

    if res_mode.lower()  == ("modify").lower()  or res_mode.lower()  == ("inhouse").lower()  or res_mode.lower()  == ("split").lower() :
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 10) == ("$OrigCode$").lower() :
                prevcode = substring(str, 10)
                f_resline.origcontcode = prevcode


                break

    if res_line.resstatus != 11 and res_line.resstatus != 13:

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, inp_gastnr)]})

        if guest_pr:

            guest_pr_obj_list = {}
            for guest_pr, queasy in db_session.query(Guest_pr, Queasy).join(Queasy,(Queasy.key == 2) & (Queasy.char1 == Guest_pr.code)).filter(
                     (Guest_pr.gastnr == inp_gastnr) & (Guest_pr.code != f_resline.contcode)).order_by(Queasy.logi2.desc(), Queasy.char1).all():
                if guest_pr_obj_list.get(guest_pr._recid):
                    continue
                else:
                    guest_pr_obj_list[guest_pr._recid] = True


                do_it = True

                if queasy.char1 != prevcode:

                    if f_resline.ci_date < queasy.date1:
                        do_it = False

                    elif f_resline.ci_date > queasy.date2:
                        do_it = False

                if do_it:
                    f_resline.combo_code = f_resline.combo_code + ";" + guest_pr.code

                    if f_resline.contcode == "":
                        f_resline.contcode = guest_pr.code


                        f_resline.tip_code = queasy.char1 + " - " + queasy.char2

                        if queasy.logi2:

                            rbuff = get_cache (Ratecode, {"code": [(eq, f_resline.contcode)]})

                            if rbuff:
                                iftask = rbuff.char1[4]
                            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                                if mestoken == "RC":
                                    rcode = mesvalue

                            if rcode != "":

                                rbuff = get_cache (Ratecode, {"code": [(eq, rcode)]})

                                if rbuff:

                                    qsy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, rbuff.marknr)]})
                        else:

                            rbuff = get_cache (Ratecode, {"code": [(eq, guest_pr.code)]})

                            if rbuff:

                                prmarket = get_cache (Prmarket, {"nr": [(eq, rbuff.marknr)]})

                            if prmarket:
                                f_resline.tip_code = f_resline.tip_code + " [" +\
                                        prmarket.bezeich + "]"

                                qsy = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, prmarket.nr)]})

                        if qsy:

                            currency_list = query(currency_list_data, filters=(lambda currency_list: currency_list.wabkurz == qsy.char3), first=True)

                            if not currency_list:
                                currency_list = Currency_list()
                                currency_list_data.append(currency_list)

                                currency_list.wabkurz = qsy.char3

    if (res_line.resstatus == 11 or res_line.resstatus == 13) and f_resline.contcode == " ":

        bresline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"kontakt_nr": [(eq, res_line.kontakt_nr)]})

        if bresline:
            for i in range(1,num_entries(bresline.zimmer_wunsch, ";") - 1 + 1) :
                str = entry(i - 1, bresline.zimmer_wunsch, ";")

                if substring(str, 0, 6) == ("$CODE$").lower() :
                    f_resline.contcode = substring(str, 6)
                    f_resline.combo_code = f_resline.contcode

    bqueasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, res_line.resnr)],"logi1": [(eq, True)]})

    if bqueasy:
        f_resline.repeat_charge = bqueasy.logi1


    disp_allotment()
    get_currency()
    f_resline.l_ankunft = reslin_list.ankunft
    f_resline.l_abreise = reslin_list.abreise
    f_resline.l_night = reslin_list.anztage

    if reslin_list.active_flag == 0 and reslin_list.zinr != "":

        outorder = get_cache (Outorder, {"zinr": [(eq, reslin_list.zinr)],"betriebsnr": [(eq, reslin_list.resnr)]})
        f_resline.offmarket = None != outorder
    disp_history()
    check_dynarate()
    check_bedsetup()

    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})
    f_resline.fixed_rate = None != reslin_queasy

    if f_resline.fixed_rate and reslin_list.l_zuordnung[0] == 0:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, reslin_list.zikatnr)]})

        if zimkateg:
            f_resline.rate_zikat = zimkateg.kurzbez
            reslin_list.l_zuordnung[0] = zimkateg.zikatnr

    if not f_resline.fixed_rate and (bediener.char1 != ""):
        f_resline.enable_disc = True

    if res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()  or res_mode.lower()  == ("qci").lower() :
        set_roomrate(True)

    if res_mode.lower()  == ("inhouse").lower()  and reslin_list.resstatus == 8:
        set_roomrate(True)

    if not split_modify:
        rline_list_data, reschanged_list_data = get_output(mk_resline_query_q1bl(pvilanguage, True, True, inp_resnr, rline_list_data, reschanged_list_data))

    if f_resline.restricted:
        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("This is Reservation with Restricted Discounted rate", lvcarea, "") + chr_unicode(10) + translateExtended ("Any reservation data changes such as C/i- or C/O-date", lvcarea, "") + chr_unicode(10) + translateExtended ("might have impact to the given room rate.", lvcarea, "") + chr_unicode(10)

    if res_mode.lower()  == ("split").lower() :
        flag_ok, init_time, init_date = get_output(check_timebl(2, inp_resnr, inp_reslinnr, "res-line", init_time, init_date))

    fixleist = get_cache (Fixleist, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

    if fixleist:
        msg_str = msg_str + "FixleistIncluded"

    return generate_output()