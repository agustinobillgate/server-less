from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Guest, Counters, Bk_reser, Bk_raum, Akt_kont, Bk_func, Bk_veran

def ba_plan_create_reslinebl(curr_resnr:int, guest_gastnr:int, bkl_ftime:int, bkl_ttime:int, bkl_raum:str, bkl_datum:date, bkl_tdatum:date, bediener_nr:int, ba_dept:int, curr_resstatus:int, user_init:str):
    guest_name = ""
    reslinnr = 0
    main_exist = False
    t_bk_reser1_list = []
    name_contact:str = ""
    telefon_contact:str = ""
    email_contact:str = ""
    ftime:int = 0
    ttime:int = 0
    week_list:[str] = ["", "", "", "", "", "", "", ""]
    ci_date:date = None
    htparam = guest = counters = bk_reser = bk_raum = akt_kont = bk_func = bk_veran = None

    t_bk_reser1 = bk_res1 = None

    t_bk_reser1_list, T_bk_reser1 = create_model("T_bk_reser1", {"veran_nr":int, "resstatus":int, "datum":date, "bis_datum":date, "raum":str, "von_zeit":str, "bis_zeit":str, "veran_resnr":int})

    Bk_res1 = Bk_reser

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, reslinnr, main_exist, t_bk_reser1_list, name_contact, telefon_contact, email_contact, ftime, ttime, week_list, ci_date, htparam, guest, counters, bk_reser, bk_raum, akt_kont, bk_func, bk_veran
        nonlocal bk_res1


        nonlocal t_bk_reser1, bk_res1
        nonlocal t_bk_reser1_list
        return {"guest_name": guest_name, "reslinnr": reslinnr, "main_exist": main_exist, "t-bk-reser1": t_bk_reser1_list}

    def get_reslinnr(resnr:int):

        nonlocal guest_name, reslinnr, main_exist, t_bk_reser1_list, name_contact, telefon_contact, email_contact, ftime, ttime, week_list, ci_date, htparam, guest, counters, bk_reser, bk_raum, akt_kont, bk_func, bk_veran
        nonlocal bk_res1


        nonlocal t_bk_reser1, bk_res1
        nonlocal t_bk_reser1_list

        reslinnr = 0

        def generate_inner_output():
            return reslinnr
        Bk_res1 = Bk_reser

        for bk_res1 in db_session.query(Bk_res1).filter(
                (Bk_res1.veran_nr == resnr)).all():
            reslinnr = bk_res1.veran_resnr + 1

            return generate_inner_output()


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    ftime = round ((bkl_ftime / 2) , 0) - 1
    ttime = round ((bkl_ttime / 2) , 0) - 1

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == guest_gastnr)).first()
    guest_name = guest.name

    if curr_resnr == 0:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 16)).first()

        if counters:

            counters = db_session.query(Counters).first()
        else:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 16
            counters.counter_bez = "Banquet Reservation No."
        counters = counters + 1

        counters = db_session.query(Counters).first()
        curr_resnr = counters
    reslinnr = get_reslinnr(curr_resnr)
    bk_reser = Bk_reser()
    db_session.add(bk_reser)


    if round ((bkl_ftime / 2) - 0.1, 0) * 2 < bkl_ftime:
        bk_reser.von_zeit = to_string(ftime, "99") + "00"
    else:
        bk_reser.von_zeit = to_string(ftime, "99") + "30"

    if round ((bkl_ttime / 2) - 0.1, 0) * 2 < bkl_ttime:
        bk_reser.bis_zeit = to_string(ttime, "99") + "30"
    else:
        bk_reser.bis_zeit = to_string(ttime + 1, "99") + "00"
    bk_reser.von_i = bkl_ftime
    bk_reser.bis_i = bkl_ttime
    bk_reser.raum = bkl_raum
    bk_reser.departement = ba_dept
    bk_reser.resstatus = curr_resstatus
    bk_reser.datum = bkl_datum
    bk_reser.bis_datum = bkl_tdatum
    bk_reser.bediener_nr = bediener_nr
    bk_reser.veran_nr = curr_resnr
    bk_reser.veran_resnr = reslinnr
    bk_reser.veran_seite = reslinnr
    bk_reser.limitdate = ci_date + 10


    pass

    bk_reser = db_session.query(Bk_reser).first()

    bk_raum = db_session.query(Bk_raum).filter(
            (func.lower(Bk_raum.raum) == (bkl_raum).lower())).first()

    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == guest.gastnr)).first()

    if akt_kont:
        name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        telefon_contact = akt_kont.telefon
        email_contact = akt_kont.email_adr
    else:
        name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        telefon_contact = guest.telefon
        email_contact = guest.email_adr
    bk_func = Bk_func()
    db_session.add(bk_func)

    bk_func.veran_nr = bk_reser.veran_nr
    bk_func.veran_seite = reslinnr
    bk_func.resstatus = bk_reser.resstatus
    bk_func.datum = bk_reser.datum
    bk_func.bis_datum = bk_reser.bis_datum
    bk_func.uhrzeit = to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99")
    bk_func.wochentag = week_list[get_weekday(bk_reser.datum) - 1]
    bk_func.personen = bk_raum.personen
    bk_func.bestellt__durch = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
    bk_func.veranstalteranschrift[0] = adresse1
    bk_func.veranstalteranschrift[1] = adresse2
    bk_func.veranstalteranschrift[2] = adresse3
    bk_func.veranstalteranschrift[3] = guest.land + " - " + guest.plz + " - " + guest.wohnort
    bk_func.veranstalteranschrift[4] = email_contact
    bk_func.v_kontaktperson[0] = name_contact
    bk_func.v_telefon = telefon_contact
    bk_func.v_telefax = telefon_contact
    bk_func.adurch = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
    bk_func.rechnungsanschrift[0] = guest.adresse1
    bk_func.rechnungsanschrift[1] = guest.adresse2
    bk_func.rechnungsanschrift[2] = guest.adresse3
    bk_func.rechnungsanschrift[3] = guest.land + " - " + guest.plz + " - " + guest.wohnort
    bk_func.kontaktperson[0] = name_contact
    bk_func.telefon = telefon_contact
    bk_func.telefax = telefon_contact
    bk_func.auf__datum = ci_date
    bk_func.nadkarte[0] = guest.name
    bk_func.resnr[0] = bk_reser.veran_resnr
    bk_func.r_resstatus[0] = bk_reser.resstatus
    bk_func.raeume[0] = bk_raum.raum
    bk_func.uhrzeiten[0] = to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99")
    bk_func.rpersonen[0] = bk_raum.personen
    bk_func.rpreis[0] = bk_raum.preis
    bk_func.vgeschrieben = user_init
    bk_func.vkontrolliert = user_init
    bk_func.betriebsnr = guest.gastnr

    if bk_reser.resstatus == 1:
        bk_func.c_resstatus[0] = "F"

    elif bk_reser.resstatus == 2:
        bk_func.c_resstatus[0] = "T"

    elif bk_reser.resstatus == 3:
        bk_func.c_resstatus[0] = "W"

    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == bk_reser.veran_nr)).first()

    if not bk_veran:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate
        bk_veran = Bk_veran()
        db_session.add(bk_veran)

        bk_veran.gastnr = guest.gastnr
        bk_veran.gastnrver = guest.gastnr
        bk_veran.veran_nr = bk_reser.veran_nr
        bk_veran.resnr = bk_reser.veran_resnr
        bk_veran.bediener_nr = bediener_nr
        bk_veran.resstatus = bk_reser.resstatus
        bk_veran.departement = ba_dept
        bk_veran.kontaktfirst = ci_date
        bk_veran.resdat = bk_reser.bis_datum
        bk_veran.limit_date = bk_reser.datum
        bk_veran.payment_userinit[8] = guest.phonetik3 + chr(2) + guest.phonetik2

        bk_veran = db_session.query(Bk_veran).first()
        main_exist = True
    else:

        if bk_veran.resdat < bk_reser.bis_datum:
            bk_veran.resdat = bk_reser.bis_datum
        main_exist = True

        bk_veran = db_session.query(Bk_veran).first()
    t_bk_reser1 = T_bk_reser1()
    t_bk_reser1_list.append(t_bk_reser1)

    t_bk_reser1.veran_nr = bk_reser.veran_nr
    t_bk_reser1.resstatus = bk_reser.resstatus
    t_bk_reser1.datum = bk_reser.datum
    t_bk_reser1.bis_datum = bk_reser.bis_datum
    t_bk_reser1.raum = bk_reser.raum
    t_bk_reser1.von_zeit = bk_reser.von_zeit
    t_bk_reser1.bis_zeit = bk_reser.bis_zeit
    t_bk_reser1.veran_resnr = bk_reser.veran_resnr

    return generate_output()