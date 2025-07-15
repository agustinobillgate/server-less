#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from models import Guest, Queasy, Bediener, Mc_guest, Artikel, Gentable, Htparam, Akt_kont, Guestseg, Segment, Guest_pr, Sourccod, History, Genlayout

def prepare_chg_gcf1_1bl(gastnr:int, chg_gcf:bool):

    prepare_cache ([Guest, Bediener, Artikel, Htparam, Akt_kont, Guestseg, Segment, Guest_pr, Sourccod, History])

    record_use = False
    init_time = 0
    init_date = None
    avail_mcguest = False
    lname = ""
    land = ""
    payment = 0
    pay_bezeich = ""
    master_gastnr = 0
    mastername = ""
    ref_nr1 = 0
    ref_nr2 = 0
    sales_id = ""
    sales_name = ""
    avail_gentable = False
    avail_genlayout = False
    avail_guestseg = False
    mc_license = False
    maincontact = ""
    mainsegm = ""
    comments = ""
    email_adr = ""
    curr_source = ""
    pricecode = ""
    ena_btn_gcfinfo = False
    f_int = 0
    refno_label = ""
    segment1_data = []
    t_guest_data = []
    sourccod1_data = []
    q1_akt_kont_data = []
    q2_history_data = []
    sourccod_chg_data = []
    tqueasy_data = []
    flag_ok:bool = False
    guest = queasy = bediener = mc_guest = artikel = gentable = htparam = akt_kont = guestseg = segment = guest_pr = sourccod = history = genlayout = None

    segment1 = sourccod1 = sourccod_chg = t_guest = q1_akt_kont = q2_history = tqueasy = guest0 = usr = None

    segment1_data, Segment1 = create_model("Segment1", {"bezeich":string})
    sourccod1_data, Sourccod1 = create_model("Sourccod1", {"source_code":int, "bezeich":string})
    sourccod_chg_data, Sourccod_chg = create_model("Sourccod_chg", {"source_code":int, "bezeich":string})
    t_guest_data, T_guest = create_model_like(Guest)
    q1_akt_kont_data, Q1_akt_kont = create_model("Q1_akt_kont", {"name":string, "vorname":string, "anrede":string, "hauptkontakt":bool})
    q2_history_data, Q2_history = create_model("Q2_history", {"ankunft":date, "abreise":date, "zinr":string, "zipreis":Decimal, "bemerk":string, "arrangement":string})
    tqueasy_data, Tqueasy = create_model_like(Queasy)

    Guest0 = create_buffer("Guest0",Guest)
    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal record_use, init_time, init_date, avail_mcguest, lname, land, payment, pay_bezeich, master_gastnr, mastername, ref_nr1, ref_nr2, sales_id, sales_name, avail_gentable, avail_genlayout, avail_guestseg, mc_license, maincontact, mainsegm, comments, email_adr, curr_source, pricecode, ena_btn_gcfinfo, f_int, refno_label, segment1_data, t_guest_data, sourccod1_data, q1_akt_kont_data, q2_history_data, sourccod_chg_data, tqueasy_data, flag_ok, guest, queasy, bediener, mc_guest, artikel, gentable, htparam, akt_kont, guestseg, segment, guest_pr, sourccod, history, genlayout
        nonlocal gastnr, chg_gcf
        nonlocal guest0, usr


        nonlocal segment1, sourccod1, sourccod_chg, t_guest, q1_akt_kont, q2_history, tqueasy, guest0, usr
        nonlocal segment1_data, sourccod1_data, sourccod_chg_data, t_guest_data, q1_akt_kont_data, q2_history_data, tqueasy_data

        return {"record_use": record_use, "init_time": init_time, "init_date": init_date, "avail_mcguest": avail_mcguest, "lname": lname, "land": land, "payment": payment, "pay_bezeich": pay_bezeich, "master_gastnr": master_gastnr, "mastername": mastername, "ref_nr1": ref_nr1, "ref_nr2": ref_nr2, "sales_id": sales_id, "sales_name": sales_name, "avail_gentable": avail_gentable, "avail_genlayout": avail_genlayout, "avail_guestseg": avail_guestseg, "mc_license": mc_license, "maincontact": maincontact, "mainsegm": mainsegm, "comments": comments, "email_adr": email_adr, "curr_source": curr_source, "pricecode": pricecode, "ena_btn_gcfinfo": ena_btn_gcfinfo, "f_int": f_int, "refno_label": refno_label, "segment1": segment1_data, "t-guest": t_guest_data, "sourccod1": sourccod1_data, "q1-akt-kont": q1_akt_kont_data, "q2-history": q2_history_data, "sourccod-chg": sourccod_chg_data, "tqueasy": tqueasy_data}

    if chg_gcf:
        flag_ok, init_time, init_date = get_output(check_timebl(1, gastnr, None, "guest", None, None))

        if not flag_ok:
            record_use = True

            return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    t_guest = T_guest()
    t_guest_data.append(t_guest)

    buffer_copy(guest, t_guest)

    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastnr)],"activeflag": [(eq, True)]})

    if mc_guest:
        avail_mcguest = True
    lname = guest.name
    land = guest.land
    payment = guest.zahlungsart

    if payment != 0:

        artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, payment)]})

        if artikel:
            pay_bezeich = artikel.bezeich
    master_gastnr = guest.master_gastnr

    if master_gastnr != 0:

        guest0 = get_cache (Guest, {"gastnr": [(eq, master_gastnr)]})

        if guest0:
            mastername = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1
        else:
            master_gastnr = 0
    ref_nr1 = guest.firmen_nr

    if ref_nr1 == None:
        ref_nr1 = 0
    ref_nr2 = guest.point_gastnr
    sales_id = guest.phonetik3

    if sales_id != "":

        usr = get_cache (Bediener, {"userinit": [(eq, sales_id)]})

        if usr:
            sales_name = usr.username

    gentable = get_cache (Gentable, {"key": [(eq, "guest card")],"number1": [(eq, gastnr)]})

    if gentable:
        avail_gentable = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})
    mc_license = htparam.flogical

    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastnr)],"hauptkontakt": [(eq, True)]})

    if akt_kont:
        maincontact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

    for guestseg in db_session.query(Guestseg).filter(
             (Guestseg.gastnr == guest.gastnr)).order_by(Guestseg._recid).all():

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

        if segment:
            segment1 = Segment1()
            segment1_data.append(segment1)

            segment1.bezeich = segment.bezeich

    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

    if guestseg:

        segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

        if segment:
            mainsegm = entry(0, segment.bezeich, "$$0")
    comments = guest.bemerkung
    email_adr = guest.email_adr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
    comments = comments + chr_unicode(2) + to_string(htparam.finteger)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
    comments = comments + chr_unicode(2) + to_string(htparam.finteger)

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

    if guest_pr:

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

        if queasy:
            pricecode = guest_pr.code + " " + queasy.char2

    if guest.segment3 != 0:

        sourccod = get_cache (Sourccod, {"source_code": [(eq, guest.segment3)]})

        if sourccod:
            curr_source = to_string(sourccod.source_code) + " " + sourccod.bezeich

    if chg_gcf:

        for sourccod in db_session.query(Sourccod).filter(
                 (Sourccod.source_code != guest.segment3)).order_by(Sourccod.source_code).all():
            sourccod1 = Sourccod1()
            sourccod1_data.append(sourccod1)

            sourccod1.source_code = sourccod.source_code
            sourccod1.bezeich = sourccod.bezeich


    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

    if htparam.finteger != 1:
        ena_btn_gcfinfo = True

    for akt_kont in db_session.query(Akt_kont).filter(
             (Akt_kont.gastnr == gastnr)).order_by(Akt_kont.hauptkontakt.desc(), Akt_kont.name).all():
        q1_akt_kont = Q1_akt_kont()
        q1_akt_kont_data.append(q1_akt_kont)

        q1_akt_kont.name = akt_kont.name
        q1_akt_kont.vorname = akt_kont.vorname
        q1_akt_kont.anrede = akt_kont.anrede
        q1_akt_kont.hauptkontakt = akt_kont.hauptkontakt

    for history in db_session.query(History).filter(
             (History.gastnr == gastnr)).order_by(History.ankunft.desc()).all():
        q2_history = Q2_history()
        q2_history_data.append(q2_history)

        q2_history.ankunft = history.ankunft
        q2_history.abreise = history.abreise
        q2_history.zinr = history.zinr
        q2_history.zipreis =  to_decimal(history.zipreis)
        q2_history.bemerk = history.bemerk
        q2_history.arrangement = history.arrangement

    for sourccod in db_session.query(Sourccod).filter(
             (Sourccod.betriebsnr == 0) & (Sourccod.source_code != t_guest.segment3)).order_by(Sourccod.source_code).all():
        sourccod_chg = Sourccod_chg()
        sourccod_chg_data.append(sourccod_chg)

        sourccod_chg.source_code = sourccod.source_code
        sourccod_chg.bezeich = sourccod.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})
    f_int = htparam.finteger

    guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastnr)]})

    if guestseg:
        avail_guestseg = True

    genlayout = get_cache (Genlayout, {"key": [(eq, "guest card")]})

    if genlayout:
        avail_genlayout = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1356)]})

    if htparam:
        refno_label = htparam.fchar

    queasy = get_cache (Queasy, {"key": [(eq, 231)],"number1": [(eq, gastnr)]})

    if queasy:
        tqueasy = Tqueasy()
        tqueasy_data.append(tqueasy)

        buffer_copy(queasy, tqueasy)

    return generate_output()