from functions.additional_functions import *
import decimal
from datetime import date
from functions.read_bedienerbl import read_bedienerbl
from models import Bediener, Guest, Queasy, Guestseg, Segment, Akt_kont

def export_gcfbl(cardtype:int, crm_flag:bool):
    guest_list_list = []
    nr:int = 0
    mastername:str = ""
    sales_name:str = ""
    mainsegm:str = ""
    bediener = guest = queasy = guestseg = segment = akt_kont = None

    guest_list = usr = masterguest = t_queasy = b_queasy = None

    guest_list_list, Guest_list = create_model("Guest_list", {"nr":int, "guest_nr":int, "guest_name":str, "guest_title":str, "address1":str, "address2":str, "address3":str, "city":str, "zip":str, "country":str, "mastercomp":str, "salesid":str, "salesid_name":str, "refno2":str, "refno3":str, "phone":str, "telefax":str, "email":str, "maincontact":str, "main_fname":str, "main_tittle":str, "main_bday":date, "main_bplace":str, "main_telp":str, "main_ext":str, "main_dept":str, "main_function":str, "main_email":str, "segmentcode":str, "tot_room":int, "tot_revenue":decimal, "tot_room_revenue":decimal, "tot_fb_revenue":decimal, "tot_otherrevenue":decimal, "refno4":str, "keyaccount":str})
    usr_list, Usr = create_model_like(Bediener)

    Masterguest = create_buffer("Masterguest",Guest)
    T_queasy = create_buffer("T_queasy",Queasy)
    B_queasy = create_buffer("B_queasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_list_list, nr, mastername, sales_name, mainsegm, bediener, guest, queasy, guestseg, segment, akt_kont
        nonlocal cardtype, crm_flag
        nonlocal masterguest, t_queasy, b_queasy


        nonlocal guest_list, usr, masterguest, t_queasy, b_queasy
        nonlocal guest_list_list, usr_list
        return {"guest-list": guest_list_list}


    guest = db_session.query(Guest).filter(
             (Guest.karteityp == cardtype) & (Guest.gastnr > 0)).first()
    while None != guest:
        nr = nr + 1
        guest_list = Guest_list()
        guest_list_list.append(guest_list)

        guest_list.nr = nr
        guest_list.guest_nr = guest.gastnr
        guest_list.salesid = guest.phonetik3

        masterguest = db_session.query(Masterguest).filter(
                 (Masterguest.gastnr == guest.master_gastnr)).first()

        if masterguest:
            mastername = masterguest.name + " " + masterguest.vorname1
        usr_list.clear()
        usr_list = get_output(read_bedienerbl(0, guest.phonetik3))

        usr = query(usr_list, first=True)

        if usr:
            sales_name = usr.username

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == guestseg.segmentcode)).first()

            if segment:
                mainsegm = entry(0, segment.bezeich, "$$0")

        akt_kont = db_session.query(Akt_kont).filter(
                 (Akt_kont.gastnr == guest.gastnr) & (Akt_kont.hauptkontakt)).first()

        if akt_kont:
            guest_list.maincontact = akt_kont.name
            guest_list.main_fname = akt_kont.vorname
            guest_list.main_tittle = akt_kont.anrede
            guest_list.main_bday = akt_kont.geburtdatum1
            guest_list.main_bplace = akt_kont.geburt_ort1
            guest_list.main_telp = akt_kont.telefon
            guest_list.main_ext = akt_kont.durchwahl
            guest_list.main_dept = akt_kont.abteilung
            guest_list.main_function = akt_kont.funktion
            guest_list.main_email = akt_kont.email_adr


        guest_list.guest_name = guest.name + " " + guest.vorname1
        guest_list.guest_title = guest.anredefirma
        guest_list.address1 = guest.adresse1
        guest_list.address2 = guest.adresse2
        guest_list.address3 = guest.adresse3
        guest_list.city = guest.wohnort
        guest_list.zip = guest.plz
        guest_list.country = guest.land
        guest_list.mastercomp = mastername
        guest_list.salesid = guest.phonetik3
        guest_list.salesid_name = sales_name
        guest_list.refno2 = to_string(guest.point_gastnr)
        guest_list.refno3 = to_string(guest.steuernr)
        guest_list.phone = guest.telefon
        guest_list.telefax = guest.fax
        guest_list.email = guest.email_adr
        guest_list.segmentcode = mainsegm


        mastername = ""
        sales_name = ""
        mainsegm = ""

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 231) & (Queasy.number1 == guest_list.guest_nr)).first()

        if queasy:
            guest_list.refno4 = queasy.char1

        t_queasy = db_session.query(T_queasy).filter(
                 (T_queasy.key == 212) & (T_queasy.number3 == guest_list.guest_nr)).first()

        if t_queasy:

            b_queasy = db_session.query(B_queasy).filter(
                     (B_queasy.key == 211) & (B_queasy.number1 == t_queasy.number1)).first()

            if b_queasy:
                guest_list.keyaccount = b_queasy.char1

        curr_recid = guest._recid
        guest = db_session.query(Guest).filter(
                 (Guest.karteityp == cardtype) & (Guest.gastnr > 0)).filter(Guest._recid > curr_recid).first()

    if crm_flag:

        for guest_list in query(guest_list_list, filters=(lambda guest_list: guest_list.refno4 == "")):
            guest_list_list.remove(guest_list)
        nr = 0

        for guest_list in query(guest_list_list):
            nr = nr + 1
            guest_list.nr = nr

    return generate_output()