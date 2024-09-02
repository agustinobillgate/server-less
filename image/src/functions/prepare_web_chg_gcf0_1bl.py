from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.check_timebl import check_timebl
from models import Guest, Guestbook, Genlayout, Htparam, Nation, Mc_guest, Gentable, Queasy, Artikel, Guestseg, Segment, History, Zimmer, Zimkateg, Akt_kont, Res_line

def prepare_web_chg_gcf0_1bl(gastnr:int, chg_gcf:bool, master_gastnr:int):
    read_birthdate = False
    def_natcode = ""
    avail_mc_guest = False
    avail_gentable = False
    mc_license = False
    pay_bezeich = ""
    payment = 0
    mainsegm = ""
    mastername = ""
    fname_flag = False
    f_int = 0
    avail_queasy = False
    record_use = False
    init_time = 0
    init_date = None
    avail_genlayout = False
    l_param472 = False
    logic_param1109 = False
    base64imagefile = ""
    t_segment1_list = []
    t_guest_list = []
    t_nation1_list = []
    t_nation2_list = []
    t_nation3_list = []
    q2_history_list = []
    q1_akt_kont_list = []
    forecast_list = []
    t_guestbook_list = []
    flag_ok:bool = False
    pointer:bytes = None
    ci_date:date = get_current_date()
    guest = guestbook = genlayout = htparam = nation = mc_guest = gentable = queasy = artikel = guestseg = segment = history = zimmer = zimkateg = akt_kont = res_line = None

    t_nation1 = t_nation2 = t_nation3 = q1_akt_kont = q2_history = t_segment1 = t_guest = forecast = t_guestbook = guest0 = None

    t_nation1_list, T_nation1 = create_model("T_nation1", {"kurzbez":str})
    t_nation2_list, T_nation2 = create_model_like(T_nation1)
    t_nation3_list, T_nation3 = create_model_like(T_nation1)
    q1_akt_kont_list, Q1_akt_kont = create_model("Q1_akt_kont", {"name":str, "vorname":str, "anrede":str, "hauptkontakt":bool})
    q2_history_list, Q2_history = create_model("Q2_history", {"ankunft":date, "abreise":date, "zinr":str, "zipreis":decimal, "kurzbez":str, "bemerk":str, "arrangement":str})
    t_segment1_list, T_segment1 = create_model("T_segment1", {"bezeich":str})
    t_guest_list, T_guest = create_model_like(Guest)
    forecast_list, Forecast = create_model("Forecast", {"ankunft":date, "abreise":date, "zinr":str, "kurzbez":str, "arrangement":str, "zipreis":decimal})
    t_guestbook_list, T_guestbook = create_model_like(Guestbook)

    Guest0 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal read_birthdate, def_natcode, avail_mc_guest, avail_gentable, mc_license, pay_bezeich, payment, mainsegm, mastername, fname_flag, f_int, avail_queasy, record_use, init_time, init_date, avail_genlayout, l_param472, logic_param1109, base64imagefile, t_segment1_list, t_guest_list, t_nation1_list, t_nation2_list, t_nation3_list, q2_history_list, q1_akt_kont_list, forecast_list, t_guestbook_list, flag_ok, pointer, ci_date, guest, guestbook, genlayout, htparam, nation, mc_guest, gentable, queasy, artikel, guestseg, segment, history, zimmer, zimkateg, akt_kont, res_line
        nonlocal guest0


        nonlocal t_nation1, t_nation2, t_nation3, q1_akt_kont, q2_history, t_segment1, t_guest, forecast, t_guestbook, guest0
        nonlocal t_nation1_list, t_nation2_list, t_nation3_list, q1_akt_kont_list, q2_history_list, t_segment1_list, t_guest_list, forecast_list, t_guestbook_list
        return {"read_birthdate": read_birthdate, "def_natcode": def_natcode, "avail_mc_guest": avail_mc_guest, "avail_gentable": avail_gentable, "mc_license": mc_license, "pay_bezeich": pay_bezeich, "payment": payment, "mainsegm": mainsegm, "mastername": mastername, "fname_flag": fname_flag, "f_int": f_int, "avail_queasy": avail_queasy, "record_use": record_use, "init_time": init_time, "init_date": init_date, "avail_genlayout": avail_genlayout, "l_param472": l_param472, "logic_param1109": logic_param1109, "base64imagefile": base64imagefile, "t-segment1": t_segment1_list, "t-guest": t_guest_list, "t-nation1": t_nation1_list, "t-nation2": t_nation2_list, "t-nation3": t_nation3_list, "q2-history": q2_history_list, "q1-akt-kont": q1_akt_kont_list, "forecast": forecast_list, "t-guestbook": t_guestbook_list}

    genlayout = db_session.query(Genlayout).filter(
            (func.lower(Genlayout.key) == "Guest Card")).first()

    if genlayout:
        avail_genlayout = True

    if chg_gcf:
        flag_ok, init_time, init_date = get_output(check_timebl(1, gastnr, None, "guest", None, None))

        if not flag_ok:
            record_use = True

            return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    master_gastnr = guest.master_gastnr


    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    guestbook = db_session.query(Guestbook).filter(
            (Guestbook.gastnr == gastnr)).first()

    if guestbook:
        t_guestbook = T_guestbook()
        t_guestbook_list.append(t_guestbook)

        buffer_copy(guestbook, t_guestbook)
        pointer = guestbook.imagefile        
        # base64imagefile = BASE64_ENCODE (pointer)
        base64imagefile = base64_encode(pointer)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 472)).first()

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        l_param472 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1109)).first()
    logic_param1109 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 937)).first()
    read_birthdate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 153)).first()

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == htparam.fchar)).first()

    if not nation:

        return generate_output()
    def_natcode = nation.kurzbez

    mc_guest = db_session.query(Mc_guest).filter(
            (Mc_guest.gastnr == gastnr) &  
            (Mc_guest.activeflag)).first()

    if mc_guest:
        avail_mc_guest = True

    gentable = db_session.query(Gentable).filter(
            (func.lower(Gentable.key) == "Guest Card".lower()) &  
            (Gentable.number1 == gastnr)
            ).first()

    if gentable:
        avail_gentable = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()
    mc_license = htparam.flogical

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 27)).first()
    avail_queasy = None != queasy
    payment = guest.zahlungsart

    if payment != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  
                (Artikel.artnr == payment)
                ).first()

        if artikel:
            pay_bezeich = artikel.bezeich

    for guestseg in db_session.query(Guestseg).filter(
            (Guestseg.gastnr == guest.gastnr)).all():

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            t_segment1 = T_segment1()
            t_segment1_list.append(t_segment1)

            t_segment1.bezeich = segment.bezeich

    guestseg = db_session.query(Guestseg).filter(
            (Guestseg.gastnr == guest.gastnr) &  
            (Guestseg.reihenfolge == 1)).first()

    if guestseg:

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            mainsegm = entry(0, segment.bezeich, "$$0")

    if master_gastnr != 0:

        guest0 = db_session.query(Guest0).filter(
                (Guest0.gastnr == master_gastnr)).first()

        if guest0:
            mastername = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1
        else:
            master_gastnr = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 939)).first()
    fname_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 975)).first()
    f_int = htparam.finteger

    for history in db_session.query(History).filter(
            (History.gastnr == gastnr)).all():
        q2_history = Q2_history()
        q2_history_list.append(q2_history)

        buffer_copy(history, q2_history)

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == history.zinr)).first()

        if zimmer:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == zimmer.zikatnr)).first()

            if zimkateg:
                q2_history.kurzbez = zimkateg.kurzbez

    for akt_kont in db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == gastnr)).all():
        q1_akt_kont = Q1_akt_kont()
        q1_akt_kont_list.append(q1_akt_kont)

        buffer_copy(akt_kont, q1_akt_kont)

    for nation in db_session.query(Nation).filter(
            (Nation.natcode == 0)).all():
        t_nation1 = T_nation1()
        t_nation1_list.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).filter(
            (Nation.natcode > 0)).all():
        t_nation2 = T_nation2()
        t_nation2_list.append(t_nation2)

        t_nation2.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).all():
        t_nation3 = T_nation3()
        t_nation3_list.append(t_nation3)

        t_nation3.kurzbez = nation.kurzbez

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()

    if htparam:
        ci_date = htparam.fdate

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    if guest:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.gastnrmember == guest.gastnr) &  
                (((Res_line.ankunft >= ci_date) &  
                  (Res_line.resstatus <= 5)
                  ) |  
                  (Res_line.resstatus == 6) |  
                  (Res_line.resstatus == 11) |  
                  (Res_line.resstatus == 13))
                ).all():
            forecast = Forecast()
            forecast_list.append(forecast)

            buffer_copy(res_line, forecast)

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if zimmer:

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == zimmer.zikatnr)).first()

                if zimkateg:
                    forecast.kurzbez = zimkateg.kurzbez

    return generate_output()