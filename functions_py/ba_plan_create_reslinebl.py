#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Guest, Counters, Bk_reser, Bk_raum, Akt_kont, Bk_func, Bk_veran
from sqlalchemy.orm.attributes import flag_modified

def ba_plan_create_reslinebl(curr_resnr:int, guest_gastnr:int, bkl_ftime:int, bkl_ttime:int, 
                             bkl_raum:string, bkl_datum:date, bkl_tdatum:date, bediener_nr:int, ba_dept:int, curr_resstatus:int, user_init:string):

    prepare_cache ([Htparam, Guest, Counters, Bk_reser, Bk_raum, Akt_kont, Bk_func, Bk_veran])

    guest_name = ""
    reslinnr = 0
    main_exist = False
    t_bk_reser1_data = []
    name_contact:string = ""
    telefon_contact:string = ""
    email_contact:string = ""
    ftime:int = 0
    ttime:int = 0
    v_zeit:string = ""
    b_zeit:string = ""
    week_list:List[string] = ["Sunday ", "Monday ", "Tuesday ", "Wednesday", "Thursday ", "Friday ", "Saturday "]
    ci_date:date = None
    htparam = guest = counters = bk_reser = bk_raum = akt_kont = bk_func = bk_veran = None

    t_bk_reser1 = None

    t_bk_reser1_data, T_bk_reser1 = create_model("T_bk_reser1", {"veran_nr":int, "resstatus":int, "datum":date, "bis_datum":date, "raum":string, "von_zeit":string, "bis_zeit":string, "veran_resnr":int})

    db_session = local_storage.db_session
    bkl_raum = bkl_raum.strip()

    def generate_output():
        nonlocal guest_name, reslinnr, main_exist, t_bk_reser1_data, name_contact, telefon_contact, email_contact, ftime, ttime, v_zeit, b_zeit, week_list, ci_date, htparam, guest, counters, bk_reser, bk_raum, akt_kont, bk_func, bk_veran
        nonlocal curr_resnr, guest_gastnr, bkl_ftime, bkl_ttime, bkl_raum, bkl_datum, bkl_tdatum, bediener_nr, ba_dept, curr_resstatus, user_init


        nonlocal t_bk_reser1
        nonlocal t_bk_reser1_data

        return {"curr_resnr": curr_resnr, "guest_name": guest_name, "reslinnr": reslinnr, "main_exist": main_exist, "t-bk-reser1": t_bk_reser1_data}

    def get_reslinnr(resnr:int):

        nonlocal guest_name, reslinnr, main_exist, t_bk_reser1_data, name_contact, telefon_contact, email_contact, ftime, ttime, v_zeit, b_zeit, week_list, ci_date, htparam, guest, counters, bk_reser, bk_raum, akt_kont, bk_func, bk_veran
        nonlocal curr_resnr, guest_gastnr, bkl_ftime, bkl_ttime, bkl_raum, bkl_datum, bkl_tdatum, bediener_nr, ba_dept, curr_resstatus, user_init


        nonlocal t_bk_reser1
        nonlocal t_bk_reser1_data

        reslinnr = 1
        bk_res1 = None

        def generate_inner_output():
            return (reslinnr)

        Bk_res1 =  create_buffer("Bk_res1",Bk_reser)

        for bk_res1 in db_session.query(Bk_res1).filter(
                 (Bk_res1.veran_nr == resnr)).order_by(Bk_res1.veran_resnr.desc()).all():
            reslinnr = bk_res1.veran_resnr + 1

            return generate_inner_output()

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate
    ftime = round ((bkl_ftime / 2) , 0) - 1
    ttime = round ((bkl_ttime / 2) , 0) - 1

    guest = get_cache (Guest, {"gastnr": [(eq, guest_gastnr)]})

    if guest:
        guest_name = guest.name

    if curr_resnr == 0:

        # counters = get_cache (Counters, {"counter_no": [(eq, 16)]})
        counters = db_session.query(Counters).filter(
                 (Counters.counter_no == 16)).with_for_update().first()

        if counters:
            pass
        else:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 16
            counters.counter_bez = "Banquet Reservation No."
        counters.counter = counters.counter + 1
        curr_resnr = counters.counter
        pass
    reslinnr = get_reslinnr(curr_resnr)
    bk_reser = Bk_reser()
    db_session.add(bk_reser)


    if round ((bkl_ftime / 2) - 0.1, 0) * 2 < bkl_ftime:
        bk_reser.von_zeit = to_string(ftime, "99") + "00"
        v_zeit = to_string(ftime, "99") + "00"


    else:
        bk_reser.von_zeit = to_string(ftime, "99") + "30"
        v_zeit = to_string(ftime, "99") + "30"

    if round ((bkl_ttime / 2) - 0.1, 0) * 2 < bkl_ttime:
        bk_reser.bis_zeit = to_string(ttime, "99") + "30"
        b_zeit = to_string(ttime, "99") + "30"


    else:
        bk_reser.bis_zeit = to_string(ttime + 1, "99") + "00"
        b_zeit = to_string(ttime + 1, "99") + "00"


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
    bk_reser.limitdate = ci_date + timedelta(days=10)

    pass

    # bk_raum = get_cache (Bk_raum, {"raum": [(eq, bkl_raum)]})
    bk_raum = db_session.query(Bk_raum).filter(
             (Bk_raum.raum == bkl_raum)).with_for_update().first()

    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest_gastnr)]})

    if akt_kont:
        name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        telefon_contact = akt_kont.telefon
        email_contact = akt_kont.email_adr

    elif guest:
        name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        telefon_contact = guest.telefon
        email_contact = guest.email_adr
    bk_func = Bk_func()
    db_session.add(bk_func)

    bk_func.veran_nr = curr_resnr
    bk_func.veran_seite = reslinnr
    bk_func.resstatus = curr_resstatus
    bk_func.datum = bkl_datum
    bk_func.bis_datum = bkl_tdatum
    bk_func.uhrzeit = to_string(v_zeit, "99:99") + " - " + to_string(b_zeit, "99:99")
    bk_func.wochentag = week_list[get_weekday(bkl_datum) - 1]
    bk_func.auf__datum = ci_date
    bk_func.resnr[0] = curr_resnr
    bk_func.r_resstatus[0] = curr_resstatus
    bk_func.uhrzeiten[0] = to_string(v_zeit, "99:99") + " - " + to_string(b_zeit, "99:99")
    bk_func.vgeschrieben = user_init
    bk_func.vkontrolliert = user_init
    bk_func.betriebsnr = guest_gastnr
    bk_func.veranstalteranschrift[4] = email_contact
    bk_func.v_kontaktperson[0] = name_contact
    bk_func.v_telefon = telefon_contact
    bk_func.v_telefax = telefon_contact
    bk_func.kontaktperson[0] = name_contact
    bk_func.telefon = telefon_contact
    bk_func.telefax = telefon_contact

    if bk_raum:
        bk_func.personen = bk_raum.personen
        bk_func.raeume[0] = bk_raum.raum
        bk_func.rpersonen[0] = bk_raum.personen
        bk_func.rpreis[0] = bk_raum.preis

    if guest:
        bk_func.bestellt__durch = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        bk_func.veranstalteranschrift[0] = guest.adresse1
        bk_func.veranstalteranschrift[1] = guest.adresse2
        bk_func.veranstalteranschrift[2] = guest.adresse3
        bk_func.veranstalteranschrift[3] = guest.land + " - " + guest.plz + " - " + guest.wohnort
        bk_func.adurch = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
        bk_func.rechnungsanschrift[0] = guest.adresse1
        bk_func.rechnungsanschrift[1] = guest.adresse2
        bk_func.rechnungsanschrift[2] = guest.adresse3
        bk_func.rechnungsanschrift[3] = guest.land + " - " + guest.plz + " - " + guest.wohnort
        bk_func.nadkarte[0] = guest.name

    if curr_resstatus == 1:
        bk_func.c_resstatus[0] = "F"

    elif curr_resstatus == 2:
        bk_func.c_resstatus[0] = "T"

    elif curr_resstatus == 3:
        bk_func.c_resstatus[0] = "W"

    flag_modified(bk_func, "c_resstatus")
    flag_modified(bk_func, "resnr")
    flag_modified(bk_func, "r_resstatus")
    flag_modified(bk_func, "uhrzeiten")
    flag_modified(bk_func, "veranstalteranschrift")
    flag_modified(bk_func, "kontaktperson")
    flag_modified(bk_func, "nadkarte")

    # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bk_reser.veran_nr)]})
    bk_veran = db_session.query(Bk_veran).filter(
             (Bk_veran.veran_nr == bk_reser.veran_nr)).with_for_update().first()

    if not bk_veran:
        bk_veran = Bk_veran()
        db_session.add(bk_veran)

        bk_veran.gastnr = guest_gastnr
        bk_veran.gastnrver = guest_gastnr
        bk_veran.veran_nr = curr_resnr
        bk_veran.resnr = reslinnr
        bk_veran.bediener_nr = bediener_nr
        bk_veran.resstatus = curr_resstatus
        bk_veran.departement = ba_dept
        bk_veran.kontaktfirst = ci_date
        bk_veran.resdat = bkl_tdatum
        bk_veran.limit_date = bkl_datum

        if guest:
            bk_veran.payment_userinit[8] = guest.phonetik3 + chr_unicode(2) + guest.phonetik2
        pass
        main_exist = True
    else:

        if bk_veran.resdat < bk_reser.bis_datum:
            bk_veran.resdat = bkl_tdatum
        main_exist = True
        pass
    t_bk_reser1 = T_bk_reser1()
    t_bk_reser1_data.append(t_bk_reser1)

    t_bk_reser1.veran_nr = curr_resnr
    t_bk_reser1.resstatus = curr_resstatus
    t_bk_reser1.datum = bkl_datum
    t_bk_reser1.bis_datum = bkl_tdatum
    t_bk_reser1.raum = bkl_raum
    t_bk_reser1.von_zeit = v_zeit
    t_bk_reser1.bis_zeit = b_zeit
    t_bk_reser1.veran_resnr = reslinnr
    flag_modified(bk_veran, "payment_userinit")
    
    return generate_output()