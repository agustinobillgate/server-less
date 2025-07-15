#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Guest, Guestbook, Genlayout, Htparam, Nation, Mc_guest, Gentable, Queasy, Artikel, Guestseg, Segment, History, Zimmer, Zimkateg, Akt_kont, Res_line

def prepare_web_chg_gcf0_1bl(gastnr:int, chg_gcf:bool, master_gastnr:int):

    prepare_cache ([Guest, Htparam, Nation, Artikel, Guestseg, Segment, Zimmer, Zimkateg])

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
    t_segment1_data = []
    t_guest_data = []
    t_nation1_data = []
    t_nation2_data = []
    t_nation3_data = []
    q2_history_data = []
    q1_akt_kont_data = []
    forecast_data = []
    t_guestbook_data = []
    flag_ok:bool = False
    pointer:bytes = None
    ci_date:date = get_current_date()
    guest = guestbook = genlayout = htparam = nation = mc_guest = gentable = queasy = artikel = guestseg = segment = history = zimmer = zimkateg = akt_kont = res_line = None

    t_nation1 = t_nation2 = t_nation3 = q1_akt_kont = q2_history = t_segment1 = t_guest = forecast = t_guestbook = guest0 = None

    t_nation1_data, T_nation1 = create_model("T_nation1", {"kurzbez":string})
    t_nation2_data, T_nation2 = create_model_like(T_nation1)
    t_nation3_data, T_nation3 = create_model_like(T_nation1)
    q1_akt_kont_data, Q1_akt_kont = create_model("Q1_akt_kont", {"name":string, "vorname":string, "anrede":string, "hauptkontakt":bool})
    q2_history_data, Q2_history = create_model("Q2_history", {"ankunft":date, "abreise":date, "zinr":string, "zipreis":Decimal, "kurzbez":string, "bemerk":string, "arrangement":string})
    t_segment1_data, T_segment1 = create_model("T_segment1", {"bezeich":string})
    t_guest_data, T_guest = create_model_like(Guest)
    forecast_data, Forecast = create_model("Forecast", {"ankunft":date, "abreise":date, "zinr":string, "kurzbez":string, "arrangement":string, "zipreis":Decimal})
    t_guestbook_data, T_guestbook = create_model_like(Guestbook)

    Guest0 = create_buffer("Guest0",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal read_birthdate, def_natcode, avail_mc_guest, avail_gentable, mc_license, pay_bezeich, payment, mainsegm, mastername, fname_flag, f_int, avail_queasy, record_use, init_time, init_date, avail_genlayout, l_param472, logic_param1109, base64imagefile, t_segment1_data, t_guest_data, t_nation1_data, t_nation2_data, t_nation3_data, q2_history_data, q1_akt_kont_data, forecast_data, t_guestbook_data, flag_ok, pointer, ci_date, guest, guestbook, genlayout, htparam, nation, mc_guest, gentable, queasy, artikel, guestseg, segment, history, zimmer, zimkateg, akt_kont, res_line
        nonlocal gastnr, chg_gcf, master_gastnr
        nonlocal guest0


        nonlocal t_nation1, t_nation2, t_nation3, q1_akt_kont, q2_history, t_segment1, t_guest, forecast, t_guestbook, guest0
        nonlocal t_nation1_data, t_nation2_data, t_nation3_data, q1_akt_kont_data, q2_history_data, t_segment1_data, t_guest_data, forecast_data, t_guestbook_data

        return {"master_gastnr": master_gastnr, "read_birthdate": read_birthdate, "def_natcode": def_natcode, "avail_mc_guest": avail_mc_guest, "avail_gentable": avail_gentable, "mc_license": mc_license, "pay_bezeich": pay_bezeich, "payment": payment, "mainsegm": mainsegm, "mastername": mastername, "fname_flag": fname_flag, "f_int": f_int, "avail_queasy": avail_queasy, "record_use": record_use, "init_time": init_time, "init_date": init_date, "avail_genlayout": avail_genlayout, "l_param472": l_param472, "logic_param1109": logic_param1109, "base64imagefile": base64imagefile, "t-segment1": t_segment1_data, "t-guest": t_guest_data, "t-nation1": t_nation1_data, "t-nation2": t_nation2_data, "t-nation3": t_nation3_data, "q2-history": q2_history_data, "q1-akt-kont": q1_akt_kont_data, "forecast": forecast_data, "t-guestbook": t_guestbook_data}

    genlayout = get_cache (Genlayout, {"key": [(eq, "guest card")]})

    if genlayout:
        avail_genlayout = True

    if chg_gcf:
        flag_ok, init_time, init_date = get_output(check_timebl(1, gastnr, None, "guest", None, None))

        if not flag_ok:
            record_use = True

            return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    master_gastnr = guest.master_gastnr


    t_guest = T_guest()
    t_guest_data.append(t_guest)

    buffer_copy(guest, t_guest)

    guestbook = get_cache (Guestbook, {"gastnr": [(eq, gastnr)]})

    if guestbook:
        t_guestbook = T_guestbook()
        t_guestbook_data.append(t_guestbook)

        buffer_copy(guestbook, t_guestbook)
        pointer = guestbook.imagefile
        base64imagefile = base64_encode(pointer)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 472)]})

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        l_param472 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1109)]})
    logic_param1109 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 937)]})
    read_birthdate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

    if not nation:

        return generate_output()
    def_natcode = nation.kurzbez

    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastnr)],"activeflag": [(eq, True)]})

    if mc_guest:
        avail_mc_guest = True

    gentable = get_cache (Gentable, {"key": [(eq, "guest card")],"number1": [(eq, gastnr)]})

    if gentable:
        avail_gentable = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})
    mc_license = htparam.flogical

    queasy = get_cache (Queasy, {"key": [(eq, 27)]})
    avail_queasy = None != queasy
    payment = guest.zahlungsart

    if payment != 0:

        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, payment)]})

        if artikel:
            pay_bezeich = artikel.bezeich

    for guestseg in db_session.query(Guestseg).filter(
             (Guestseg.gastnr == guest.gastnr)).order_by(Guestseg._recid).all():

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

        if segment:
            t_segment1 = T_segment1()
            t_segment1_data.append(t_segment1)

            t_segment1.bezeich = segment.bezeich

    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

    if guestseg:

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

        if segment:
            mainsegm = entry(0, segment.bezeich, "$$0")

    if master_gastnr != 0:

        guest0 = get_cache (Guest, {"gastnr": [(eq, master_gastnr)]})

        if guest0:
            mastername = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1
        else:
            master_gastnr = 0

    htparam = get_cache (Htparam, {"paramnr": [(eq, 939)]})
    fname_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})
    f_int = htparam.finteger

    for history in db_session.query(History).filter(
             (History.gastnr == gastnr)).order_by(History._recid).all():
        q2_history = Q2_history()
        q2_history_data.append(q2_history)

        buffer_copy(history, q2_history)

        zimmer = get_cache (Zimmer, {"zinr": [(eq, history.zinr)]})

        if zimmer:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zimkateg:
                q2_history.kurzbez = zimkateg.kurzbez

    for akt_kont in db_session.query(Akt_kont).filter(
             (Akt_kont.gastnr == gastnr)).order_by(Akt_kont.hauptkontakt.desc(), Akt_kont.name).all():
        q1_akt_kont = Q1_akt_kont()
        q1_akt_kont_data.append(q1_akt_kont)

        buffer_copy(akt_kont, q1_akt_kont)

    for nation in db_session.query(Nation).filter(
             (Nation.natcode == 0)).order_by(Nation._recid).all():
        t_nation1 = T_nation1()
        t_nation1_data.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).filter(
             (Nation.natcode > 0)).order_by(Nation._recid).all():
        t_nation2 = T_nation2()
        t_nation2_data.append(t_nation2)

        t_nation2.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation3 = T_nation3()
        t_nation3_data.append(t_nation3)

        t_nation3.kurzbez = nation.kurzbez

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnrmember == guest.gastnr) & (((Res_line.ankunft >= ci_date) & (Res_line.resstatus <= 5)) | (Res_line.resstatus == 6) | (Res_line.resstatus == 11) | (Res_line.resstatus == 13))).order_by(Res_line._recid).all():
            forecast = Forecast()
            forecast_data.append(forecast)

            buffer_copy(res_line, forecast)

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if zimmer:

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                if zimkateg:
                    forecast.kurzbez = zimkateg.kurzbez

    return generate_output()