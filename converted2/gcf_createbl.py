#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Akt_kont, Guest, Segment, Guestseg, Htparam, Akt_cust, Bediener, Res_history

guest_list_data, Guest_list = create_model("Guest_list", {"guest_nr":int, "guest_nr2":int, "guest_name":string, "guest_title":string, "address1":string, "address2":string, "address3":string, "city":string, "zip":string, "country":string, "mastercomp":string, "salesid":string, "salesid_name":string, "refno2":string, "refno3":string, "phone":string, "telefax":string, "email":string, "maincontact":string, "main_fname":string, "main_tittle":string, "main_bday":date, "main_bplace":string, "main_telp":string, "main_ext":string, "main_dept":string, "main_function":string, "main_email":string, "segmentcode":string, "refno4":string, "keyaccount":string, "delflag":bool, "karteityp":int})

def gcf_createbl(user_init:string, guest_list_data:[Guest_list]):

    prepare_cache ([Queasy, Akt_kont, Guest, Segment, Guestseg, Bediener, Res_history])

    curr_gastnr:int = 0
    nr:int = 0
    kont_nr:int = 0
    queasy = akt_kont = guest = segment = guestseg = htparam = akt_cust = bediener = res_history = None

    guest_list = t_queasy = b_queasy = b_akt = None

    T_queasy = create_buffer("T_queasy",Queasy)
    B_queasy = create_buffer("B_queasy",Queasy)
    B_akt = create_buffer("B_akt",Akt_kont)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_gastnr, nr, kont_nr, queasy, akt_kont, guest, segment, guestseg, htparam, akt_cust, bediener, res_history
        nonlocal user_init
        nonlocal t_queasy, b_queasy, b_akt


        nonlocal guest_list, t_queasy, b_queasy, b_akt

        return {}

    def gcf_create():

        nonlocal curr_gastnr, nr, kont_nr, queasy, akt_kont, guest, segment, guestseg, htparam, akt_cust, bediener, res_history
        nonlocal user_init
        nonlocal t_queasy, b_queasy, b_akt


        nonlocal guest_list, t_queasy, b_queasy, b_akt


        curr_gastnr = 0

        if curr_gastnr == 0:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr != None)).order_by(Guest._recid.desc()).first()

            if guest:
                curr_gastnr = guest.gastnr + 1
            else:
                curr_gastnr = 1

        for guest_list in query(guest_list_data, filters=(lambda guest_list: guest_list.guest_nr == 0)):
            guest = Guest()
            db_session.add(guest)

            guest.gastnr = curr_gastnr
            guest.karteityp = guest_list.karteityp
            guest.name = guest_list.guest_name
            guest.anredefirma = guest_list.guest_title
            guest.adresse1 = guest_list.address1
            guest.adresse2 = guest_list.address2
            guest.adresse3 = guest_list.address3
            guest.wohnort = guest_list.city
            guest.plz = entry(0, guest_list.zip, ".")
            guest.land = guest_list.country
            guest.phonetik3 = entry(0, guest_list.salesid, ".")
            guest.point_gastnr = to_int(guest_list.refno2)
            guest.steuernr = guest_list.refno3
            guest.telefon = entry(0, guest_list.phone, ".")
            guest.fax = entry(0, guest_list.telefax, ".")
            guest.email_adr = guest_list.email

            if guest_list.maincontact != "":
                kont_nr = 0

                for b_akt in db_session.query(B_akt).filter(
                         (B_akt.gastnr == curr_gastnr)).order_by(B_akt._recid).all():

                    if b_akt.kontakt_nr > kont_nr:
                        kont_nr = b_akt.kontakt_nr

                akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, curr_gastnr)],"hauptkontakt": [(eq, True)]})

                if not akt_kont:
                    kont_nr = kont_nr + 1
                    akt_kont = Akt_kont()
                    db_session.add(akt_kont)

                    akt_kont.gastnr = curr_gastnr
                    akt_kont.name = guest_list.maincontact
                    akt_kont.vorname = guest_list.main_fname
                    akt_kont.anrede = guest_list.main_tittle
                    akt_kont.geburtdatum1 = guest_list.main_bday
                    akt_kont.geburt_ort1 = guest_list.main_bplace
                    akt_kont.telefon = entry(0, guest_list.main_telp, ".")
                    akt_kont.durchwahl = guest_list.main_ext
                    akt_kont.abteilung = guest_list.main_dept
                    akt_kont.funktion = guest_list.main_function
                    akt_kont.email_adr = guest_list.main_email
                    akt_kont.hauptkontakt = True
                    akt_kont.kontakt_nr = kont_nr
                    akt_kont.kategorie = 1


                else:
                    kont_nr = kont_nr + 1
                    akt_kont = Akt_kont()
                    db_session.add(akt_kont)

                    akt_kont.gastnr = curr_gastnr
                    akt_kont.name = guest_list.maincontact
                    akt_kont.vorname = guest_list.main_fname
                    akt_kont.anrede = guest_list.main_tittle
                    akt_kont.geburtdatum1 = guest_list.main_bday
                    akt_kont.geburt_ort1 = guest_list.main_bplace
                    akt_kont.telefon = entry(0, guest_list.main_telp, ".")
                    akt_kont.durchwahl = guest_list.main_ext
                    akt_kont.abteilung = guest_list.main_dept
                    akt_kont.funktion = guest_list.main_function
                    akt_kont.email_adr = guest_list.main_email
                    akt_kont.hauptkontakt = True
                    akt_kont.kontakt_nr = kont_nr
                    akt_kont.kategorie = 1

            if guest_list.segmentcode != "":

                segment = db_session.query(Segment).filter(
                         (entry(0, Segment.bezeich, "$$0") == guest_list.segmentcode)).first()

                if segment:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, curr_gastnr)],"reihenfolge": [(eq, 1)]})

                    if not guestseg:
                        guestseg = Guestseg()
                        db_session.add(guestseg)

                        guestseg.gastnr = curr_gastnr
                        guestseg.reihenfolge = 1
                        guestseg.segmentcode = segment.segmentcode

            if guest_list.salesid != "":

                htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})

                if htparam.flogical:

                    akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, curr_gastnr)]})

                    if not akt_cust:
                        akt_cust = Akt_cust()
                        db_session.add(akt_cust)

                        akt_cust.gastnr = curr_gastnr
                        akt_cust.c_init = user_init
                        akt_cust.userinit = guest_list.salesid


                    else:

                        if akt_cust.userinit == guest_list.salesid:
                            pass
                        else:
                            pass
                            akt_cust.c_init = user_init
                            akt_cust.userinit = guest_list.salesid


                            pass
            else:

                akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, curr_gastnr)],"userinit": [(eq, guest_list.salesid)]})

                if akt_cust:
                    db_session.delete(akt_cust)
                    pass

            if guest_list.refno4 != "":

                queasy = get_cache (Queasy, {"key": [(eq, 231)],"number1": [(eq, curr_gastnr)]})

                if queasy:
                    queasy.char1 = guest_list.refno4


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 231
                    queasy.number1 = curr_gastnr
                    queasy.char1 = guest_list.refno4

            if guest_list.keyaccount != "":

                b_queasy = get_cache (Queasy, {"key": [(eq, 211)],"char1": [(eq, guest_list.keyaccount)]})

                if b_queasy:

                    for t_queasy in db_session.query(T_queasy).filter(
                             (T_queasy.key == 212) & (T_queasy.number1 == b_queasy.number1)).order_by(T_queasy.number2.desc()).yield_per(100):
                        nr = t_queasy.number2 + 1
                        break

                    t_queasy = get_cache (Queasy, {"key": [(eq, 212)],"number3": [(eq, curr_gastnr)]})

                    if not t_queasy:
                        t_queasy = Queasy()
                        db_session.add(t_queasy)

                        t_queasy.key = 212
                        t_queasy.number1 = b_queasy.number1
                        t_queasy.number2 = nr
                        t_queasy.char1 = guest_list.guest_name
                        t_queasy.number3 = curr_gastnr

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Create GuestCard: GastNo " + to_string(curr_gastnr) +\
                    " " + guest_list.guest_name
            res_history.action = "GuestFile"


            pass
            pass
            curr_gastnr = curr_gastnr + 1

    gcf_create()

    return generate_output()