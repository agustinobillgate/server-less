from functions.additional_functions import *
import decimal
from datetime import date
from functions.check_timebl import check_timebl
from sqlalchemy import func
from models import Guest, Queasy, Bediener, Mc_guest, Artikel, Gentable, Htparam, Akt_kont, Guestseg, Segment, Guest_pr, Sourccod, History, Genlayout

def prepare_chg_gcf1_1bl(gastnr:int, chg_gcf:bool):
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
    segment1_list = []
    t_guest_list = []
    sourccod1_list = []
    q1_akt_kont_list = []
    q2_history_list = []
    sourccod_chg_list = []
    tqueasy_list = []
    flag_ok:bool = False
    guest = queasy = bediener = mc_guest = artikel = gentable = htparam = akt_kont = guestseg = segment = guest_pr = sourccod = history = genlayout = None

    segment1 = sourccod1 = sourccod_chg = t_guest = q1_akt_kont = q2_history = tqueasy = guest0 = usr = None

    segment1_list, Segment1 = create_model("Segment1", {"bezeich":str})
    sourccod1_list, Sourccod1 = create_model("Sourccod1", {"source_code":int, "bezeich":str})
    sourccod_chg_list, Sourccod_chg = create_model("Sourccod_chg", {"source_code":int, "bezeich":str})
    t_guest_list, T_guest = create_model_like(Guest)
    q1_akt_kont_list, Q1_akt_kont = create_model("Q1_akt_kont", {"name":str, "vorname":str, "anrede":str, "hauptkontakt":bool})
    q2_history_list, Q2_history = create_model("Q2_history", {"ankunft":date, "abreise":date, "zinr":str, "zipreis":decimal, "bemerk":str, "arrangement":str})
    tqueasy_list, Tqueasy = create_model_like(Queasy)

    Guest0 = Guest
    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal record_use, init_time, init_date, avail_mcguest, lname, land, payment, pay_bezeich, master_gastnr, mastername, ref_nr1, ref_nr2, sales_id, sales_name, avail_gentable, avail_genlayout, avail_guestseg, mc_license, maincontact, mainsegm, comments, email_adr, curr_source, pricecode, ena_btn_gcfinfo, f_int, refno_label, segment1_list, t_guest_list, sourccod1_list, q1_akt_kont_list, q2_history_list, sourccod_chg_list, tqueasy_list, flag_ok, guest, queasy, bediener, mc_guest, artikel, gentable, htparam, akt_kont, guestseg, segment, guest_pr, sourccod, history, genlayout
        nonlocal guest0, usr


        nonlocal segment1, sourccod1, sourccod_chg, t_guest, q1_akt_kont, q2_history, tqueasy, guest0, usr
        nonlocal segment1_list, sourccod1_list, sourccod_chg_list, t_guest_list, q1_akt_kont_list, q2_history_list, tqueasy_list
        return {"record_use": record_use, "init_time": init_time, "init_date": init_date, "avail_mcguest": avail_mcguest, "lname": lname, "land": land, "payment": payment, "pay_bezeich": pay_bezeich, "master_gastnr": master_gastnr, "mastername": mastername, "ref_nr1": ref_nr1, "ref_nr2": ref_nr2, "sales_id": sales_id, "sales_name": sales_name, "avail_gentable": avail_gentable, "avail_genlayout": avail_genlayout, "avail_guestseg": avail_guestseg, "mc_license": mc_license, "maincontact": maincontact, "mainsegm": mainsegm, "comments": comments, "email_adr": email_adr, "curr_source": curr_source, "pricecode": pricecode, "ena_btn_gcfinfo": ena_btn_gcfinfo, "f_int": f_int, "refno_label": refno_label, "segment1": segment1_list, "t-guest": t_guest_list, "sourccod1": sourccod1_list, "q1-akt-kont": q1_akt_kont_list, "q2-history": q2_history_list, "sourccod-chg": sourccod_chg_list, "tqueasy": tqueasy_list}

    if chg_gcf:
        flag_ok, init_time, init_date = get_output(check_timebl(1, gastnr, None, "guest", None, None))

        if not flag_ok:
            record_use = True

            return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    mc_guest = db_session.query(Mc_guest).filter(
            (Mc_guest.gastnr == gastnr) &  (Mc_guest.activeflag)).first()

    if mc_guest:
        avail_mcguest = True
    lname = guest.name
    land = guest.land
    payment = guest.zahlungsart

    if payment != 0:

        artikel = db_session.query(Artikel).filter(
                (Artikel.departement == 0) &  (Artikel.artnr == payment)).first()

        if artikel:
            pay_bezeich = artikel.bezeich
    master_gastnr = guest.master_gastnr

    if master_gastnr != 0:

        guest0 = db_session.query(Guest0).filter(
                (Guest0.gastnr == master_gastnr)).first()

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

        usr = db_session.query(Usr).filter(
                (Usr.userinit == sales_id)).first()

        if usr:
            sales_name = usr.username

    gentable = db_session.query(Gentable).filter(
            (func.lower(Gentable.key) == "Guest Card") &  (Gentable.number1 == gastnr)).first()

    if gentable:
        avail_gentable = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()
    mc_license = htparam.flogical

    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == gastnr) &  (Akt_kont.hauptkontakt)).first()

    if akt_kont:
        maincontact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

    for guestseg in db_session.query(Guestseg).filter(
            (Guestseg.gastnr == guest.gastnr)).all():

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            segment1 = Segment1()
            segment1_list.append(segment1)

            segment1.bezeich = segment.bezeich

    guestseg = db_session.query(Guestseg).filter(
            (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()

    if guestseg:

        segment = db_session.query(Segment).filter(
                (Segment.segmentcode == guestseg.segmentcode)).first()

        if segment:
            mainsegm = entry(0, segment.bezeich, "$$0")
    comments = guest.bemerkung
    email_adr = guest.email_adr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 123)).first()
    comments = comments + chr(2) + to_string(htparam.finteger)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 109)).first()
    comments = comments + chr(2) + to_string(htparam.finteger)

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == guest.gastnr)).first()

    if guest_pr:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == guest_pr.code)).first()

        if queasy:
            pricecode = guest_pr.code + "  " + queasy.char2

    if guest.segment3 != 0:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == guest.segment3)).first()

        if sourccod:
            curr_source = to_string(sourccod.source_code) + " " + sourccod.bezeich

    if chg_gcf:

        for sourccod in db_session.query(Sourccod).filter(
                (Sourccod.source_code != guest.segment3)).all():
            sourccod1 = Sourccod1()
            sourccod1_list.append(sourccod1)

            sourccod1.source_code = sourccod.source_code
            sourccod1.bezeich = sourccod.bezeich


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 975)).first()

    if htparam.finteger != 1:
        ena_btn_gcfinfo = True

    for akt_kont in db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == gastnr)).all():
        q1_akt_kont = Q1_akt_kont()
        q1_akt_kont_list.append(q1_akt_kont)

        q1_akt_kont.name = akt_kont.name
        q1_akt_kont.vorname = akt_kont.vorname
        q1_akt_kont.anrede = akt_kont.anrede
        q1_akt_kont.hauptkontakt = akt_kont.hauptkontakt

    for history in db_session.query(History).filter(
            (History.gastnr == gastnr)).all():
        q2_history = Q2_history()
        q2_history_list.append(q2_history)

        q2_history.ankunft = history.ankunft
        q2_history.abreise = history.abreise
        q2_history.zinr = history.zinr
        q2_history.zipreis = history.zipreis
        q2_history.bemerk = history.bemerk
        q2_history.arrangement = history.arrangement

    for sourccod in db_session.query(Sourccod).filter(
            (Sourccod.betriebsnr == 0) &  (Sourccod.source_code != t_guest.segment3)).all():
        sourccod_chg = Sourccod_chg()
        sourccod_chg_list.append(sourccod_chg)

        sourccod_chg.source_code = sourccod.source_code
        sourccod_chg.bezeich = sourccod.bezeich

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 975)).first()
    f_int = htparam.finteger

    guestseg = db_session.query(Guestseg).filter(
            (Guestseg.gastnr == gastnr)).first()

    if guestseg:
        avail_guestseg = True

    genlayout = db_session.query(Genlayout).filter(
            (func.lower(Genlayout.key) == "Guest Card")).first()

    if genlayout:
        avail_genlayout = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1356)).first()

    if htparam:
        refno_label = htparam.fchar

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 231) &  (Queasy.number1 == gastnr)).first()

    if queasy:
        tqueasy = Tqueasy()
        tqueasy_list.append(tqueasy)

        buffer_copy(queasy, tqueasy)

    return generate_output()